from setuptools import setup, find_packages
import os

# Import version number
version = {}
with open("./ara_tools/version.py") as fp:
    exec(fp.read(), version)

setup(
    name="ara-tools",
    version=version['__version__'],
    packages=find_packages(),
    include_package_data=True,  # Add this line
    entry_points={
        "console_scripts": [
            "ara = ara_tools.__main__:cli",
            "ara-list = ara_tools.__main__:list",
        ],
    },
    install_requires=[
        'langchain',
        'langchain-community',
        'langchain_openai',
        'openai',
        'markdown-it-py',
        # Add your package dependencies here
    ],
)

