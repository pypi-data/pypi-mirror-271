# -*- coding: utf-8 -*-

import os
import sys
import argparse 

from diwork_ways import *

class REP_OBJ():

    def __init__(self):
        self.IN_REP, self.OUT_REP = "{in}", "{out}" # absolute file path
        self.IN_REP_REL, self.OUT_REP_REL = "{in_rel}", "{out_rel}" # relative path
        self.IN_REP_FN, self.OUT_REP_FN = "{in_fn}", "{out_fn}" # file name with extension
        self.IN_REP_FNO, self.OUT_REP_FNO = "{in_fno}", "{out_fno}" # file name without extension
        self.IN_REP_FNE, self.OUT_REP_FNE = "{in_fne}", "{out_fne}" # file extension
        self.IN_REP_DIR, self.OUT_REP_DIR = "{in_dir}", "{out_dir}" # directory, where this file
        self.IN_REP_DIR_REL, self.OUT_REP_DIR_REL = "{in_dir_rel}", "{out_dir_rel}" # relative path of directory, where this file
        self.IN_REP_INDEX, self.OUT_REP_INDEX = "{in_i}", "{out_i}" # index, like 1,2,3...


def replace_REP_with_needed(command: str, REPS: list, REP_OBJ: object, file_abs_path: str, folder: str, index) -> str:
    file_rel_path = rel_path(file_abs_path, folder)
    file_fn = os.path.basename(file_abs_path)
    file_fno, file_fne = os.path.splitext(file_fn)
    if(file_fne != ""):
        file_fne = file_fne[1:]
    file_dir = os.path.dirname(file_abs_path)
    file_dir_rel = rel_path(file_dir, folder)
    for rep_i in REPS:
        if(rep_i in [REP_OBJ.IN_REP, REP_OBJ.OUT_REP]):
            command = command.replace(rep_i, file_abs_path)
        elif(rep_i in [REP_OBJ.IN_REP_REL, REP_OBJ.OUT_REP_REL]):
            command = command.replace(rep_i, file_rel_path)
        elif(rep_i in [REP_OBJ.IN_REP_FN, REP_OBJ.OUT_REP_FN]):
            command = command.replace(rep_i, file_fn)
        elif(rep_i in [REP_OBJ.IN_REP_FNO, REP_OBJ.OUT_REP_FNO]):
            command = command.replace(rep_i, file_fno)
        elif(rep_i in [REP_OBJ.IN_REP_FNE, REP_OBJ.OUT_REP_FNE]):
            command = command.replace(rep_i, file_fne)
        elif(rep_i in [REP_OBJ.IN_REP_DIR, REP_OBJ.OUT_REP_DIR]):
            command = command.replace(rep_i, file_dir)
        elif(rep_i in [REP_OBJ.IN_REP_DIR_REL, REP_OBJ.OUT_REP_DIR_REL]):
            command = command.replace(rep_i, file_dir_rel)
        elif(rep_i in [REP_OBJ.IN_REP_INDEX, REP_OBJ.OUT_REP_INDEX]):
            command = command.replace(rep_i, str(index))
        else:
            pout(f"replace_REP_with_needed ({rep_i}): Failed successfully")
            exit()
    return command

def help4command(repo) -> str:
    res = ""
    res += "Expected: \"python diwork.py exec {folder_in} {folder_out} {command}\", where: \n"
    res += "\t{command} like this \"convert \\\"{in}\\\" \\\"{out}\\\"\", where: \n"
    res += f"\t\t{repo.IN_REP}" + " each file from {folder_in} \n"
    res += f"\t\t{repo.OUT_REP}" + " each file from {folder_out} \n"
    res += "\t{folder_out} must be empty string (\"\") if do not used\n"
    res += "\n\tFor exampe, convert all jpg-pictures from \"path/to/jpg/image/folder\" to png-image:\n"
    res += "\t> python diwork.py exec \"path/to/jpg/image/folder\" \"path/to/png/image/folder\" \"convert \\\"{in}\\\" \\\"{out}.png\\\"\"\n"
    res += "\tTags for use:\n"
    res += f"\t\t{repo.IN_REP}" + ": full path of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP}" + ": full path of files from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_REL}" + ": relative path of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_REL}" + ": relative path of files from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_FN}" + ": name of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_FN}" + ": name of files from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_FNO}" + ": name without extension of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_FNO}" + ": name without extension of files from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_FNE}" + ": files extension (without dot) from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_FNE}" + ": files extension (without dot) from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_DIR}" + ": directory of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_DIR}" + ": directory of files from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_DIR_REL}" + ": relative path of directory of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_DIR_REL}" + ": relative path of directory of files from {folder_out}\n"
    res += f"\t\t{repo.IN_REP_INDEX}" + ": index of files from {folder_in}\n"
    res += f"\t\t{repo.OUT_REP_INDEX}" + ": index of files from {folder_out}\n"
    res += "Example 1: \"" + repo.IN_REP + "\" and \"" + repo.IN_REP_DIR +"/" + repo.IN_REP_FNO + "." + repo.IN_REP_FNE + "\" the same text.\n"
    res += "Example 2: \"" + repo.OUT_REP_FN + "\" and \"" + repo.OUT_REP_FNO + "." + repo.OUT_REP_FNE +"\" the same text.\n"
    return res

