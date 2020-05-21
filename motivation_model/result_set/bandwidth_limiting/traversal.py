#!/usr/bin/env python3 
import os
import sqlite3
def traversal_logic(indices):
    results = []
    intercept = ","
    keys = indices.keys()

    for key in keys:
        print(key + intercept,end='')    
    print(list(keys))
    recursive_in(list(keys))

def recursive_in(prefix_list,line=""):
    if len(prefix_list) == 1:
        print(line + prefix_list[0])
    else:
        print(prefix_list[0]) 
        recursive_in(prefix_list[1:],line + prefix_list[0])

def get_log_dirs(prefix="."):
    result_dirs = []
    for root, dirs, files in os.walk(prefix, topdown=False):
        for dir in dirs:
            if "MB" in dir:
                result_dirs.append(os.path.join(root,dir)[2:])
    return result_dirs 

def get_log_and_std_files(prefix="."):
    LOG_FILES = []
    stdout_files = []
    for root, dirs, files in os.walk(prefix, topdown=False):
        for filename in files:
            if "stdout" in filename:
                stdout_files.append(os.path.join(root, filename)[2:])
            if "LOG" in filename:
                LOG_FILES.append(os.path.join(root, filename)[2:])
    return stdout_files,LOG_FILES 

if __name__ == "__main__":
    # traversal_logic(
    #     {
    #         "size":["400mb","800mb","1200mb","1600mb","2000mb",],
    #         "media":["StorageMaterial.NVMeSSD"],
    #         "cpu":["1CPU","2CPU","3CPU","4CPU","8CPU","12CPU"],
    #         "batch_size":["16MB","32MB","64MB","128MB"]
    #     }
    # )

    dirs = get_log_dirs()
    print("file loaded")
   
    conn = sqlite3.connect('speed_info.db')
    
    
    