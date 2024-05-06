# -*- coding: utf-8 -*-

import os
import sys
import argparse
import re
import subprocess
import time

from diwork_ways import *
from diwork_sup import *

# TODO: check how wort with sshpass

def process_src_dest_or_exit(folder1: str, folder2: str) -> "tuple(sorce, dest, user, host, path, if_src_remote)":
    req = f"(.+)@(.+):(.+)"
    re_res1 = re.match(req, folder1)
    re_res2 = re.match(req, folder2)
    if(   (re_res1 == None and re_res2 == None) or (re_res1 != None and re_res2 != None)   ):
        pout(f"Only one of \"{folder1}\" and \"{folder2}\" must be sshd (\"user@IP:path/to/dir\")")
        exit()
    
    if(re_res1 == None):
        if(is_folder(folder1) == False):
            pout(f"\"{folder1}\" must be folder. ")
            exit()
        else:
            re_res1 = os.path.abspath(folder1)
    else:
        pout(f"Will be connect to {re_res1[1]} on remote host {re_res1[2]} and use directory: {re_res1[3]}")
        res_user, res_host, res_path = re_res1[1], re_res1[2], re_res1[3]
        if_src = True

    if(re_res2 == None):
        if(is_folder(folder2) == False):
            pout(f"\"{folder2}\" must be folder. ")
            exit()
        else:
            re_res2 = os.path.abspath(folder2)
    else:
        pout(f"Will be connect to {re_res2[1]} on remote host {re_res2[2]} and use directory: {re_res2[3]}")
        res_user, res_host, res_path = re_res2[1], re_res2[2], re_res2[3]
        if_src = False

    return (re_res1, re_res2, res_user, res_host, res_path, if_src)
    

def run_remote_host_command(command: str, user: str, host: str, port: int, pswd:str=None) -> tuple:
    ''' return tuple of (stdout, stderr, returncode) '''
    if(pswd == None):
        com = f"ssh -p {port} {user}@{host} \"{command}\""
        DEBUG = True
    else:
        com = f"sshpass -p \"{pswd}\" ssh -p {port} {user}@{host} \"{command}\""
        com_out = f"sshpass -p *** ssh -p {port} {user}@{host} \"{command}\""
        DEBUG = False
        pout(f"> {com_out}")
    exe_res = exe(com, debug=DEBUG)
    #print(exe_res)
    #exit()
    return exe_res

def get_all_files_from_remote_host(user: str, host: str, port: int, path: str, pswd:str=None) -> list:
    com = f"find {path} -type f"
    #print(exe_res)
    exe_res = run_remote_host_command(com, user, host, port, pswd)
    if(exe_res[1] != ""):
        pout(f"=====ERROR=====\n{exe_res[1]}\n===============")
        exit()
    else:
        files = exe_res[0].split("\n")
    #print(files)
    return files[:len(files)-1] # last element is empty string

def do_copy(if_src_remote: bool, src: str, dest: str, port: int, pswd:str=None):
    if(pswd != None):
        com_prefix = f"sshpass -p \"{pswd}\" "
        com_prefix_out = f"sshpass -p *** "
        DEBUG = False
    else:
        com_prefix = ""
        DEBUG = True
    
    com = f"scp -P {port} \"{src}\" \"{dest}\""
    while(True):
        exe_res = exe(com_prefix + com, debug=DEBUG, std_out_fd=None, std_err_fd=subprocess.PIPE)
        #print(exe_res)
        if(exe_res[1] != ""):
            pout(f"Error: {exe_res[1]}\n Trying again...\n")
            time.sleep(3)
        else:
            break

    if(DEBUG == False):
        pout(f"> {com_prefix_out + com}")

def delete_all_if_dir_not_empty_ssh(dir_path: str, user: str, host: str, port: int = 22, pswd:str=None):
    exe_res = run_remote_host_command(f"ls \"{dir_path}\"", user, host, port, pswd)
    if(exe_res[1] != ""):
        pout(f"=====ERROR=====\n{exe_res[1]}\n===============")
        exit()
    if(exe_res[0] != ""):
        ssh_folder_name = f"{user}@{host}:{dir_path}"
        #rm_command = f"rm -rf {path}"
        #rm_command = f"find {path} -type f -delete"
        rm_command = f"find \"{dir_path}\" ! -wholename \"{dir_path}\" -delete"

        pout(f"Folder \"{ssh_folder_name}\" is not empty. ")
        pout(f"===============\n\t All files in \"{ssh_folder_name}\" will be removed before continue. \n\tOn server \"{host}\" command \"\"\"\n> {rm_command}\n\"\"\" will be executed. \n===============")
        pout("Continue? Type \"yes\" in capital letter to continue or \"no\" to exit. \n> ", endl=False)
        
        while(True):
            user_in = input().strip()
            if(user_in != "YES"):
                pout("Type \"YES\" in capital letter to remove all content of directory \"{dir_path}\" or press CTRL+C or type \"no\" to exit. ")
            if(user_in.lower() == "no"):
               pout("Exitting...")
               exit()
            if(user_in == "YES"):
                break
            pout("> ", endl=False)

        exe_res = run_remote_host_command(rm_command, user, host, port, pswd)
        if(exe_res[1] != ""):
            pout(f"=====ERROR=====\n{exe_res[1]}\n===============")
            exit()
        
        exe_res = run_remote_host_command(f"ls \"{dir_path}\"", user, host, port, pswd)
        if(exe_res[1] != ""):
            pout(f"=====ERROR=====\n{exe_res[1]}\n===============")
            exit()
        if(exe_res[0] == ""):
            pout(f"All files from folder \"{ssh_folder_name}\" removed. This folder is empty now.")
        else:
            pout(f"Cannot clean folder \"{ssh_folder_name}\"! Exiting ")
            exit()



