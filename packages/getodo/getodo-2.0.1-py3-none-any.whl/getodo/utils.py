# Contains all utility functions required for getodo

from os import path
from json import loads
from colorama import Fore, Style
from re import match


def load_getodo_cfg() -> dict:
    # Loads the content of getodo_cfg.json
    try:
        with open(path.join(path.dirname(__file__), "getodo_cfg.json"), "r") as f:
            json_data = f.read()
        return loads(json_data)
    except Exception as e:
        print_error(e)


def get_comment_syntax(file: str, _comments: dict) -> list | None:
    file_type = file[file.rindex('.'):]
    return _comments.get(file_type, '')


def get_first_letter_index(s: str) -> int:
    for c in s:
        if c.isalpha():
            return s.index(c)
        

def print_error(e: Exception | str) -> None:
    print(Fore.RED + Style.BRIGHT + "Encountered Error" + Style.RESET_ALL)
    print(e)
    exit(-1)


def add_to_gitignore(parse_path: str, out_file: str) -> None:
    # Assume .gitignore is in the directory of the parse_path
    gitignore_root = path.abspath(parse_path)
    gitignore_file = path.join(gitignore_root, ".gitignore")
   
    if path.exists(gitignore_file):
        try:
            with open(gitignore_file, "r") as f:
                lines = f.readlines()
                for line in lines:
                    if line.strip() == out_file:
                        exit(0)
            with open(gitignore_file, "a") as f:
                f.write(out_file + "\n")
                print(Fore.GREEN + Style.BRIGHT + f"Appended {out_file} to {gitignore_root}" + Style.RESET_ALL)
        except Exception as e:
            print_error(e)

    else:
        print(Fore.RED + Style.BRIGHT + f"No .gitignore found in {gitignore_root} to append the output file name to it" + Style.RESET_ALL)


def is_ignored(parse_path: str, file_path: str, list_ignored: list) -> bool:
    if path.exists(path.join(path.abspath(path.join(parse_path, file_path)), "pyvenv.cfg")):
        return True # It is a virtual env directory

    for ignore in list_ignored:
        if file_path.endswith(ignore):
            return True
    return False