def main_exec(args: list):
    repo = REP_OBJ()
    REPS_IN = [repo.IN_REP, repo.IN_REP_REL, repo.IN_REP_FN, repo.IN_REP_FNO, repo.IN_REP_FNE, repo.IN_REP_DIR, repo.IN_REP_DIR_REL, repo.IN_REP_INDEX]
    REPS_OUT = [repo.OUT_REP, repo.OUT_REP_REL, repo.OUT_REP_FN, repo.OUT_REP_FNO, repo.OUT_REP_FNE, repo.OUT_REP_DIR, repo.OUT_REP_DIR_REL, repo.OUT_REP_INDEX]

    parser = argparse.ArgumentParser(prog = "diwork exec",
        description="execute by certain rules. This module will help you execute a command with all files in certain directories.\n")
    parser.add_argument("folder_in", type=str, nargs=1,
                       help="Path to \"input\" directory")
    parser.add_argument("folder_out", type=str, nargs=1,
                       help="Path to \"output\" directory")
    parser.add_argument("command", type=str, nargs=1,
                       help=help4command(repo))
    parser.add_argument("--no_exec", default=False, action='store_true',
                       help="If True, the commands will not be executed, but only displayed. Default False")
    parser.add_argument("--exec_help", default=False, action='store_true',
                       help="If help looks terrible, then set this flag, like that: \"> python diwork.py exec "" "" "" --exec_help\"")
    parser = common_init_parser(parser)
    args = parser.parse_args(args)
    common_init_parse(args)


    if(args.exec_help == True):
        pout(help4command(repo))
        exit()
    folder_in = args.folder_in[0]
    folder_out = args.folder_out[0]
    command = args.command[0]
    NO_EXEC = args.no_exec

    err_out = []
    if(is_folder(folder_in) == False):
        pout(f"\"{folder_in}\" is not folder. ")
        exit()
    folder_in_abs = os.path.abspath(folder_in)
    if(folder_out != "" and is_folder(folder_out) == False):
        pout(f"\"{folder_out}\" is not folder. ")
        exit()
    if(folder_out == ""):
        #if OUT_REP in command:
        #    pout(f"{OUT_REP} in {command} finded, but folder_out is empty string. Exitting")
        #    exit()
        pass
    else:
        folder_out_abs = os.path.abspath(folder_out)

    if(folder_out != "" ):
        if(NO_EXEC == False):
            delete_all_if_dir_not_empty(folder_out_abs)

    if(NO_EXEC == True):
        print("===============GENERATED COMMANDS:===============")

    if(folder_out != ""):
        dirs_abs_in = list(set(getDirsList(folder_in_abs)))
        dirs_abs_in = sorted(dirs_abs_in)
        for dir_in_i in dirs_abs_in:
            dir_in_i_rel = rel_path(dir_in_i, folder_in_abs)
            dir_out_i_abs = os.path.join(folder_out_abs, dir_in_i_rel)
            cmd2exec = f"mkdir -p \"{dir_out_i_abs}\""
            if(NO_EXEC == False):
                # exe_out = exe(cmd2exec)
                # if(exe_out[1] != ""):
                #     pout(f"ERROR: {exe_out[1]}")
                #     exit()
                mkdir(dir_out_i_abs)
            else:
                pout(cmd2exec)
                

    files_abs_in = get_files_list(folder_in_abs)
    files_abs_in = sorted(files_abs_in)
    gi, N = 0, len(files_abs_in)
    for file_in_i in files_abs_in:
        gi+=1
        if(is_file(file_in_i) == False):
            err_out.append(f"\"{file_in_i}\" is not file or does not exists, it will be skipped. ")
            continue
        
        #command_i = command.replace(IN_REP, file_in_i)
        command_i = replace_REP_with_needed(command, REPS_IN, repo, file_in_i, folder_in_abs, gi)
        if(folder_out != ""):
            file_i_rel = rel_path(file_in_i, folder_in_abs)
            file_out_i = os.path.join(folder_out_abs, file_i_rel)
            #command_i = command_i.replace(OUT_REP, file_out_i)
            command_i = replace_REP_with_needed(command_i, REPS_OUT, repo, file_out_i, folder_out_abs, gi)
        if(NO_EXEC == False):
            pout(f"({gi}/{N}) Executing... ")
            #print(command_i)
            exe_out = exe(command_i)
            if(exe_out[1] != ""):
                err_out.append(f"ERROR: {exe_out[1]}")
                continue
        else:
            pout(command_i)

    os.sync()
    #exe("sync")

    if(len(err_out) != 0):
        pout(f"\n===============\nSome troubles happened:")
        for err_i in err_out:
            pout(f"\t{err_i}")
        pout(f"===============")

    pout("=============== Done! ===============")
