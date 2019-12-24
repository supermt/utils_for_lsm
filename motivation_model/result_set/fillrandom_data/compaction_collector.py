import re
import json
import os
import glob
import statistics


def dev(input_list):
    return statistics.stdev(input_list)

def avg(input_list):
    return statistics.mean(input_list)

def column_values_time(compaction_sequence):
    return "%s,%.2f,%.2f,%s,%.2f,%s"%(len(compaction_sequence),sum([x / TRANS_MICRO_SEC for x in compaction_sequence])
                        ,max([x / TRANS_MICRO_SEC for x in compaction_sequence]),min(compaction_sequence)
                        ,avg([x / TRANS_MICRO_SEC for x in compaction_sequence]),dev(compaction_sequence))

def column_values_record(compaction_sequence):
    return "%s,%s,%s,%s,%.2f"%(len(compaction_sequence),sum(compaction_sequence)
                        ,max(compaction_sequence),min(compaction_sequence)
                        ,avg(compaction_sequence))



TRANS_MICRO_SEC = 1000000


# files = [os.path.abspath(filename) for filename in glob.glob("./**",recursive=True) if "LOG" in filename]
# print("DISK TYPE,CPU,Memtable Size,Number of Compactions,Overall Compaction Latency(sec),Max Compaction Latency(sec),Min Compaction Latency(ms),Avg of Compaction Latency(sec),Dev of Compaction Latency")
# print("DISK TYPE,CPU,Memtable Size,Number of Compactions,Overall Compaction CPU Latency(sec),Max Compaction CPU Latency(sec),Min Compaction CPU Latency(ms),Avg of Compaction CPU Latency(sec),Dev of Compaction CPU Latency")
# print("DISK TYPE,CPU,Memtable Size,Number of Compactions,Overall Compaction Input Records,Max Compaction Input Records,Min Compaction Input Records,Avg of Compaction Input Records")
# print("DISK TYPE,CPU,Memtable Size,Number of Compactions,Overall Compaction Output Records,Max Compaction Output Records,Min Compaction Output Records,Avg of Compaction Output Records,Dev of Compaction Output Records")
print("DISK TYPE,CPU,Memtable Size,Number of Compactions,Overall Compaction Redundant Records,Max Compaction Redundant Records,Min Compaction Redundant Records,Avg of Compaction Redundant Records,Dev of Compaction Redundant Records")


materials = ["PM","SATASSD","NVMeSSD"]
CPUs = [2,4,8]
memtable_sizes = [16,32,64,128]

for material in materials:
    for cpu_count in CPUs:
        for memtable_size in memtable_sizes:
            name = "%s/%s/%s"%("StorageMaterial."+material,str(cpu_count)+"CPU",str(memtable_size)+"MB")
            single_file = [os.path.abspath(filename) for filename in glob.glob(name+"/**") if "LOG" in filename][0]
            print(single_file)
            # material = single_file.split("/")[-4].split(".")[1]
            # cpu_count = single_file.split("/")[-3]
            # memtable_size = single_file.split("/")[-2]

            log_lines = open(single_file,"r").readlines()

            compaction_latencies = []
            compaction_cpu_latencies = []
            compaction_input = []
            compaction_output = []
            compaction_redundant = []
            
            for log_line in log_lines:
                line_split = re.search('(\{.+\})', log_line)
                if line_split:
                    try:
                        log_dict = json.loads(line_split[0])
                        # print(log_dict['time_micros'])
                        if log_dict['event'] == "compaction_finished":
                            compaction_latencies.append(log_dict['compaction_time_micros'])
                            compaction_cpu_latencies.append(log_dict['compaction_time_cpu_micros'])
                            compaction_input.append(log_dict['num_input_records'])
                            compaction_output.append(log_dict['num_output_records'])
                            compaction_redundant.append(log_dict['num_input_records']-log_dict['num_output_records'])
                    except json.decoder.JSONDecodeError:
                        pass
                    # print(log_line)


            print("%s,%s,%s,%s"%(material,cpu_count,memtable_size,column_values_time(compaction_latencies)))
            # print("%s,%s,%s,%s"%(material,cpu_count,memtable_size,column_values_time(compaction_cpu_latencies)))
            # print("%s,%s,%s,%s"%(material,cpu_count,memtable_size,column_values_record(compaction_input)))
            # print("%s,%s,%s,%s"%(material,cpu_count,memtable_size,column_values_record(compaction_output)))
            # print("%s,%s,%s,%s"%(material,cpu_count,memtable_size,column_values_record(compaction_redundant)))



#{'time_micros': 1576765865294212, 'job': 5865, 'event': 'compaction_finished', 
# 'compaction_time_micros': 1632160, 'compaction_time_cpu_micros': 931408, 
# 'output_level': 2, 'num_output_files': 6, 'total_output_size': 393232668, 
# 'num_input_records': 3503018, 'num_output_records': 3447878, 
# 'num_subcompactions': 1, 'output_compression': 'NoCompression', 
# 'num_single_delete_mismatches': 0, 'num_single_delete_fallthrough': 0}
