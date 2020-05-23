import json
import re
import gzip

def open_file(file_name):
    log_file = None
    if "gz" in file_name:
        log_file = gzip.open(file_name,"r")
    else:
        log_file = open(file_name,"r")
    
    return log_file

def handle_compaction_line(line):
    result = {}
    print("compaction_finished")
    return result

def handle_flush_line(line):
    result = {}
    return result

def get_data_list(log_file):
    for line in log_file.readlines():
        line = str(line)
        line = re.search('(\{.+\})', line)
        if line: 
            log_row = json.loads(line[0])
            if "compaction_finished" in str(log_row):
            # if log_row['event'] == 'compaction_finished':
                handle_compaction_line(log_row)
            if log_row['event'] == 'flush_finished':
                handle_flush_line(log_row)

