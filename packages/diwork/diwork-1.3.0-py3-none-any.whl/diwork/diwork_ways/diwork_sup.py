# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import hashlib
import datetime
import shutil
from threading import Thread


class Global():
    version = None
    outfile = None
    symlink_mode = None


class ThreadWithReturnValue(Thread):

    def __init__(self, index: int, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._index = index
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args,
                                        **self._kwargs)

    def get_index(self):
        return self._index

    def join(self, *args):
        Thread.join(self, *args)
        return self._return


def get_files_list(dirPath: str) -> list:
    return [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in files]


def getDirsList(dirPath: str) -> list:
    dirs = [os.path.join(path, name) for path, subdirs, files in os.walk(dirPath) for name in subdirs]
    return list(set(dirs))


# return False, if folder_path not exists or folder_path is not folder
def is_folder(folder_path: str) -> bool:
    return os.path.isdir(folder_path)


# return False, if file_path not exists or file_path is not file
def is_file(file_path: str) -> bool:
    return os.path.isfile(file_path)


# return False, if file_path not exists
def is_exists(file_path: str) -> bool:
    return os.path.exists(file_path)


def check_files_exists_or_exit(files: list) -> None:
    F = False
    for file_i in files:
        if(is_exists(file_i) == False):
            pout(f"File \"{file_i}\" does not exists. ")
            F = True
    if(F == True):
        exit()


def is_folder_empty(folder_path: str) -> bool:
    if(len(os.listdir(folder_path)) == 0):
        return True
    else:
        return False


def rel_path(file_path: str, folder_path: str) -> str:
    return os.path.relpath(file_path, folder_path)


def rm_folder_content(folder_path: str, root_dir_too: bool = False, does_not_exists_is_ok = False):
    """Удаляет всё содержимое папки. Саму папку не трогает, если root_dir_too == False"""
    if(does_not_exists_is_ok == True and is_folder(folder_path) == False):
        return
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file_i in files:
            os.remove(os.path.join(root, file_i))
        for dir in dirs:
            os.rmdir(os.path.join(root, dir))
    if(root_dir_too == True):
        os.rmdir(folder_path)


def pout(msg: str, endl = True):
    if(endl == False):
        pout_low(msg)
    else:
        pout_low(msg + "\n")


def pout_low(msg: str):
    print(msg, end="")
    if(Global.outfile != None):
        with open(Global.outfile, "a", encoding="utf-8") as fd:
            fd.write(msg)
            fd.flush()


def write2File_str(fileName : str, s : str) -> None:
    with open(fileName, 'w', encoding="utf-8") as temp:
        temp.write(s)
        temp.flush()


def mkdir(path: str, p: bool = True):
    os.makedirs(path, exist_ok=True)


def get_link_unwinding(link_path: str) -> str or None:
    """Вернёт конечный файл, на который (рекурсивно) ссылаются сылки. """
    if(os.path.exists(link_path) == False):
        return None
    elif(os.path.islink(link_path) == False):
        return link_path
    else:
        linkto = os.readlink(link_path)
        if(os.path.islink(linkto) == False):
            return linkto
        else:
            return get_link_unwinding(linkto)


def get_nice_size(size_bytes: int) -> str:
    if(size_bytes < 1024):
        return f"{size_bytes} B"
    elif(size_bytes < 1024*1024):
        return f"{size_bytes // 1024} KB"
    elif(size_bytes < 1024*1024*1024):
        return f"{size_bytes // (1024*1024)} MB"
    elif(size_bytes < 1024*1024*1024*1024):
        return f"{size_bytes // (1024*1024*1024)} GB"
    else:
        return f"{size_bytes // (1024*1024*1024*1024)} TB"


def get_time_str() -> str:
    # time_str = datetime.datetime.now().strftime("[%y.%m.%d %H:%M:%S.%f]")
    time_str = datetime.datetime.now().strftime("%y.%m.%d %H:%M:%S")
    return time_str


def get_time_file(file_path: str) -> str:
    dt_m = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
    return dt_m.strftime("%d.%m.%Y_%H-%M-%S")


def copy_file(src: str, dest: str) -> bool or None:
    if os.path.islink(src):
        if Global.symlink_mode == 0:
            return None
        elif Global.symlink_mode == 1:
            linkto = os.readlink(src)
            os.symlink(linkto, dest)
            return True
        elif Global.symlink_mode == 2:
            file_path = get_link_unwinding(src)
            if file_path is None:
                return False
        else:
            raise Exception(f"Failed successfully: copy_file with {src}->{dest}")

    shutil.copy(src, dest)
    return True


def get_hash_file(file_path: str) -> str or None:
    if os.path.islink(file_path):
        if Global.symlink_mode == 0:
            return None
        elif Global.symlink_mode == 1:
            return get_hash_str(os.readlink(file_path))
        elif Global.symlink_mode == 2:
            file_path = get_link_unwinding(file_path)
            if file_path is None:
                return None
        else:
            raise Exception(f"Failed successfully: get_hash_file with {file_path}")

    buff_BLOCKSIZE = 65536  # 64 kB
    sha = hashlib.sha256()
    with open(file_path, "rb") as temp:
        file_buffer = temp.read(buff_BLOCKSIZE)
        while len(file_buffer) > 0:
            sha.update(file_buffer)
            file_buffer = temp.read(buff_BLOCKSIZE)
    return sha.hexdigest()


