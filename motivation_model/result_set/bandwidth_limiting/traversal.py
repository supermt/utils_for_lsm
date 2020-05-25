#!/usr/bin/env python3
import os
import sqlite3
import log_file_handler as log_reader
import stdout_file_handler as std_reader
#from string_utils import bandwidth_string_sort
from functools import cmp_to_key
import plotly.graph_objects as go
import plotly.subplots
import pandas as pd


def traversal_logic(indices):
    results = []
    intercept = ","
    keys = indices.keys()

    for key in keys:
        print(key + intercept, end='')
    print(list(keys))
    recursive_in(list(keys))


def recursive_in(prefix_list, line=""):
    if len(prefix_list) == 1:
        print(line + prefix_list[0])
    else:
        print(prefix_list[0])
        recursive_in(prefix_list[1:], line + prefix_list[0])


def get_log_dirs(prefix="."):
    result_dirs = []
    for root, dirs, files in os.walk(prefix, topdown=False):
        for dir in dirs:
            if "MB" in dir:
                result_dirs.append(os.path.join(root, dir))
    return result_dirs


def get_log_and_std_files(prefix="."):
    LOG_FILES = []
    stdout_files = []
    for root, dirs, files in os.walk(prefix, topdown=False):
        for filename in files:
            if "stdout" in filename:
                stdout_files.append(os.path.join(root, filename))
            if "LOG" in filename:
                LOG_FILES.append(os.path.join(root, filename))
    return stdout_files, LOG_FILES


def create_data_table(conn):
    c = conn.cursor()

    c.execute('''Drop Table if exists speed_results''')
    c.execute("CREATE TABLE speed_results (bandwidth text, media text, cpu text, batch_size text," +
              "IOPS INT, average_latency_ms REAL" +
              # ",compaction_frequency INT, overall_compaction_latency INT" +
              # ",overall_compaction_cpu_latency INT"+
              # ",overall_input_record INT"+
              # ",overall_output_record INT"+
              # ",overall_redundant_record INT"+
              ")")
    conn.commit()

    print("table created")


def get_row(dir_path):
    stdfile, logfile = get_log_and_std_files(dir_path)
    primary_key_list = dir_path.split("/")[-4:]
    data_row = ""

    for split in primary_key_list:
        data_row += "'"+split.replace("StorageMaterial.", "")+"',"

    # logfile = log_reader.oepn_file(logfile[0])
    iops, avg_latency = std_reader.get_iops_and_avg_latency(stdfile[0])

    data_row += str(iops) + "," + str(avg_latency)
# skip log handling first

#        print("handling "+ str(logfile[0]))
#        logfile = log_reader.open_file(logfile[0])

#        log_reader.get_data_list(logfile)
    return data_row


if __name__ == "__main__":
    dirs = get_log_dirs()
    print("file loaded")

    db_conn = sqlite3.connect('speed_info.db')

    create_data_table(db_conn)

    insert_sql_head = "INSERT INTO speed_results VALUES"

    for dir in dirs:
        sql_data_row = get_row(dir)
        sql_sentence = insert_sql_head + "(" + sql_data_row + ")"
        db_conn.execute(sql_sentence)

    cursor = db_conn.cursor()

    
    cpu_group = [1, 4, 8,12]
    cpu_group = [str(x) + "CPU" for x in cpu_group]
    bandwidth_group = ['400', '800', '1200', '1600', '2000']
    bandwidth_group = [x + "mb" for x in bandwidth_group]
#   size_color = {16: "rgb(66,106,199)", 32: "rgb(254,117,0)",
#              64: "rgb(165,165,165)", 128: "rgb(255,194,0)"}
    
    media = "NVMeSSD"
    batch_size_group = ["16MB","32MB","64MB","128MB"]
    
    df = pd.read_sql_query("SELECT * FROM speed_results", db_conn)

    # print(df)
    import plotly.express as px

    fig = px.bar(df,x="cpu",y="IOPS",color="batch_size",barmode="group",
                facet_col="bandwidth",
                facet_row="media",
                category_orders={
                    # "bandwidth":["400mb","800mb","1200mb","1600mb","2000mb","unlimited"]
                    "bandwidth":bandwidth_group,
                    "cpu":cpu_group,
                    "batch_size":batch_size_group
                },
                labels={"cpu":"","IOPS":"Overall Throughput (OPs/sec)"},
                # range_y=[100000,300000]
            )
    fontsize=20
    fig.update_layout(
        autosize=False,
        width=1600,
        height=900,
        # margin=dict(l=fontsize,r=fontsize,t=fontsize,b=fontsize),
        paper_bgcolor="LightSteelBlue",
        # yaxis=dict(title="IOPS"),
        xaxis=dict(autorange=True),
        font=dict(size=fontsize),
    )
    fig.update_yaxes(automargin=True)
    # fig.show()
    fig.write_image("image/CPUvsBandwidth.pdf")
