#!/usr/bin/python3
import glob
import os

import matplotlib.pyplot as plt
import numpy as np

OP_LIST = ["fillseq", "fillseqdeterministic", "fillsync", "fillrandom", "filluniquerandomdeterministic", "overwrite",
           "readrandom", "newiterator", "newiteratorwhilewriting", "seekrandom", "seekrandomwhilewriting",
           "seekrandomwhilemerging", "readseq", "readreverse", "compact", "compactall", "multireadrandom", "mixgraph",
           "readseq", "readtocache", "readreverse", "readwhilewriting", "readwhilemerging", "readwhilescanning",
           "readrandomwriterandom", "updaterandom", "xorupdaterandom", "randomwithverify", "fill100K", "crc32c",
           "xxhash", "compress", "uncompress", "acquireload", "fillseekseq", "randomtransaction", "randomreplacekeys",
           "timeseries", "getmergeoperands"]


def extract_performance(line):
    speed = 0
    workload = ""
    speed = 10.0  # sec / op
    return workload, speed


def get_speed_info(filename):
    speed_dict = {}
    workloads = set()
    db_size = [part for part in filename.split("/") if "DB_RESULT" in part][0]

    file = open(filename)
    lines = file.readlines()
    for line in lines:
        splits = line.split(":")
        if len(splits) == 2:
            key, record = line.split(":")
            if (key is not None) and (key.replace(" ", "")) in OP_LIST:  # determine if its a resolve line
                # fillrandom   :       7.187 micros/op 139140 ops/sec;   76.4 MB/s
                key = key.replace(" ", "")
                workloads.add(key)

                speeds, bandwidth = record.split(";")
                speeds = [word for word in speeds.split(" ") if word is not ""]
                avg_time_per_op = speeds[0]
                avg_ops_per_sec = speeds[2]
                speed_dict.setdefault(key, [filename.split("/")[-2], db_size, float(avg_time_per_op),
                                            float(avg_ops_per_sec)])

    return workloads, speed_dict


# def autolabel(rects):
#     """Attach a text label above each bar in *rects*, displaying its height."""
#     for rect in rects:
#         height = rect.get_height()
#         ax.annotate('{}'.format(height),
#                     xy=(rect.get_x() + rect.get_width() / 2, height),
#                     xytext=(0, 3),  # 3 points vertical offset
#                     textcoords="offset points",
#                     ha='center', va='bottom')


if __name__ == '__main__':

    statics_files = [os.path.abspath(filename) for filename in glob.glob("./*DB_RESULT/**", recursive=True) if
                     ("stdout" in filename)]
    workloads = set()
    plot_dict = {}
    for statics_file in statics_files:
        workload_period, result_dict = get_speed_info(statics_file)
        workloads.update(workload_period)
        for workload in workloads:
            if result_dict.get(workload):
                plot_dict.setdefault(workload, []).append(result_dict.get(workload))

    speed_bars = np.asmatrix(plot_dict["fillrandom"])
    labels = set()
    data_grid = {}
    [labels.add(str(v[0, 0])) for v in speed_bars[:, 1]]

    # all parameter sets, each as a x tick
    groups = set()
    for row in np.asmatrix(speed_bars):
        param_set = row[0, 0][0:len(row[0, 0]) - row[0, 0][::-1].find("*") - 1]
        groups.add(param_set)

    groups = list(groups)
    groups.sort()

    # init the dict
    for label in labels:
        data_grid[label] = [0] * len(groups)

    for row in np.asmatrix(speed_bars):
        # print(row)
        current_param_set = row[0, 0][0:len(row[0, 0]) - row[0, 0][::-1].find("*") - 1]
        column_no = groups.index(current_param_set)
        label = row[0, 1]
        speed = row[0, 3]
        #     for param in groups:
        #         if param_set in current_param_set:
        data_grid[label][column_no] = float(speed)

    print(data_grid)
    fig, ax = plt.subplots()

    x = np.arange(len(groups))  # the label locations
    width = 0.70  # the width of the bars
    gap = width / len(labels)
    offset = -0.5 * (width - gap)  # offset from the width
    col = 0
    for label_ in labels:
        rects = ax.bar(x + offset, data_grid[label_], gap, label=label_)
        offset += width / len(labels)
        col += 1

    ax.set_xticks(x)
    ax.set_yscale('log')
    ax.set_xticklabels(groups)
    ax.legend()
    plt.xticks(rotation='vertical')
    plt.savefig("./throughput.png")
    plt.close()
