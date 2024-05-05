# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_help(args: list, modules: str):
    text = f"""
Available modules: {modules}.
To choose a module, run the command:
> diwork {'{module_name}'} ...

For example:
> diwork hash ...

If the syntax is incorrect, it will show the help and description of the selected module.

For example. To show the help and description of module clone, run the command:
> diwork clone

Some modules require the help flag to be specified explicitly. For example:
> diwork hash --help
"""
    pout(text)
