#!/usr/bin/python3

import os

import matplotlib.pyplot as plt

def extract_index(input_file):
    xs = []
    line = input_file.readline()
    while line:
        line = input_file.readline()
        if (line.split(",")[0].isdigit()):
            xs.append(int(line.split(",")[0]))
    return xs

def plot_file_with_index(axe,file):
    input_file = open(file,"r")
    xs = []
    index_size = []
    memtable_size = []
    sst_size = []
    index_ratio = []

    index = extract_index(input_file)

    input_file = open(file,"r")
    for op_seq in index:
        line = input_file.readline()
        if (line.split(",")[0].isdigit()):
            xs.append(op_seq)
            data_row = line.split(",")
            index_size.append(int(data_row[1]))
            memtable_size.append(int(data_row[2]))
            sst_size.append(int(data_row[3]))
            if float(data_row[3]) == 0:
                index_ratio.append(0)
            else:
                index_ratio.append(float(data_row[1])/float(data_row[3]))
        else:
           pass
    axe.plot(xs,index_size,"r",label="index_size")
    axe.plot(xs,memtable_size,"g",label="memtable_size")
    # axe.plot(xs,sst_size,"b",label="sst_size")
    axe.set_title(file)
    ratio_axe = axe.twinx()
    ratio_axe.plot(xs,index_ratio,label="index_size / sst_size")
    ratio_axe.legend()
    axe.legend()

def plot_file_with_index_total(axe,file):
    input_file = open(file,"r")
    xs = []
    index_size = []
    memtable_size = []
    sst_size = []
    index_ratio = []

    index = extract_index(input_file)

    input_file = open(file,"r")
    for op_seq in index:
        line = input_file.readline()
        if (line.split(",")[0].isdigit()):
            xs.append(op_seq)
            data_row = line.split(",")
            index_size.append(int(data_row[1]))
            memtable_size.append(int(data_row[2]))
            sst_size.append(int(data_row[3]))
            if float(data_row[3]) == 0:
                index_ratio.append(0)
            else:
                index_ratio.append(float(data_row[1])/float(data_row[3]))
        else:
           pass
    axe.plot(xs,index_size,"r",label="index_size")
    axe.plot(xs,memtable_size,"g",label="memtable_size")
    axe.plot(xs,sst_size,"b",label="sst_size")
    axe.set_title(file + " with total sst size")
    ratio_axe = axe.twinx()
    ratio_axe.plot(xs,index_ratio,label="index_size / sst_size")
    ratio_axe.legend()
    axe.legend()

if __name__ == "__main__":
    MEMORY_FOOTPRINT_FILE = "MEMORY_USAGE_199900000_Single_HDD"
    fig,axes = plt.subplots(2)
    plot_file_with_index(axes[0],MEMORY_FOOTPRINT_FILE)
    plot_file_with_index_total(axes[1],MEMORY_FOOTPRINT_FILE)
    plt.show()
