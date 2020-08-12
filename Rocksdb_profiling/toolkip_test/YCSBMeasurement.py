#!/usr/bin/python3

import os
import subprocess
from time import sleep
import signal
import sys


def start_db_bench(DB_PATH):

    db_process = subprocess.Popen(['./db_bench','--benchmarks=fillrandom'],stdout=subprocess.PIPE)
    print(db_process.pid)
    return db_process.pid
if __name__ == "__main__":
    DB_PATH = "/media/supermt/hdd/rocksdb"
    if len(os.sys.argv) > 1:
        DB_PATH = os.sys.argv[1]
    try:
        db_bench_id = start_db_bench(DB_PATH)
    except KeyboardInterrupt as identifier:
        os.kill(db_bench_id)
        exit(0)