def get_hash_str(s: str):
    return hashlib.sha256( s.encode("utf-8") ).hexdigest()


def get_hash_of_hashes(hashes: list) -> str:

    # IF CHANGE, then change make_archive_one_folder in diwork_archive.py (its legacy_version)

    # from io import StringIO
    # o = StringIO()
    # for hash_i in hashes:
    #     o.write(hash_i)
    # hash_files = get_hash_str(o.getvalue())
    # return hash_files
    hash_files = ""
    li = 0
    for hash_i in hashes:
        hash_files += hash_i
        li-=-1
        if(li == 30):
            hash_files = get_hash_str(hash_files)
            li = 0
    hash_files = get_hash_str(hash_files)
    return hash_files


def exclude_files(src_files: list, exclude_files: list) -> list:
    """
    Убрать из src те файлы, которые есть в exclude_files
    exclude_files - это список файлов или директорий
    Пути к файлам либо все абсолютные, либо все относительные
    """
    if(exclude_files == None):
        return src_files
    res = []

    for file_i in src_files:
        if file_i not in exclude_files:
            F = True
            for ex_file_i in exclude_files:
                if ex_file_i in file_i:
                    F = False
            if(F == True):
                res.append(file_i) 
    return res


def delete_all_if_dir_not_empty(dir_path: str):
    if(is_folder_empty(dir_path) == False):
        pout(f"Folder \"{dir_path}\" is not empty. ")
        pout(f"===============\n\t All files in \"{dir_path}\" will be removed before continue. \n===============")
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
        rm_folder_content(dir_path)
        if(is_folder_empty(dir_path) == True):
            pout(f"All files from folder \"{dir_path}\" removed. This folder is empty now.")
        else:
            pout(f"Cannot clean folder \"{dir_path}\"! Exiting ")
            exit()


def get_dirs_needed_for_files(files: list) -> list:
    dirs = set()
    for file_i in files:
        dir_i = os.path.dirname(file_i)
        dirs.add(dir_i)
    dirs = sorted(list(dirs))
    return dirs


def exe_lowout(command: str, debug: bool = True, std_out_pipe: bool = False, std_err_pipe: bool = False) -> tuple:
    '''
    Аргумент command - команда для выполнения в терминале. Например: "ls -lai ."
    Возвращает кортеж, где элементы:
        0 - строка stdout or None if std_out_pipe == False
        1 - строка stderr or None if std_err_pipe == False
        2 - returncode
    '''
    if(debug):
        pout(f"> {command}")
    
    if(std_out_pipe == True):
        if(std_err_pipe == True):
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            # https://stackoverflow.com/questions/1180606/using-subprocess-popen-for-process-with-large-output
            out = process.stdout.read().decode("utf-8")
            err = process.stderr.read().decode("utf-8")
        else:
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
            out = process.stdout.read().decode("utf-8")
            err = None
    else:
        if(std_err_pipe == True):
            process = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
            out = None
            err = process.stderr.read().decode("utf-8")
        else:
            process = subprocess.Popen(command, shell=True)
            out = None
            err = None
    errcode = process.returncode
    return (out, err, errcode)


def exe(command: str, debug: bool = True, std_out_fd = subprocess.PIPE, std_err_fd = subprocess.PIPE, stdin_msg: str = None) -> tuple:
    '''
    Аргумент command - команда для выполнения в терминале. Например: "ls -lai ."
    if(std_out_fd or std_err_fd) == subprocess.DEVNULL   |=>    No output enywhere
    if(std_out_fd or std_err_fd) == subprocess.PIPE      |=>    All output to return
    if(std_out_fd or std_err_fd) == open(path, "w")      |=>    All output to file path
    Возвращает кортеж, где элементы:
        0 - строка stdout
        1 - строка stderr
        2 - returncode
    '''
    _ENCODING = "utf-8"

    if(debug):
        #pout(f"> " + " ".join(command))
        if(stdin_msg != None):
            pout(f"> {command}, with stdin=\"{stdin_msg}\"")
        else:
            pout(f"> {command}")

    #proc = subprocess.run(command, shell=True, capture_output=True, input=stdin_msg.encode("utf-8"))
    if(stdin_msg == None):
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd)
    else:
        proc = subprocess.run(command, shell=True, stdout=std_out_fd, stderr=std_err_fd, input=stdin_msg.encode("utf-8"))
    
    #return (proc.stdout.decode("utf-8"), proc.stderr.decode("utf-8"))

    res_stdout = proc.stdout.decode("utf-8") if proc.stdout != None else None
    res_errout = proc.stderr.decode("utf-8") if proc.stderr != None else None
    return (res_stdout, res_errout, proc.returncode)
