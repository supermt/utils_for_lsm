import matplotlib.pyplot as plt
import os

DEFAULT_IMAGE = "result.png"


def extract_index(input_file):
    xs = []
    line = input_file.readline()
    while line:
        line = input_file.readline()
        if (line.split(",")[0].isdigit()):
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

    input_file = open(file, "r")
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
    axe.plot(xs, index_size, "r", label="index_size")
    axe.plot(xs, memtable_size, "g", label="memtable_size")
    # axe.plot(xs,sst_size,"b",label="sst_size")
    axe.set_title(str(xs[-1]) + "ops")
    ratio_axe = axe.twinx()
    ratio_axe.plot(xs, index_ratio, label="index_size / sst_size")
    ratio_axe.legend()
    axe.legend()

# def plot_file_with_index_total(axe,file):
#     input_file = open(file,"r")
#     xs = []
#     index_size = []
#     memtable_size = []
#     sst_size = []
#     index_ratio = []

#     index = extract_index(input_file)

#     input_file = open(file,"r")
#     for op_seq in index:
#         line = input_file.readline()
#         if (line.split(",")[0].isdigit()):
#             xs.append(op_seq)
#             data_row = line.split(",")
#             index_size.append(int(data_row[1]))
#             memtable_size.append(int(data_row[2]))
#             sst_size.append(int(data_row[3]))
#             if float(data_row[3]) == 0:
#                 index_ratio.append(0)
#             else:
#                 index_ratio.append(float(data_row[1])/float(data_row[3]))
#         else:
#            pass
#     axe.plot(xs,index_size,"r",label="index_size")
#     axe.plot(xs,memtable_size,"g",label="memtable_size")
#     axe.plot(xs,sst_size,"b",label="sst_size")
#     axe.set_title(file + " with total sst size")
#     ratio_axe = axe.twinx()
#     ratio_axe.plot(xs,index_ratio,label="index_size / sst_size")
#     ratio_axe.legend()
#     axe.legend()


def result_image_path(OUTPUT_DIR, Sequence=0):
    if OUTPUT_DIR[-1] != "/":
        OUTPUT_DIR = OUTPUT_DIR + "/"
    return OUTPUT_DIR + str(Sequence) + "_" + DEFAULT_IMAGE


def draw_frame(column, row, sequence, OUTPUT_DIR, files, start_point):
    fig = plt.figure(figsize=(16, 12))
    axes = fig.subplots(row, column, sharex=True, sharey=True)
    fig.text(0.5, 0.04, 'Entry Sequence', ha='center')
    fig.text(0.04, 0.5, 'Memory Usage (Bytes)',
             va='center', rotation="90")
    file_index = start_point

    for axes_row in axes:
        for axe in axes_row:
            plot_file_with_index(axe, files[file_index])
            file_index += 1
            if file_index >= len(files):
                break

    plt.savefig(result_image_path(OUTPUT_DIR, sequence))
    plt.close()


def getfiles(dirpath):
    files = [s for s in os.listdir(dirpath)
             if os.path.isfile(os.path.join(dirpath, s))]
    files.sort(key=lambda s: os.path.getmtime(os.path.join(dirpath, s)))
    return files


def plot_files(FILE_DIR, OUTPUT_DIR, column=2, row=2):
    files = []
    if FILE_DIR[-1] != "/":
        FILE_DIR = FILE_DIR + "/"

    for file in getfiles(FILE_DIR):
        if "MEMORY_USAGE" in file:
            files.append(FILE_DIR + file)
    print(files)
    if (len(files) < 1):
        raise Exception("no file need plotting")

    if (len(files) < 2):
        fig = plt.figure(figsize=(16, 12))
        plot_file_with_index(fig.subplots(1, 1), files[0])
        # print("saving the image at: " + result_image_path(OUTPUT_DIR, 0))
        plt.savefig(result_image_path(OUTPUT_DIR, 0))
        return

    row_in_total = len(files) / column
    frames = int(row_in_total / row)
    frame = 0
    start_point = 0
    # files in frame
    while frame < frames:
        draw_frame(column, row, frame, OUTPUT_DIR, files, start_point)
        start_point += (column * row)
        frame += 1
    # files at tail

    while start_point < len(files):
        fig = plt.figure(figsize=(16, 12))
        plot_file_with_index(fig.subplots(1, 1), files[start_point])
        plt.savefig(result_image_path(OUTPUT_DIR, frame))
        frame += 1
        start_point += 1
        plt.close()
