from os.path import join, dirname
import os
import sys
import argparse
from ara_tools.version import __version__
from ara_tools.artefact_creator import ArtefactCreator
from ara_tools.artefact_renamer import ArtefactRenamer
from ara_tools.classifier import Classifier
from ara_tools.filename_validator import is_valid_filename
from ara_tools.classifier_validator import is_valid_classifier
from ara_tools.template_manager import SpecificationBreakdownAspects, TemplatePathManager
from ara_tools.artefact_deleter import ArtefactDeleter
from ara_tools.artefact_lister import ArtefactLister
from ara_tools.vectorDB import create_DB, add_paths, reset_config, reset_DB, search_DB, update_DB
from ara_tools.prompt_handler import read_prompt, send_prompt, append_headings, write_prompt_result, default_prompt_creation, initialize_prompt_templates, load_selected_prompt_templates, create_and_send_custom_prompt
from ara_tools.prompt_extractor import extract_and_save_prompt_results

from ara_tools.chat import Chat

def check_validity(condition, error_message):
    if not condition:
        print(error_message)
        sys.exit(1)

def create_action(args):
    if args.parameter and args.classifier and args.aspect:
        sba = SpecificationBreakdownAspects()
        try:
            sba.create(args.parameter, args.classifier, args.aspect)
        except ValueError as ve:
            print(f"Error: {ve}")
            sys.exit(1)

    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")
    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")

    template_path = join(dirname(__file__), 'templates')
    artefact_creator = ArtefactCreator()
    artefact_creator.run(args.parameter, args.classifier, template_path)

def delete_action(args):
    artefact_deleter = ArtefactDeleter()
    artefact_deleter.delete(args.parameter, args.classifier)


def rename_action(args):
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")
    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.aspect), "Invalid new filename provided. Please provide a valid filename.")

    artefact_renamer = ArtefactRenamer()
    artefact_renamer.rename(args.parameter, args.aspect, args.classifier)

def list_action(args):
    artefact_lister = ArtefactLister()
    if args.tags:
        artefact_lister.list_files(tags=args.tags)
    else:
        artefact_lister.list_files()
    

def prompt_action(args):
    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(is_valid_filename(args.parameter), "Invalid filename provided. Please provide a valid filename.")

    classifier = args.classifier
    param = args.parameter
    init = args.init
    
    if (init == 'init'):
        initialize_prompt_templates(classifier, param)
    elif (init == 'load'):
        load_selected_prompt_templates(classifier, param)
    elif (init == 'send'):
        create_and_send_custom_prompt(classifier, param)  # Use the new method when the 'send' command is used
    elif (init == 'extract'):
        extract_and_save_prompt_results(classifier, param)  # Use the new method when the 'send' command is used    
    
    else: # default rules.md, givens.md, prompt.md and commands.md files are used
        default_prompt_creation(classifier, param)
        prompt = read_prompt(classifier, param)
        
        if(prompt):
            append_headings(classifier, param, "prompt")
            write_prompt_result(classifier, param, prompt)
            
            response = send_prompt(prompt)
            append_headings(classifier, param, "result")
            write_prompt_result(classifier, param, response)


def chat_action(args):
    if args.name:
        # Start or continue specific chat
        chat_name = args.name
    else:
        # Start or continue default chat
        chat_name = "chat"
    chat = Chat(chat_name)
    chat.start()

def vector_action(args): 
    match args.vector_command:
        case 'init':
            create_DB()

        case 'update':
            if args.path:
                add_paths(args.path)
            if not args.path:
                update_DB()

        case 'reset':
            if args.config:
                reset_config()
            if not args.config:
                reset_DB()

        case 'search':
            search_DB(args.amount, args.user_input)