def main_sshclone(args: list):

    parser = argparse.ArgumentParser(prog = "diwork sshclone",
        description="Clone directory by scp. Set up ssh-agent. And run \"ssh-add\" or use flag --askpass (sshpass must be installed). ")
    parser.add_argument("source", type=str, nargs=1,
                       help="Path to directory or user@IP/DOMEN:path/to/dir")
    parser.add_argument("destination", type=str, nargs=1,
                       help="Path to directory or user@IP/DOMEN:path/to/dir")
    parser.add_argument("--askpass", default=False, action='store_true',
                       help="If ssh do not use key. Then it will ask password. Package \"sshpass\" must be installed. ")
    parser.add_argument("--port", type=int, default=22, 
                       help="port of sshd. ")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)

    folder1 = args.source[0]
    folder2 = args.destination[0]
    IF_ASKPASS = args.askpass
    PORT = args.port


    folder1, folder2, user, host, path, if_src_remote = process_src_dest_or_exit(folder1, folder2)

    if(IF_ASKPASS == True):
        from getpass import getpass
        while(True):
            PSWD1 = getpass(f"Input password of {user}: ")
            PSWD2 = getpass(f"Input again password of {user}: ")
            if(PSWD1 != PSWD2):
                pout("Passwords do not match. Try again.")
            else:
                break
        PSWD = PSWD1
        
    else:
        PSWD = None

    exe_res = run_remote_host_command(f"[ -d \"{path}\" ] && echo -n 1", user, host, PORT, PSWD)
    if(exe_res[1] != ""):
        pout(f"=====ERROR=====\n{exe_res[1]}\n===============")
        exit()
    if(exe_res[0] != "1"):
        pout(f"Directory \"{user}@{host}:{path}\" does not exists. ")
        exit()

    if(if_src_remote == True):
        cpfiles = get_all_files_from_remote_host(user, host, PORT, path, PSWD)
    else:
        cpfiles = get_files_list(folder1)

    if(if_src_remote == False):
        delete_all_if_dir_not_empty_ssh(path, user, host, PORT, PSWD)
        dirs = get_dirs_needed_for_files(cpfiles)
        for dir_i in dirs:
            dir_i_rel = rel_path(dir_i, folder1)
            dir_i_2 = os.path.join(path, dir_i_rel)
            com = f"mkdir -p \"{dir_i_2}\""
            exe_res = run_remote_host_command(com, user, host, PORT, PSWD)
            if(exe_res[1] != ""):
                pout(f"=====ERROR=====\n{exe_res[1]}\n===============")
                exit()


    if(if_src_remote == True):
        #pout(f"Folder \"{folder2}\" is not empty. ")
        #exit()
        delete_all_if_dir_not_empty(folder2)

        dirs = get_dirs_needed_for_files(cpfiles)
        for dir_i in dirs:
            dir_i_rel = rel_path(dir_i, path)
            dir_i_2 = os.path.join(folder2, dir_i_rel)
            exe_out = exe(f"mkdir -p \"{dir_i_2}\"")
            if(exe_out[1] != ""):
                pout(f"ERROR: {exe_out[1]}")
                exit()

    if(if_src_remote == True):
        gi, N = 1, len(cpfiles)
        for file_i in cpfiles:
            file_i_rel = rel_path(file_i, path)
            src_file, dest_file = f"{user}@{host}:{file_i}",  os.path.join(folder2, file_i_rel)
            pout(f"({gi}/{N}) Coping file \"{src_file}\" to \"{dest_file}\"...")
            do_copy(if_src_remote, src_file,dest_file, PORT, PSWD)
            gi-=-1
    else:
        gi, N = 1, len(cpfiles)
        for file_i in cpfiles:
            file_i_rel = rel_path(file_i, folder1)
            dest_file = f"{user}@{host}:{os.path.join(path, file_i_rel)}"
            pout(f"({gi}/{N}) Coping file \"{file_i}\" to \"{dest_file}\"...")
            do_copy(if_src_remote, file_i, dest_file, PORT, PSWD)
            gi-=-1





    pout("\n=============== Done! ===============")
