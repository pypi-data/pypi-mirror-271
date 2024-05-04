import os
import re
import sys
import yaml
import subprocess
from rich.console import Console

from agent.utils import Config
from agent.types import ProjectState
from agent.const import CONFIG_PROJECT_FILE


def list_all_files(path):
    """
    Lists all files and directories under the given path if it is a directory.
    If the path is a file, returns None.

    Args:
    path (str): The file system path to check and list contents from.

    Returns:
    list of str or None: A list of file and directory names under the given path, or None if the path is a file.
    """
    if os.path.isfile(path):
        return None  # Return None if the path is a file

    file_list = []
    for root, dirs, files in os.walk(path):
        for name in files:
            file_list.append(os.path.join(root, name))
        for name in dirs:
            file_list.append(os.path.join(root, name))

    return file_list


def create_directory(dir_name: str):
    """
    Create a directory if it does not exist.
    :param dir_name: the name of the directory to create.
    :return: the directory created.
    """
    console = Console()
    cwd = os.getcwd()
    path = os.path.join(cwd, dir_name)

    try:
        os.makedirs(path, exist_ok=True)
        console.log(f"[green]Directory '{path}' created successfully.")
    except OSError as error:
        console.log(f"[red]Creation of the directory '{path}' failed due to: {error}")
    return path


def get_directory_name(path):
    """
    Get the directory name if the path is a directory.
    :param path: the path to check.
    :return: the directory name if it's a directory, otherwise None.
    """
    if os.path.isdir(path):
        return os.path.basename(path)
    else:
        return None


def read_project_state(config_path: str = None):
    """
    Read the project state.
    :return: the project state.
    """
    console = Console()
    if not config_path:
        config_path = os.path.join(os.getcwd(), CONFIG_PROJECT_FILE)

    if not os.path.exists(config_path):
        console.log(f"[red]The file {config_path} does not exist.")
        return None

    try:
        with open(config_path, 'r') as file:
            data = yaml.safe_load(file)
            return ProjectState(**data)
    except FileNotFoundError:
        console.log(f"[red]The file {config_path} does not exist.")
        return None
    except yaml.YAMLError as error:
        console.log(f"[red]Error parsing YAML file: {error}")
        return None
    except Exception as error:
        console.log(f"[red]An error occurred: {error}")
        return None


def update_project_state(project_path: str, content_dict: dict = None):
    """
    Update the project state.
    :param project_path: the path of the project.
    :param content_dict: the content dictionary to update.
    """
    console = Console()
    file_path = os.path.join(project_path, CONFIG_PROJECT_FILE)

    try:
        with open(file_path, 'w') as file:
            yaml.dump(content_dict, file)
        console.log(f"[green]File '{file_path}' updated successfully.")
    except IOError as error:
        console.log(f"[red]Updating the file '{file_path}' failed due to: {error}")


def extract_and_save_file(input_text):
    """
    Extracts the file name and code block from a text formatted as specified,
    then creates a local file with the file name and writes the code into it.

    Args:
    input_text (str): The text containing the file name and code block.

    Returns:
    str: The name of the file created.
    """
    console = Console()
    file_name_match = re.search(r"File Name:\s*(.*?)\s*\n+\s*Code:", input_text, re.DOTALL)
    if not file_name_match:
        console.log("File name not found in the text.")
        return None, None

    file_name = file_name_match.group(1).strip()

    project_file_path = os.path.join(Config().read()['project']['path'], file_name)
    code_match = re.search(r"```(?:[a-zA-Z0-9]+)?\n(.*?)```", input_text, re.DOTALL)
    if not code_match:
        console.log("Code block not found in the text.")
        return None, None

    code = code_match.group(1).strip()
    with open(project_file_path, 'w') as file:
        file.write(code)

    return project_file_path, code


def extract_file_name(text: str) -> str:
    """
    Extracts the file name from a given text string.

    Args:
    text (str): The text containing the file name.

    Returns:
    str: The extracted file name, or an empty string if no file name is found.
    """
    match = re.search(r'File Name: (\S+)', text)
    if match:
        return match.group(1)
    else:
        return None


def extract_code(text: str) -> str:
    """
    Extracts the code block from a given text string.

    Args:
    text (str): The text containing the code block.

    Returns:
    str: The extracted code block, or an empty string if no code block is found.
    """
    match = re.search(r'```(?:[a-zA-Z0-9]+)?\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1)
    else:
        return None


def load_yaml_file(file_path: str):
    """
    Load a YAML file and return the data.
    :param file_path: the path of the YAML file.
    :return: the data in the YAML file.
    """
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    return data


def read_file_to_string(file_path: str):
    """
    Reads the contents of a file and returns it as a string.

    Args:
    file_path (str): The path to the file that needs to be read.

    Returns:
    str: The contents of the file as a string.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        return None


def run_command(command):
    """
    Run a command in the shell and return the output and error.
    :param command: the input command to run.
    :return: the output and error.
    """
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        output = ''
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            output += line

        return output
    except Exception as e:
        return str(e)