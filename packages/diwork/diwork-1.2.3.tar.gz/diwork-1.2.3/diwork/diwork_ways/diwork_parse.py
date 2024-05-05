# -*- coding: utf-8 -*-

import os
import sys
import argparse

from . import Global

def common_init_parser(parser: "ArgumentParser") -> "ArgumentParser":
    # https://docs.python.org/3/library/argparse.html
    # https://stackoverflow.com/questions/20063/whats-the-best-way-to-parse-command-line-arguments

    parser.add_argument("--dublicate_out_to_file", type=str, default=None, required=False,
                       help="Duplicate program output to file")

    parser.add_argument("--version", action="version", version=f"diwork {Global.version}",
                       help="Check version of diwork")

    parser.add_argument("--symlink_mode", type=int, choices=[0, 1, 2], default=2, required=False,
                       help="What to do with links: 0 - ignor, 1 - consider link content, 2 - use the file where the link refers to. Default 2.")
    return parser

def common_init_parse(args: "ArgumentParser.parse_args") -> None:
    Global.outfile = args.dublicate_out_to_file
    Global.symlink_mode = args.symlink_mode
