# pip install gitignore_parser
import argparse
import sys
import os, json
from zipfile import ZipFile

endings = {
    ".pyc",
    ".git",
}

ignored_files = {
    ".git",
    ".gitignore",
    ".gitattributes",
    "build.zip",
    "settings.json"
}

non_relative_folders = {
    "__pycache__",
    ".git",
    "cache",
    "downloads",
    "cache",
    "scripts",
    "tools",
    "img"
} 


def create_arg_parser():
    """"Creates and returns the ArgumentParser object."""
    parser = argparse.ArgumentParser(description='Point towards a valid github repo to build a zipfile respecting the buildignore.')
    parser.add_argument('inputDirectory',
                    help='Path to the input directory.')
    return parser

def matches(basepath, root, file):
    if not root:
        sys.exit("No root passed to matching function")

    if not file:
        sys.exit("No file passed to matching function")

    if not os.path.isfile(os.path.join(root, file)):
        sys.exit("Passed file does not exist")
    if file in ignored_files:
        return

    for folder in non_relative_folders:
        if root.endswith(folder):
            return

    for folder in non_relative_folders:
        fold = root
        finished = False
        while not finished:
            if fold == basepath:  
                break
            if fold.endswith(folder):
                return

            fold = os.path.dirname(fold)
            if not fold:
                finished = True


    for ending in endings:
        if file.endswith(ending):
            return

    return(os.path.join(root, file))


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    wd = parsed_args.inputDirectory
    if not os.path.isdir(wd):
        sys.exit("Invalid path passed")

    files = []
    # r=root, d=directories, f = files
    output = os.path.join(wd, "build.zip")
    with ZipFile(output, 'w') as build_zip:
        for r, d, f in os.walk(wd):
            for file in f:
                approved_file = matches(wd, r, file)
                if approved_file:
                    rel_file = os.path.relpath(approved_file, wd)
                    build_zip.write(approved_file,rel_file)
                    files.append(approved_file)
                    print("Archived - {}".format(file))

        print(json.dumps(files, indent = 4))