# Contains the main parser of getodo 

try:
    from getodo import utils
except ImportError:
    import utils

from os import path, scandir, getcwd
from colorama import Fore, Style, init

class TodoParser:

    def __init__(self, parse_path, out_file, print_to_term, ignore) -> None:
        
        init() # Colorama

        self.cfg: dict = utils.load_getodo_cfg()
        self._todo: list = self.cfg['_todo']
        self._comments: dict = self.cfg['comment_syntax']
        self._ignored: list = self.cfg['default_ignored']
        self.output: dict = {}

        self.parse_path: str = parse_path if not parse_path == "." else getcwd()
        # Create a out file specified by user or a default  in the folder where `getodo` is run
        self.out_file: str = out_file 
        self.print_to_term: bool = print_to_term
        self.ignore: list = ignore

        if self.ignore:
            # User provided path(s) to ignore
            for item in self.ignore:
                if path.basename(item):
                    self._ignored.append(path.basename(item))
                else:
                    item: str = path.dirname(item)
                    try:
                        if item.index("/") != 0:
                            self._ignored.append(item.split("/")[-1])
                        else:
                            self._ignored.append(item)
                    except:
                        self._ignored.append(item)
                    

        if path.isdir(parse_path):
            # User provided a directory to parse
            self.parse_dir(parse_path)
            pass

        else:
            # User provided a file to parse
            self.parse_file(parse_path)
            pass
        
        if not self.output:
            print(Fore.RED + Style.BRIGHT + "NO TODO (s) found" + Style.RESET_ALL)
            exit(0)

        if self.print_to_term:
            self.print_to_terminal()
            # Below condition will determine whether or not to save to a file depending 
            # on how the user has used the flags
            # Check the end of `getodo_cli.py` to know how the flags work

            if self.out_file: # If user wants to save to a file
                if not self.out_file == "no_out":
                    self.write_out_file() # Save to file defined by user
                else:
                    self.out_file = self.cfg['default_out_file']
                    self.write_out_file() # Save to default file
        
        else:

            if not self.out_file: # No output file was provided by user
                self.out_file = self.cfg['default_out_file']
                self.write_out_file()
            
            else: # Output file was provided by user 
                if self.out_file == "no_out": 
                    # This check is need to see whether user has not passed any out_file
                    # when only the -o flag is used
                    utils.print_error("Please provide a path to a output file in which you wish to save the output")
                    exit(-1)
                self.write_out_file()


    def parse_dir(self, dir: str):
        # Recursively walk the directory and when the file is encountered, parse it
        dir_contents = scandir(dir)
        
        for contents in dir_contents:
            # use contents.name
            if utils.is_ignored(self.parse_path, contents.name, self._ignored):
                continue
            
            if contents.is_dir():
                self.parse_dir(contents.path)
            
            if contents.is_file():
                self.parse_file(contents.path)


    def parse_file(self, file: str):
        try:
            with open(file) as f:
                # Parse TODO from the file
                current_comment_syntax = utils.get_comment_syntax(f.name, self._comments)
                
                if not current_comment_syntax:
                    # print(f"File type of {f.name} is not yet implemented [ADD TO IGNORE FILES]")
                    pass
                
                else:
                    line_num = 0
                    file_todo = {}
                    for line in f.readlines():
                        line = line.strip()
                        line_num += 1

                        if any(line.startswith(syntax) for syntax in current_comment_syntax):
                            line = line[utils.get_first_letter_index(line):]
                            
                            if any(line.startswith(todo) for todo in self._todo):
                                file_todo[line_num] = line
                    
                    if file_todo:
                        self.output[f.name] = file_todo
        except Exception as e:
            utils.print_error(e)


    def print_to_terminal(self):
        for key,value in self.output.items():
            print(Fore.GREEN + Style.BRIGHT + "\n[FILE] "+Fore.LIGHTRED_EX+f"{key}\n"+Style.RESET_ALL)
            for line_num, content in value.items():
                print(Fore.CYAN + Style.BRIGHT + f"[Line {line_num}] " + Style.RESET_ALL + Fore.WHITE + f"{content}" + Style.RESET_ALL)


    def write_out_file(self):
        #TODO: output file is being saved in folder where getodo is run
        # Change it to folder of parse_path
        try:
            with open(self.out_file, "w+") as f:
                for key, value in self.output.items():
                    f.write(f"[FILE] {key}\n")
                    for line_num, content in value.items():
                        f.write(f"\n[Line {line_num}] {content}")
                    f.write("\n--------------------------------------------------------------------------------\n")
            print(Fore.GREEN + Style.BRIGHT + f"\nTODO(s) written to {path.abspath(self.out_file)}" + Style.RESET_ALL)
            utils.add_to_gitignore(self.parse_path, self.out_file)
        except Exception as e:
            utils.print_error(e)


# TODO: IDEA: Find a way to support multi line TODO's without having to type TODO in each line