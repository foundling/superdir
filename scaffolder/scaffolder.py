#!/usr/bin/env python
# -*- coding: utf-8 -*-


import datetime
import os
import sys

import click

from tree import Tree
import utils
from validator import Validator
from walk_funcs import make_line_printer
from walk_funcs import make_file_creator

def main():

    SCHEMA_FILE, OUTPUT_DIR, ABS_BASE_PATH = utils.handle_args(sys.argv)

    raw_lines = open(SCHEMA_FILE).readlines()
    schema = utils.clean(raw_lines)

    validator = Validator()
    validator.load_schema(schema)
    indent_size = validator.validate()

    directory_tree = Tree(

        indent_size = indent_size,
        output_dir = OUTPUT_DIR

    )
    directory_tree.load_data(schema)
    directory_tree.build_tree()

    file_creator = make_file_creator(ABS_BASE_PATH)
    directory_tree.walk(callback=file_creator)

if __name__ == '__main__':
    main()
