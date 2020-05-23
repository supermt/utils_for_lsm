def get_iops_and_avg_latency(file_name):
    iops = 0
    avg_latency = 0
    record = open(file_name,"r").readlines()[-1]
    data = record.split(" ")
    avg_latency = float(data[10])
    iops = int(data[12])
    return iops,avg_latency