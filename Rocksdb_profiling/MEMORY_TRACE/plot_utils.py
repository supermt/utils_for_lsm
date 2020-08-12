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
