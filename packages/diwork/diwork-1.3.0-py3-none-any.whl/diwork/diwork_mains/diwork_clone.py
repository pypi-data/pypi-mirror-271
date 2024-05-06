# -*- coding: utf-8 -*-

import os
import sys
import argparse 
import shutil

from diwork_ways import *

def define_clone_command() -> "str":
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        return "cp"
    elif sys.platform == "win32":  # In windows cp == copy
        return "copy"
    else:
        pout("(define_clone_command) Failed successfully. ")

def cp(src: str, dest: str, copy_mode: int = 0) -> None:
    if(copy_mode == 0):
        shutil.copy(src, dest)
    elif(copy_mode == 1):
        COPY_COMMAND = define_clone_command()
        exe_out = exe(f"{COPY_COMMAND} \"{src}\" \"{dest}\"")
        if(exe_out[1] != ""):
            pout(f"ERROR: {exe_out[1]}")
            exit()
    else:
        pout("(cp) Failed successfully. ")

def main_clone(args: list):
    parser = argparse.ArgumentParser(prog = "diwork clone",
        description="This module will clone all the contents of {folder_src} to {folder_dest}. As a result, {folder_src} and {folder_dest} will be completely identical.")
    parser.add_argument("folder_src", type=str, nargs=1,
                       help="Path to source directory")
    parser.add_argument("folder_dest", type=str, nargs=1,
                       help="Path to destination directory")
    # parser.add_argument("--symlink_mode", type=int, choices=[0,1,2], default=2, required=False,
    #                    help="What to do with links: 0 - ignor, 1 - consider link content, 2 - use the file where the link refers to. Default 2.")
    parser.add_argument("--copy_mode", type=int, choices=[0,1], default=0, required=False,
                       help="How to copy files: 0 - python shutil, 1 - system cp (copy). Default 0.")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)
    
    folder1 = args.folder_src[0]
    folder2 = args.folder_dest[0]
    err_out = []
    folder1_abs = os.path.abspath(folder1)
    folder2_abs = os.path.abspath(folder2)
    if(is_folder(folder1_abs) == False):
        pout(f"\"{folder1_abs}\" is not folder. ")
        exit()
    if(is_folder(folder2_abs) == False):
        pout(f"\"{folder2_abs}\" is not folder. ")
        exit()
    
    if(folder1_abs in folder2_abs):
        pout(f"Directory \"{folder1_abs}\" contains directory \"{folder2_abs}\". Exiting...")
        input("Enter to continue...")
    if(folder2_abs in folder1_abs):
        pout(f"Directory \"{folder2_abs}\" contains directory \"{folder1_abs}\". Exiting...")
        input("Enter to continue...")
    symlink_mode = args.symlink_mode
    copy_mode = args.copy_mode
    
    delete_all_if_dir_not_empty(folder2_abs)
    pout("Clonning...")

    dirs_abs_1 = getDirsList(folder1_abs)
    dirs_abs_1 = sorted(dirs_abs_1)
    for dir_i_1 in dirs_abs_1:
        dir_i_rel = rel_path(dir_i_1, folder1_abs)
        dir_i_2 = os.path.join(folder2_abs, dir_i_rel)
        mkdir(dir_i_2)
        #exe_out = exe(f"mkdir -p \"{dir_i_2}\"")
        #if(exe_out[1] != ""):
        #    pout(f"ERROR: {exe_out[1]}")
        #    exit()

    files_abs_1 = get_files_list(folder1_abs)
    files_abs_1 = sorted(files_abs_1)
    gi, N = 0, len(files_abs_1)
    for file_i_1 in files_abs_1:
        gi+=1
        if(os.path.islink(file_i_1) == False and is_file(file_i_1) == False):
            err_out.append(f"\"{file_i_1}\" is not file or does not exists, it will be skipped. ")
            continue

        file_i_rel = rel_path(file_i_1, folder1_abs)
        file_i_2 = os.path.join(folder2_abs, file_i_rel)
        if(os.path.islink(file_i_1) == True):
            if(symlink_mode == 0):
                pout(f"({gi}/{N}) \"{file_i_1}\" is symlink and symlink_mode={symlink_mode}. So it will be skipped. ")
                continue
            elif(symlink_mode == 1):
                linkto = os.readlink(file_i_1)
                os.symlink(linkto, file_i_2)
            elif(symlink_mode == 2):
                linkto = get_link_unwinding(file_i_1)
                if(linkto == None):
                    pout(f"({gi}/{N}) \"{file_i_1}\" refers to nonexistent file. So it will be skipped. ")
                    err_out.append(f"\"{file_i_1}\" refers to nonexistent file, it will be skipped. ")
                    continue
                pout(f"({gi}/{N}) Copying \"{file_i_rel}\" (\"{file_i_1}\"=\"{linkto}\" -> \"{file_i_2}\")... ")
                cp(linkto, file_i_2, copy_mode)
            else:
                pout(f"Failed successfully. symlink_mode={symlink_mode}, cannot understand it. ")
                exit()
        else:
            pout(f"({gi}/{N}) Copying \"{file_i_rel}\"... ")
            cp(file_i_1, file_i_2, copy_mode)
    if(copy_mode == 0):
        if sys.platform != "win32":
            os.sync()
    elif(copy_mode == 1):
        if sys.platform != "win32":
            exe("sync")
    else:
        pass

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")
