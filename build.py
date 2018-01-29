import os
from os import path
from shutil import copy
from generate import SOURCE_PATH, OUTPUT_PATH
from generate.codes import CodeList


def main():
    if not path.isdir(OUTPUT_PATH):
        os.mkdir(OUTPUT_PATH)
    l = CodeList.parse_from_file('code.yaml')
    l.generate()
    for file in os.listdir(SOURCE_PATH):
        copy(path.join(SOURCE_PATH, file), path.join(OUTPUT_PATH, file))


if __name__ == '__main__':
    main()
