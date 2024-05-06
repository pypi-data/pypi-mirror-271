# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

def main_difx(args: list):
    argc = len(args)
    if(argc != 2):
        pout("This module will show the difference between the two directories.\n")
        pout("Syntax error. Expected: \"python folder_work.py difx {folder1} {folder2}\"")
        exit()
    folder1 = args[0]
    folder2 = args[1]
    err_out = []
    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)
    if(is_folder(folder1_abs) == False):
        pout(f"\"{folder1_abs}\" is not folder. ")
        exit()
    if(is_folder(folder2_abs) == False):
        pout(f"\"{folder2_abs}\" is not folder. ")
        exit()

    files1_abs, files2_abs = sorted(get_files_list(folder1_abs)), sorted(get_files_list(folder2_abs))
    dr1, dr2 = {}, {}
    gi, N = 0, len(files1_abs)+len(files2_abs)
    for file_i in files1_abs:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        file_i_rel = rel_path(file_i, folder1_abs)
        dr1[file_i_rel] = file_i_hash
    for file_i in files2_abs:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        file_i_hash = get_hash_file(file_i)
        pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        file_i_rel = rel_path(file_i, folder2_abs)
        dr2[file_i_rel] = file_i_hash
    files1_rel, files2_rel = list(dr1.keys()), list(dr2.keys())
    files1_rel_set, files2_rel_set = set(dr1.keys()), set(dr2.keys())

    pout("\n===============\nDifx:")

    IF_AT_LEAST_ONE = False

    for file_i in files1_rel:
        if(file_i in files2_rel_set and dr1[file_i] != dr2[file_i]):
            IF_AT_LEAST_ONE = True
            file1_i_abs = os.path.join(folder1_abs, file_i)
            file2_i_abs = os.path.join(folder2_abs, file_i)
            pout("*\t\t\t==========Difx changed==========")
            pout(f"\t\"{file1_i_abs}\" with hash=\"{dr1[file_i]}\"")
            pout(f"\t\"{file2_i_abs}\" with hash=\"{dr2[file_i]}\"\n")
    
    for file_i in files1_rel:
        if(file_i not in files2_rel_set):
            pout("*\t\t\t==========Difx new/removed==========")
            IF_AT_LEAST_ONE = True
            pout(f"\t\"{file_i}\"     IN \"{folder1_abs}\"")
            pout(f"\t\"{file_i}\" NOT IN \"{folder2_abs}\"")

    for file_i in files2_rel:
        if(file_i not in files1_rel_set):
            pout("*\t\t\t==========Difx new/removed==========")
            IF_AT_LEAST_ONE = True
            pout(f"\t\"{file_i}\" NOT IN \"{folder1_abs}\"")
            pout(f"\t\"{file_i}\"     IN \"{folder2_abs}\"")

    if(IF_AT_LEAST_ONE == False):
        pout("\tNo such files")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")