def template_action(args):
    check_validity(is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")
    check_validity(Classifier.is_valid_classifier(args.classifier), "Invalid classifier provided. Please provide a valid classifier.")

    template_manager = TemplatePathManager()
    content = template_manager.get_template_content(args.classifier)

def handle_invalid_action(args):
    sys.exit("Invalid action provided. Type ara -h for help")

def create_parser(subparsers):
    create_parser = subparsers.add_parser("create", help="Create a file with a classifier and aspect")
    create_parser.add_argument("parameter", help="Filename for create action")
    create_parser.add_argument("classifier", help="Classifier for the file to be created")
    create_parser.add_argument("aspect", help="Specification breakdown aspect", nargs='?', default=None)

def delete_parser(subparsers):
    delete_parser = subparsers.add_parser("delete", help="Delete a file with a classifier")
    delete_parser.add_argument("parameter", help="Filename for delete action")
    delete_parser.add_argument("classifier", help="Classifier for the file to be deleted")

def rename_parser(subparsers):
    rename_parser = subparsers.add_parser("rename", help="Rename a file with a classifier and new filename")
    rename_parser.add_argument("parameter", help="Current filename for rename action")
    rename_parser.add_argument("classifier", help="Classifier for the file to be renamed")
    rename_parser.add_argument("aspect", help="New filename for the file")

def list_parser(subparsers):
    list_parser = subparsers.add_parser("list", help="List files with optional tags")
    list_parser.add_argument("tags", nargs="*", help="Tags for listing files")

def prompt_parser(subparsers):
    prompt_parser = subparsers.add_parser("prompt", help="Creates a prompt and sends it to ChatGPT and save the result")
    prompt_parser.add_argument("parameter", help="Filename for prompt action")
    prompt_parser.add_argument("classifier", help="Classifier for the file to be prompted")
    prompt_parser.add_argument("init", help="initialize | load | send the prompt template config selection file in the prompt directory", nargs='?', default=None)

def vector_init_parser(vector_subparsers):
    init_parser = vector_subparsers.add_parser("init", help="Initialize vectorDB")

def vector_update_parser(vector_subparsers):
    update_parser = vector_subparsers.add_parser("update", help="Update vectorDB")
    update_parser.add_argument("path", nargs='*', help="Path(s) to add to config file", default=None)

def vector_reset_parser(vector_subparsers):
    reset_parser = vector_subparsers.add_parser("reset", help="Reset vectorDB")
    reset_parser.add_argument("config", nargs="?", help="Optional config to reset", default=None)

def vector_search_parser(vector_subparsers):
    search_parser = vector_subparsers.add_parser("search", help="Search vectorDB")
    search_parser.add_argument("amount", nargs="?", help="Amount of paths to return from search", default=4, type=int)
    search_parser.add_argument("user_input", help="Required query to be executed on vectorDB")

def vector_parser(subparsers):
    vector_parser = subparsers.add_parser("vector")
    vector_subparsers = vector_parser.add_subparsers(dest='vector_command')

    vector_init_parser(vector_subparsers)
    vector_update_parser(vector_subparsers)
    vector_reset_parser(vector_subparsers)
    vector_search_parser(vector_subparsers)

def chat_parser(subparsers):
    chat_parser = subparsers.add_parser("chat", help="Command line chatbot")
    chat_parser.add_argument("name", help="Optional name for a specific chat. Pass the .md file to continue an existing chat", nargs='?', default=None)

def template_parser(subparsers):
    template_parser = subparsers.add_parser("template", help="Output ara template")
    template_parser.add_argument("classifier", help="Classifier for ara artefact type")

# TODO hack for ara-list command for listing python files
def crawl_directory(start_dir):
    python_files = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            if file.endswith(".py"):
                python_files.append(os.path.join(root, file))
    return python_files

def format_output(files):
    formatted_output = "Source files\n"
    for file in files:
        formatted_output += f"  - [ ] {file}\n"
    return formatted_output

def save_to_file(output, filename):
    with open(filename, "w") as f:
        f.write(output)

def list():
    if len(sys.argv) != 3:
        print("Usage: python script.py <start_directory> <output_filename>")
        sys.exit(1)

    start_dir = sys.argv[1]
    output_filename = sys.argv[2]

    python_files = crawl_directory(start_dir)
    output = format_output(python_files)
    save_to_file(output, output_filename)
    print(f"File list saved to {output_filename}")

def cli():
    parser = argparse.ArgumentParser(description="Ara tools for creating files and directories.")
    # Add version argument
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')

    subparsers = parser.add_subparsers(dest="action", help="Action to perform")

    create_parser(subparsers)
    delete_parser(subparsers)
    rename_parser(subparsers)
    list_parser(subparsers)
    prompt_parser(subparsers)
    vector_parser(subparsers)
    chat_parser(subparsers)
    template_parser(subparsers)

    action_mapping = {
        "create": create_action,
        "delete": delete_action,
        "rename": rename_action,
        "list": list_action,
        "prompt": prompt_action,
        "vector": vector_action,
        "chat": chat_action,
        "template": template_action
    }

    args = parser.parse_args()
    if hasattr(args, 'action') and args.action:
        action = action_mapping.get(args.action, handle_invalid_action)
        action(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    cli()
