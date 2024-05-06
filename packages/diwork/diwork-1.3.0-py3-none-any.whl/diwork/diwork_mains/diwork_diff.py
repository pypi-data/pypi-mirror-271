# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *


def diff_new_files(dr1, dr2) -> list:
    '''Do not need hash'''
    files_rel_old, files_rel_new = set(dr1.keys()), set(dr2.keys())
    res = []
    for file_i in files_rel_new:
        if(file_i not in files_rel_old):
            res.append(file_i)
    return res

def diff_changes_files(dr1, dr2) -> list:
    files_rel_old, files_rel_new = set(dr1.keys()), set(dr2.keys())
    res = []
    for file_i in files_rel_new:
        if(file_i in files_rel_old):
            if(dr1[file_i] != dr2[file_i]):
                res.append(file_i)
    return res

def diff_removed_files(dr1, dr2) -> list:
    '''Do not need hash'''
    files_rel_old, files_rel_new = set(dr1.keys()), set(dr2.keys())
    res = []
    for file_i in files_rel_old:
        if(file_i not in files_rel_new):
            res.append(file_i)
    return res

def diff_moved_files(dr1, dr2, old_folder_path, new_folder_path) -> list:
    files_rel_old, files_rel_new = set(dr1.keys()), set(dr2.keys())
    res = []
    for file_i_old in files_rel_old:
        S = f"File \"[{old_folder_path}] {file_i_old}\" has been moved (renamed) to: \n"
        S += f"\t\t{dr1[file_i_old]}\n"
        IF_AT_LEAST_ONE = False
        for file_i_new in files_rel_new:
            if(dr1[file_i_old] == dr2[file_i_new]):
                if(file_i_old != file_i_new):
                    if(file_i_new not in files_rel_old):
                        IF_AT_LEAST_ONE = True
                        S += f"\t[{new_folder_path}] {file_i_new}"
        if(IF_AT_LEAST_ONE == True):
            res.append(S)
    return res

def diff_identical_files(d1, d2, old_folder_path, new_folder_path) -> list:
    len_diff = len(old_folder_path) - len(new_folder_path)
    old_folder_prefix, new_folder_prefix = "", ""
    if(len_diff > 0):
        new_folder_prefix = " "*len_diff
    else:
        old_folder_prefix = " "*(-len_diff)
    files_abs_old, files_abs_new = set(d1.keys()), set(d2.keys())
    hashes1, hashes2 = list(d1.values()), list(d2.values())
    hashes = set(hashes1 + hashes2)
    res = []
    for hash_i in hashes:
        item_fits = 0
        S = f"* Hash \"{hash_i}\" have files: \n"
        for file_i in files_abs_new:
            if(d2[file_i] == hash_i):
                item_fits += 1
                S += f"\t- {new_folder_prefix}{file_i}\n"
        for file_i in files_abs_old:
            if(d1[file_i] == hash_i):
                item_fits += 1
                S += f"\t- {old_folder_prefix}{file_i}\n"
        if(item_fits >= 2):
            res.append(S)
    return res

def main_diff(args: list):
    argc = len(args)
    mode_explain_str = "\t- n: show New files (does not need the hash)\n\t- c: show Changed files\n\t- r: show Removed files (does not need the hash)\n\t- m: show Moved (renamed) files\n\t- i: show Identical files"
    if(argc != 3):
        pout("This module will show all changes in directories.\n")
        pout("Syntax error. Expected: \"python folder_work.py diff {n|c|r|m|i} {folder_old} {folder_new}\", where: ")
        pout(mode_explain_str)
        exit()
    mode = args[0]
    folder_old = args[1]
    folder_new = args[2]
    err_out = []
    folder_old_abs = os.path.abspath(folder_old)
    folder_new_abs = os.path.abspath(folder_new)
    if(is_folder(folder_old_abs) == False):
        pout(f"\"{folder_old_abs}\" is not folder. ")
        exit()
    if(is_folder(folder_new_abs) == False):
        pout(f"\"{folder_new_abs}\" is not folder. ")
        exit()
    for letter_i in mode:
        if(letter_i not in "ncrmi"):
            pout(f"Cannot understand \"{letter_i}\" in \"{mode}\". Expected: n, c, r, m, i or their combination: ")
            pout(mode_explain_str)
            exit()
        if(mode.count(letter_i) > 1):
            pout(f"\"{letter_i}\" cannot repeat. ")
            exit()
    if(len(mode) == 2 and mode[0] in "nr" and mode[1] in "nr"):
        HASH_NOT_NEEDED = True
    else:
        HASH_NOT_NEEDED = False
    d1, d2, dr1, dr2 = {}, {}, {}, {}
    files_abs_old = sorted(get_files_list(folder_old_abs))
    files_abs_new = sorted(get_files_list(folder_new_abs))
    gi, N = 0, len(files_abs_old)+len(files_abs_new)
    for file_i in files_abs_old:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        if(HASH_NOT_NEEDED == True):
            file_i_hash = ""
        else:
            file_i_hash = get_hash_file(file_i)
            pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        d1[file_i] = file_i_hash
        file_i_rel = rel_path(file_i, folder_old_abs)
        dr1[file_i_rel] = file_i_hash
    for file_i in files_abs_new:
        gi+=1
        if(is_file(file_i) == False):
            err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
            continue
        if(HASH_NOT_NEEDED == True):
            file_i_hash = ""
        else:
            file_i_hash = get_hash_file(file_i)
            pout(f"({gi}/{N}) Calculated hash of \"{file_i}\": {file_i_hash}")
        d2[file_i] = file_i_hash
        file_i_rel = rel_path(file_i, folder_new_abs)
        dr2[file_i_rel] = file_i_hash

    pout("\nHashes calculated. Calculating differences. \n")

    for mode_i in mode:
        if(mode_i == "n"):
            new_files_rel = diff_new_files(dr1, dr2)
            pout("\n====================\n* New files: ")
            if(len(new_files_rel) > 0):
                for file_i in new_files_rel:
                    pout(f"\t{os.path.join(folder_new_abs, file_i)}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "c"):
            changed_files_rel = diff_changes_files(dr1, dr2)
            pout("\n====================\n* Changed files: ")
            if(len(changed_files_rel) > 0):
                for file_i in changed_files_rel:
                    pout(f"\t{file_i}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "r"):
            removed_files_rel = diff_removed_files(dr1, dr2)
            pout("\n====================\n* Removed files: ")
            if(len(removed_files_rel) > 0):
                for file_i in removed_files_rel:
                    pout(f"\t{os.path.join(folder_old_abs, file_i)}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "m"):
            moved_files_rel = diff_moved_files(dr1, dr2, folder_old_abs, folder_new_abs)
            pout("\n====================\n* Moved (renamed) files: ")
            if(len(moved_files_rel) > 0):
                for file_i in moved_files_rel:
                    pout(f"{file_i}")
            else:
                pout("\tNo such files. ")
        elif(mode_i == "i"):
            identical_files = diff_identical_files(d1, d2, folder_old_abs, folder_new_abs)
            pout("\n====================\n* Identical files: ")
            if(len(identical_files) > 0):
                for file_i in identical_files:
                    pout(f"{file_i}")
            else:
                pout("\tNo such files. ")
        else:
            pout(f"Failed successfully (\"{mode_i}\").")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")
