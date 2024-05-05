# -*- coding: utf-8 -*-

import os
import sys

from diwork_ways import pout, Global

from diwork_mains import *

from . import __version__

VERSION = __version__

def main():
    MODULES = "{help, hash, clone, diffclone, sshclone, diff, difx, repeats, exec, archive}"
    SyntaxError_str = f"Syntax error. Expected: \"> python folder_work.py {MODULES} ...\""
    argc = len(sys.argv)
    Global.version = VERSION
    if(argc < 2):
        pout(SyntaxError_str)
        exit()
    else:
        sub_modul_name = sys.argv[1]
        if(sub_modul_name == "hash"):
            main_hash(sys.argv[2:])
        elif(sub_modul_name == "clone"):
            main_clone(sys.argv[2:])
        elif(sub_modul_name == "diffclone"):
            main_diffclone(sys.argv[2:])
        elif(sub_modul_name == "sshclone"):
            main_sshclone(sys.argv[2:])
        elif(sub_modul_name == "diff"):
            main_diff(sys.argv[2:])
        elif(sub_modul_name == "repeats"):
            main_repeats(sys.argv[2:])
        elif(sub_modul_name == "difx"):
            main_difx(sys.argv[2:])
        elif(sub_modul_name == "exec"):
            main_exec(sys.argv[2:])
        elif(sub_modul_name == "archive"):
            main_archive(sys.argv[2:])
        elif(sub_modul_name == "help"):
            main_help(sys.argv[2:], MODULES)
        else:
            pout(SyntaxError_str)
            exit()

