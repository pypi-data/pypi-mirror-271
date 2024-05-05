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

    parser.add_argument("--hash_mode", type=int, choices=[0,1,2], default=1, required=False,
                       help="Hash mode: 0 is sha256sum, 1 is hashlib.sha256, 2 is sha512sum. Default 1.")

    parser.add_argument("--version", action="version", version=f"diwork {Global.version}",
                       help="Check version of diwork")

    return parser

def common_init_parse(args: "ArgumentParser.parse_args") -> None:
    Global.outfile = args.dublicate_out_to_file
    Global.hash_mode = args.hash_mode