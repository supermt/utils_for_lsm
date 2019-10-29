import os

import matplotlib.pyplot as plt

DEFAULT_IMAGE = "result.png"


def check_header(line):
    return line.split(",")[0].isdigit()


def extract_index(input_file):
    xs = []
    line = input_file.readline()
    while line:
        line = input_file.readline()
        if (check_header(line)):
            xs.append(int(line.split(",")[0]))
    return xs


def plot_file_with_index(axe, file):
    input_file = open(file, "r")
    xs = []
    index_size = []
    memtable_size = []
    sst_size = []
    index_ratio = []

    index = extract_index(input_file)

    input_file.seek(0)
    for op_seq in index:
        line = input_file.readline()
        if (check_header((line))):
            xs.append(op_seq)
            data_row = line.split(",")
            index_size.append(int(data_row[1]))
            memtable_size.append(int(data_row[2]))
            sst_size.append(int(data_row[3]))
            if float(data_row[3]) == 0:
                index_ratio.append(0)
            else:
                index_ratio.append(float(data_row[1]) / float(data_row[3]))
        else:
            pass
    index_size_line, = axe.plot(xs, index_size, "r", label="index_size")
    memtable_size_line, = axe.plot(xs, memtable_size, "g", label="memtable_size")
    # axe.plot(xs,sst_size,"b",label="sst_size")
    axe.set_title(file.split("/")[-2])
    ratio_axe = axe.twinx()
    index_ratio_line, = ratio_axe.plot(xs, index_ratio, label="index_size / sst_size")
    # ratio_axe.legend()
    # axe.legend()
    return index_size_line, memtable_size_line, index_ratio_line


def result_image_path(output_dir, sequence=0):
    if output_dir[-1] != "/":
        output_dir = output_dir + "/"
    return output_dir + str(sequence) + "_" + DEFAULT_IMAGE


def draw_frame(column, row, sequence, output_dir, files, start_point):
    fig = plt.figure(figsize=(16, 12))
    axes = fig.subplots(row, column, sharex='none', sharey='row')
    fig.text(0.5, 0.04, 'Entry Sequence', ha='center')
    fig.text(0.04, 0.5, 'Memory Usage (Bytes)',
             va='center', rotation="90")
    file_index = start_point
    label_infors = ("index_size", "memtable_size", "index_size / sst_size")
    for axes_row in axes:
        for axe in axes_row:
            label_lines = plot_file_with_index(axe, files[file_index])
            file_index += 1
            if file_index >= len(files):
                break
    save_path = result_image_path(output_dir, sequence)
    fig.legend(label_lines, label_infors)
    plt.savefig(save_path)
    plt.close()
    return save_path


def get_files(dir_path):
    files = [s for s in os.listdir(dir_path)
             if os.path.isfile(os.path.join(dir_path, s))]
    files.sort(key=lambda s: os.path.getmtime(os.path.join(dir_path, s)))
    return files


def plot_file_list_ratio(files, output_dir, column, row):
    output_dir = os.path.abspath(output_dir)
    array_size = len(files)

    if array_size < 1:
        raise Exception("no file need plotting")
    if array_size < 2:
        fig = plt.figure(figsize=(16, 12))
        plot_file_with_index(fig.subplots(1, 1), files[0])
        fig.legend()
        plt.savefig(result_image_path(output_dir, 0))
        return output_dir

    row_in_total = array_size / column
    frames = int(row_in_total / row)
    frame = 0
    start_point = 0
    result_files = []
    # print(frames)
    # files in frame
    while frame < max(frames, 1):
        result_files.append(draw_frame(column, row, frame, output_dir, files, start_point))
        start_point += (column * row)
        frame += 1
    # files at tail

    while start_point < len(files):
        fig = plt.figure(figsize=(16, 12))
        plot_file_with_index(fig.subplots(1, 1), files[start_point])
        save_path = result_image_path(output_dir, frame)
        plt.legend()
        plt.savefig(save_path)
        result_files.append(save_path)
        frame += 1
        start_point += 1
        plt.close()

    return result_files


def plot_files(file_dir, output_dir, column=2, row=2):
    files = []
    file_dir = os.path.abspath(file_dir)

    for file in get_files(file_dir):
        if "MEMORY_USAGE" in file:
            files.append(file_dir + file)

    plot_file_list_ratio(files, output_dir, column, row)
