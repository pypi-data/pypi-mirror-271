from ara_tools.prompt_handler import send_prompt, get_file_content
from ara_tools.classifier import Classifier
import re
import json
import os

from markdown_it import MarkdownIt

def extract_code_blocks_md(markdown_text):
    md = MarkdownIt()
    tokens = md.parse(markdown_text)
    code_blocks = [token.content for token in tokens if token.type == 'fence']
    return code_blocks

def extract_responses(document_path):
    print(f"Debug: Starting extraction from {document_path}")
    block_extraction_counter = 0

    with open(document_path, 'r') as file:
        content = file.read()
    
    code_blocks_found = extract_code_blocks_md(content)
    for block in code_blocks_found:
        if "# [x] extract" in block:
            print("Block found and processed.")
            file_path_search = re.search(r"# filename: (.+)", block)
            if file_path_search:
                file_path = file_path_search.group(1).strip()
                print(f"Debug: Filename extracted: {file_path}")
                handle_existing_file(file_path, block)
                block_extraction_counter += 1
            else:
                print("No filename found, skipping this block.")
        else:
            print("Block found but skipped due to absence of extract tag.")
    
    print(f"Debug: End of extraction. Found {block_extraction_counter} blocks.")

    
def modify_and_save_file(response, file_path):
    print(f"Debug: Modifying and saving file {file_path}")
    try:
        response_data = json.loads(response)
        filename_from_response = response_data['filename']
        print(f"Debug: Response parsed, filename from response: {filename_from_response}")

        if filename_from_response != file_path:
            user_decision = prompt_user_decision("Filename does not match, overwrite? (y/n): ")
            if user_decision.lower() not in ['y', 'yes']:
                print("Debug: User chose not to overwrite")
                print("Skipping block.")
                return
        content = response_data['content']
        with open(file_path, 'w') as file:
            file.write(content)
            print(f"Debug: File {file_path} updated successfully.")
    except json.JSONDecodeError:
        print("ERROR: Failed to decode JSON response.")

def create_file_if_not_exist(filename, content):
    print(f"Debug: Checking if file exists: {filename}")
    if not os.path.exists(filename):
        print("Debug: File does not exist, prompting user")
        user_decision = prompt_user_decision("File does not exist. Create? (y/n): ")
        if user_decision.lower() in ['y', 'yes']:
            with open(filename, 'w') as file:
                file.write(content)
                print(f"Debug: File {filename} created successfully.")
        else:
            print("Debug: User skipped file creation")
            print("File creation skipped by user.")

def create_prompt_for_file_modification(content_str, filename):
    print(f"Debug: Creating modification prompt for {filename}")
    
    if not os.path.exists(filename):
        print(f"WARNING: {filename} for merge prompt creation does not exist.")
        return

    content_of_existing_file = json.dumps(get_file_content(filename))
    content = json.dumps(content_str)

    prompt_text = f"""
    * given this new_content: 
    ```
    {content}
    ```
    * and given this existing file {filename}
    ```
    {content_of_existing_file}
    ```
    * then merge the new content into {filename}
    * merge the provided information only; do not add any new details
    * as prompt response format of the merged file use strictly the following json format. Escape special characters properly so that your response is always a valid json format:
    {{
        "filename": "path\\ filename.filextension",
        "content":  "full content of the modified file",
    }}
    * do not respond any more than the specified valid json response format 
    """

    print(f"Debug: modification prompt created: {prompt_text}")

    return prompt_text

def handle_existing_file(filename, block_content):
    print(f"Debug: Handling existing file: {filename}")
    if not os.path.isfile(filename):
        print(f"Debug: File does not exist, attempting to create")
        create_file_if_not_exist(filename, block_content)
    else:
        print(f"Debug: File exists, creating modification prompt")
        prompt = create_prompt_for_file_modification(block_content, filename)
        response = send_prompt(prompt)
        print(f"DEBUG: got this response: {response}")
        modify_and_save_file(response, filename)


def prompt_user_decision(prompt_message):
    print(f"Debug: Prompting user with message: {prompt_message}")
    return input(prompt_message)

def extract_and_save_prompt_results(classifier, param):
    print(f"Debug: Extracting and saving prompt results for classifier {classifier} with param {param}")
    sub_directory = Classifier.get_sub_directory(classifier)
    exploration_file = f"ara/{sub_directory}/{param}.data/{classifier}_exploration.md"
    print(f"Debug: Computed exploration file path: {exploration_file}")

    extract_responses(exploration_file)