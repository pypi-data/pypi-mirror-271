# -*- coding: utf-8 -*-

import os
import sys
import argparse

import json
import zipfile

from diwork_ways import *

def get_folders_one_deep(dir_path: str) -> list:
    # return [x[0] for x in os.walk(dir_path)]
    return [ f.path for f in os.scandir(dir_path) if f.is_dir() ]



def make_archive_one_folder(folder_path: str, path_to_zip: str, cur_iter: str = None) -> "(errors: list,)":
    """
    json:
    hashes: {file: hashs},
    sizes: {file: sizes},
    folder_size: int,
    folder_hash: hash,
    date: str(DD.MM.YY HH:MM:SS),
    legacy_version: int
    hash_mode: int
    """
    legacy_version = 1
    d = {"hashes":{}, "sizes": {}}

    errors = []
    folder_path_name = os.path.basename(folder_path)
    # folder_path_name = "content"
    files = sorted(get_files_list(folder_path))
    files = [os.path.abspath(file_i) for file_i in files]
    files_rel = [rel_path(file_i, folder_path) for file_i in files]

    with zipfile.ZipFile(path_to_zip, mode="w") as zfd:
        gi, gN = 0, len(files)
        for file_i, file_rel_i in zip(files, files_rel):
            gi-=-1
            hash_i = get_hash_file(file_i)
            size_i = os.path.getsize(file_i)
            d["hashes"][file_i] = hash_i
            d["sizes"][file_i] = size_i
            if(cur_iter != None):
                pout(f"{cur_iter} ({gi}/{gN}) Hash \"{hash_i}\" have file \"{file_i}\" ({get_nice_size(size_i)}). ")
            else:
                pout(f"({gi}/{gN}) Hash \"{hash_i}\" have file \"{file_i}\" ({get_nice_size(size_i)}). ")
            zfd.write(file_i, f"{folder_path_name}/{file_rel_i}")
        d["folder_hash"] = hash_files = get_hash_of_hashes(sorted(d["hashes"].values()))
        d["folder_size"] = sum(d["sizes"].values())
        d["date"] = get_time_str()
        d["legacy_version"] = legacy_version # if calculating hash will be changed or changed other things, this needed change too (increment)
        zfd.writestr("archive_info.json", json.dumps(d).encode("utf-8"))
    
    return (errors, )  # TODO: errors

def process_if_zip_exists(zip_path: str) -> int:
    """ 0=override,    1=skip """
    while(True):
        pout(f"File \"{zip_path}\" already exists. Override this?")
        pout("Type \"yes\" in capital letter to override or \"no\" to skip. \n> ", endl=False)
        user_in = input()
        if(user_in == "YES"):
            return 0
        if(user_in.lower().strip() == "no"):
            return 1
        pout(f"Wrong! Try again...")

def main_archive(args: list):

    parser = argparse.ArgumentParser(prog = "diwork archive",
        description="Makes archives from folders in the current directory. Make from each folder archive, where the folder and hash consist, and other data. ")
    parser.add_argument("folder_in", type=str, nargs=1,
                       help="Path to the directory where the folders from which you want to make an archive are located. ")
    parser.add_argument("folder_out", type=str, nargs=1,
                       help="Path to the directory where the archive will be placed. ")
    parser.add_argument("--yes", default=False, action='store_true',
                       help="No interractive. Answer \"yes\" always. ")
    parser.add_argument("--one", default=False, action='store_true',
                       help="Archive only one folder {folder_in}. Then {folder_in} path to the archived folder, not to directory of folders. ")

    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    IF_YES = args.yes
    IF_ONE = args.one

    root_dir = args.folder_in[0]
    if(is_folder(root_dir) == False):
        pout(f"\"{root_dir}\" is not directory. ")
        exit()
    root_dir = os.path.abspath(root_dir)

    out_dir = args.folder_out[0]
    if(is_folder(out_dir) == False):
        pout(f"\"{out_dir}\" is not directory. ")
        exit()
    out_dir = os.path.abspath(out_dir)

    err_out = []
    
    if(IF_ONE == False):
        folders = get_folders_one_deep(root_dir)
    else:
        folders = [root_dir]
    if(len(folders) == 0):
        pout(f"\"{folders}\" is empty. ")
        exit()
    folders = sorted([os.path.abspath(folder_i) for folder_i in folders])
    
    gi, gN = 0, len(folders)
    for folder_i in folders:
        gi-=-1
        if(IF_ONE == False):
            zip_path = os.path.join(out_dir, rel_path(folder_i, root_dir) + ".zip")
        else:
            zip_path = os.path.join(out_dir, os.path.basename(folder_i) + ".zip")
        pout(f"\t\t ({gi}/{gN}) Archiving folder \"{folder_i}\" to \"{zip_path}\"... ")
        if(is_exists(zip_path) == True):
            if(IF_YES == False):
                action = process_if_zip_exists(zip_path)
            else:
                pout(f"File \"{zip_path}\" already exists. It will be overridden! ")
                action = 0
            if(action == 1):
                pout("Skipping folder \"{folder_i}\". ")
                continue
            elif(action == 0):
                pout("File \"{zip_path}\" will be overridden. ")
            else:
                pout(f"Failed successfully. Unknown action={action}")
                exit()

        errors = make_archive_one_folder(folder_i, zip_path, f"({gi}/{gN})")[0]
        if(len(errors) > 0):
            err_out.append(f"\t *Error with folder \"{folder_i}\" BEGIN ")
            err_out += errors
            err_out.append(f"\t *Error with folder \"{folder_i}\"   END ")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")
    
    pout("\n=============== Done! ===============")
