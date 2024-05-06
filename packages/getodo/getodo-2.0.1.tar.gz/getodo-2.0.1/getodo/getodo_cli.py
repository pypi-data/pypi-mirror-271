# Contains the CLI of getodo

try:
    from getodo.getodo import TodoParser
except:
    from getodo import TodoParser

try:
    from getodo import utils
except:
    import utils

import argparse


def main():
    parser = argparse.ArgumentParser(description="Scan a file or a directory and extract all the TODO into a file/stdout")

    # Required Arguments

    parser.add_argument("parse_path", help="Directory/file to parse for TODO's")

    # Flags

    parser.add_argument("-o", "--output", nargs="?", const="no_out", help="File to store the output")
    parser.add_argument("-t", "--term", action="store_true", help="Print the output to terminal")
    parser.add_argument("-i", "--ignore", nargs="+", help="Ignore directories and files")

    args = parser.parse_args()

    # Arguments

    parse_path = args.parse_path
    out_file = args.output
    print_to_term = args.term
    ignore = args.ignore

    TodoParser(parse_path=parse_path, out_file=out_file, print_to_term=print_to_term, ignore=ignore)


if __name__ == '__main__':
    main()


# -------------------- HOW THE FLAGS WORK--------------------

# getodo parse_path -> Just stores to outfile(rn default(will be changed when configs added))
# getodo parse_path -t -> Only prints to terminal
# getodo parse_path -o out_file -> Saves to file provided by the user
# getodo parse_path -t -o -> Prints to term and stores to out file(rn default, in future will be changed when configs are added)
# getodo parse_path -t -o filename -> Prints to term and stores to outfile(name specified by user)
# getodo parse_path -i ignorepath1 ignorepath2 ... -> Stores to default outfile and ignores the given ignore paths(i.e does not parse for TODO(s))

# -----------------------------------------------------------
