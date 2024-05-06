# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil

from diwork_ways import *

def main_hash(args: list) -> "list of hashes":

    parser = argparse.ArgumentParser(prog = "diwork hash",
        description="Calculate hash of directory(s)")
    parser.add_argument("folders_paths", type=str, nargs="+",
                       help="Paths to directories whose hash will be calculated")
    parser.add_argument("--exclude", type=str, nargs="+", default=None, action="append",
                       help="Do not take these files or directories into consideration when calculating the hash")
    # parser.add_argument("--symlink_mode", type=int, choices=[0,1,2], default=2, required=False,
    #                    help="What to do with links: 0 - ignor, 1 - consider link content, 2 - use the file where the link refers to. Default 2.")
    parser.add_argument("--hierarchy", default=False, action='store_true',
                       help="If True, then the file hierarchy will be considered when calculating the hash. Default False")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    folders = args.folders_paths
    files_exclude = args.exclude
    if(files_exclude != None):
        files_exclude = [shit[0] for shit in files_exclude]
        check_files_exists_or_exit(files_exclude)
    err_out = []
    folders_abs = [os.path.abspath(folder_i) for folder_i in folders]
    for folder_i in folders_abs:
        if(is_folder(folder_i) == False):
            pout(f"No such directory: \"{folder_i}\"")
            exit()
        if(folders_abs.count(folder_i) > 1):
            pout(f"Directory \"{folder_i}\" occurs several ({folders_abs.count(folder_i)}) times. Exiting...")
            exit()
    symlink_mode = args.symlink_mode
    if_hierarchy = args.hierarchy
    if(if_hierarchy == False):
        RES_OUT_PREFIX_HIERARCHY = "not"
    else:
        RES_OUT_PREFIX_HIERARCHY = "with"

    dir_hashes = {}
    ggi, ggN = 0, len(folders_abs)
    for folder_i in folders_abs:
        ggi-=-1
        pout(f"\nCalculating hash of directory \"{folder_i}\":")
        files = get_files_list(folder_i)
        files = sorted(files)
        files = exclude_files(files, files_exclude)
        hashes = []
        gi, files_len = 0, len(files)
        for file_i in files:
            gi+=1
            if(os.path.islink(file_i) == False and is_file(file_i) == False):
                err_out.append(f"\"{file_i}\" is not file or does not exists, it will be skipped. ")
                continue

            if(os.path.islink(file_i) == True):
                if(symlink_mode == 0):
                    pout(f"[{ggi}/{ggN}] ({gi}/{files_len}) \"{file_i}\" is symlink and symlink_mode={symlink_mode}. So it will be skipped. ")
                    continue
                elif(symlink_mode == 1):
                    linkto = os.readlink(file_i)
                    hash_i = get_hash_str(linkto)
                elif(symlink_mode == 2):
                    linkto = get_link_unwinding(file_i)
                    if(linkto == None):
                        pout(f"[{ggi}/{ggN}] ({gi}/{files_len}) \"{file_i}\" refers to nonexistent file. So it will be skipped. ")
                        err_out.append(f"\"{file_i}\" refers to nonexistent file, it will be skipped. ")
                        continue
                    file_i = linkto
                    hash_i = get_hash_file(file_i)
                else:
                    pout(f"Failed successfully. symlink_mode={symlink_mode}, cannot understand it. ")
                    exit()
            else:
                hash_i = get_hash_file(file_i)
            hashes.append(hash_i)
            pout(f"[{ggi}/{ggN}] ({gi}/{files_len}) Hash \"{hash_i}\" have file \"{file_i}\". ")
        hashes = sorted(hashes)

        # IF CHANGE, then change make_archive_one_folder in diwork_archive.py (its legacy_version)
        hash_files = get_hash_of_hashes(hashes)
        if(if_hierarchy == True):
            files_rel = [rel_path(fileh_i, folder_i) for fileh_i in files]
            dirs = getDirsList(folder_i)
            dirs_rel = [rel_path(dirh_i, folder_i) for dirh_i in dirs]
            hash_hierarchy = get_hash_of_hashes(  sorted(files_rel+dirs_rel) )
            hash_files = get_hash_str(hash_files + hash_hierarchy)

        pout(f"\n\nHash ({RES_OUT_PREFIX_HIERARCHY} considering the files hierarchy) of the directory \"{folder_i}\": \n==============================\n{hash_files}\n==============================\n")
        dir_hashes[folder_i] = hash_files


    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    col_1 = []
    col_2 = []
    for el in dir_hashes:
        col_1.append(dir_hashes[el])
        col_2.append(el)
    pout(f"\n\nHashes of directories ({RES_OUT_PREFIX_HIERARCHY} considering the files hierarchy): ")
    for i in range(len(col_1)):
        print(f"{col_1[i]} | {col_2[i]}")
    pout("\n=============== Done! ===============")

    return list(dir_hashes.values())
