# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_repeats(args: list):
    parser = argparse.ArgumentParser(prog = "diwork repeats",
        description="This module will find duplicates (exactly the same files) in the directory")
    parser.add_argument("folder_path", type=str, nargs=1,
                       help="Path to directory where repeats will be found")
    parser.add_argument("--delete", default=False, action='store_true',
                       help="Deletes files so that only 1 duplicate remains")
    parser.add_argument("--yes", default=False, action='store_true',
                       help="No interractive. Answer \"yes\" always. ")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    folder = args.folder_path[0]
    IF_DELETE = args.delete
    IF_YES = args.yes
    err_out = []
    files_to_delete = []
    folder_abs = os.path.abspath(folder)
    if(is_folder(folder_abs) == False):
        pout(f"\"{folder_abs}\" is not folder. ")
        exit()
    files_abs = sorted(get_files_list(folder_abs))
    hashes = set()
    d = {}
    gi, N = 0, len(files_abs)
    for file_i in files_abs:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        if(file_i_hash not in hashes):
            hashes.add(file_i_hash)
            d[file_i_hash] = [file_i]
        else:
            d[file_i_hash].append(file_i)

    pout("\n===============\nIdentical files: ")
    IF_AT_LEAST_ONE = False
    hashesss = list(d.keys())
    for hash_i in hashesss:
        fl = d[hash_i]
        if(len(fl) > 1):
            IF_AT_LEAST_ONE = True
            pout(f"* Hash \"{hash_i}\" have files: ")
            li = 0
            for file_i in fl:
                if(li > 0 and IF_DELETE):
                    pout(f"\t{file_i} (will be deleted)")
                    files_to_delete.append(file_i)
                else:
                    pout(f"\t{file_i}")
                li-=-1
            pout("")

    if(IF_AT_LEAST_ONE == False):
        pout("\tNo such files")
    else:
        pout("\nThis file will be delete:")
        for del_file_i in files_to_delete:
            pout(f"\"{del_file_i}\"")
        if(IF_YES == False):
            input(f"Type enter to continue or press CTRL+C to cancel.")
        for del_file_i in files_to_delete:
            os.remove(del_file_i)
        pout("DELETED: OK")



    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")
