#!/usr/bin/python3

import matplotlib.pyplot as plt 
import os

def plot_memory_footprint(axe,file,index):
    input_file = open(file,"r")
    xs = []
    index_size = []
    memtable_size = []
    sst_size = []
    index_ratio = []

    for op_seq in index:
        line = input_file.readline()
        if (line.split(",")[0].isdigit()):
            xs.append(op_seq)
            data_row = line.split(",")
            index_size.append(int(data_row[0]))
            memtable_size.append(int(data_row[1]))
            sst_size.append(int(data_row[2]))
            if float(data_row[2]) == 0:
                index_ratio.append(0)
            else:
                index_ratio.append(float(data_row[0])/float(data_row[2]))
        else:
           pass
    axe.plot(xs,index_size,"r",label="index_size")
    axe.plot(xs,memtable_size,"g",label="memtable_size")
    axe.plot(xs,sst_size,"b",label="sst_size")
    axe.set_title(file)
    ratio_axe = axe.twinx()
    ratio_axe.plot(xs,index_ratio,label="index_size / sst_size")
    ratio_axe.legend()
    axe.legend()

def extract_index(input_file):
    xs = []
    line = input_file.readline()
    while line:
        line = input_file.readline()
        if (line.split(",")[0].isdigit()):
            xs.append(int(line.split(",")[0]))
    return xs

if __name__ == "__main__":
    DUMP_FILE_DIR = "./"
    files = []

    # for r, d, f in os.walk(DUMP_FILE_DIR):
    #     for file_name in f:
    #         if 'MEMORY_USAGE' in file_name and 'MEMORY_USAGE_INDEX' not in file_name:
    #             files.append(file_name)
    # files.sort()

    # baseline for hdd : 1 single None Compression
    files.append("MEMORY_USAGE_1_HDD_NONE")
    # baseline for ssd : 1 single None Compression
    files.append("MEMORY_USAGE_1_SSD_NONE")
    # adding multi-thread
    files.append("MEMORY_USAGE_16_THREADS_HDD_NONE")
    # files.append("MEMORY_USAGE_16_THREADS_SSD_NONE")
    # adding compression
    files.append("MEMORY_USAGE_16_THREADS_SSD_SNAPPY")
    # files.append("MEMORY_USAGE_16_THREADS_HDD_NONE")

    column = 2

    row = 2

    fig = plt.figure()

    axes = fig.subplots(row, column, sharex=True, sharey=True)

    fig.text(0.5, 0.04, 'Entry Sequence', ha='center')
    fig.text(0.04, 0.5, 'Memory Usage (Bytes)',
             va='center', color="b", rotation="90")
    file_index = 0
    index_file = open("MEMORY_USAGE_INDEX","r")
    index = extract_index(index_file)


    for axes_row in axes:
        for axe in axes_row:
            plot_memory_footprint(axe, files[file_index],index)
            file_index += 1
            if file_index >= len(files):
                break
    plt.show()
                    
