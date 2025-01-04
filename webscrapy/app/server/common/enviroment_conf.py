import os
from dotenv import load_dotenv, dotenv_values, find_dotenv
from pathlib import Path


def get_path_file(folder1: str, folder2: str, file: str) -> Path:
    #root_dir = Path(__file__).parent.parent.parent
    root_dir = os.getcwd()
    if folder2 is None:
        path_complete = os.path.join(root_dir, folder1, file)
    else:
        path_complete = os.path.join(root_dir, folder1, folder2, file)
    return path_complete


def env_check():
    env_file = None
    if os.environ['ENVIRONMENT_TYPE'] == 'DEV':
        path_file = get_path_file(folder1="env", folder2=None, file="dev.env")
        print("PATH.ENV DEV", path_file)
        env_file = find_dotenv(path_file)
        load_dotenv(env_file)

    elif os.environ['ENVIRONMENT_TYPE'] == 'PRO':
        path_file = get_path_file(folder1="env", folder2=None, file="pro.env")
        print("PATH.ENV DEV", path_file)
        env_file = find_dotenv(path_file)
        load_dotenv(env_file)
    load_dotenv(env_file)
