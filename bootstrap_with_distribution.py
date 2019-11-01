#!/usr/bin/python3

import os
import pathlib
import subprocess
from shutil import copyfile

import psutil

from plot_util import plot_files

SUDO_PASSWD = "sasomi"
OUTPUT_PREFIX = "/home/supermt/PycharmProjects/utils_for_lsm/distribution_comparison"
DEFAULT_DB_PATH = "/media/supermt/hdd/rocksdb"
DEFAULT_BLOOM_BITS = 10


def start_db_bench(key_size, value_size, entry_count, bench_mark, compression="none", db_bench_path=DEFAULT_DB_PATH,
                   db_path=DEFAULT_DB_PATH, bloom_bits=DEFAULT_BLOOM_BITS):
    """
    Starting the db_bench thread by subprocess.popen(), return the Popen object
    ./db_bench --benchmarks="fillrandom" --key_size=16 --value_size=1024 --db="/media/supermt/hdd/rocksdb"
    """
    db_bench_path = os.path.abspath(db_bench_path)
    db_path = os.path.abspath(db_path)

    with open(db_path + "/stdout.txt", "wb") as out, open(db_path + "/stderr.txt", "wb") as err:
        print("DB_BENCH starting, with parameters:")
        parameter_list = [db_bench_path + '/db_bench', '--benchmarks=' + bench_mark, '--num=' + str(entry_count),
                          '--key_size=' + str(key_size),
                          '--value_size=' + str(value_size), '--db=' + db_path, '--compression_type=' + compression,
                          '--bloom_bits=' + str(bloom_bits)]
        print(parameter_list)
        db_bench_process = subprocess.Popen(
            parameter_list, stdout=out, stderr=err)
        sudoPassword = SUDO_PASSWD
        # in case there are too many opened files
        os.system('echo %s|sudo -S %s' % (sudoPassword, "prlimit --pid " +
                                          str(db_bench_process.pid) + " --nofile=20480:40960"))

    return db_bench_process


def para_to_dir(key_size, value_size, entry_count):
    """
    create a directory, copy the MEMORY_USAGE0 and return the absolute path of this directory
    """
    target_path = OUTPUT_PREFIX + "/MEMORY_FOOTPRINT" + \
                  "/" + str(key_size) + "+" + str(value_size) + "*" + str(entry_count)
    return target_path


def create_target_dir(target_path):
    pathlib.Path(target_path).mkdir(parents=True, exist_ok=True)


def copy_current_data(src_dir, dst_dir, timestamp, file_names=["MEMORY_USAGE0"]):
    if src_dir[-1] != '/':
        src_dir = src_dir + "/"
    if dst_dir[-1] != '/':
        dst_dir = dst_dir + "/"
    # if len(file_name) == 0 and file_name[0] == "MEMORY_USAGE0":
    #     move(src_dir + file_name[0], dst_dir +
    #          file_name[0] + "_" + str(timestamp))
    #     return

    for file_name in file_names:
        copyfile(src_dir + file_name, dst_dir +
                 file_name + "_" + str(timestamp))
    return


def single_run(key_size, value_size, entry_count, benchmark, gap, db_path, db_bench_path):
    """
    key size: the size of entry keys
    value size: the size of entry values
    entry_count: how many entry inserted into the file
    gap: sleep gap each run
    returns the output of this running
    """
    try:
        timestamp = 0
        db_bench_process = start_db_bench(
            key_size, value_size, entry_count, benchmark, db_path, db_bench_path)  # use db_path as default place
        result_dir = para_to_dir(key_size, value_size, str(entry_count)+str(benchmark))
        create_target_dir(result_dir)
        while True:
            try:
                db_bench_process.wait(gap)
                print("mission complete")
                # copy the results
                copy_current_data(db_bench_path, result_dir, timestamp, ["MEMORY_USAGE0"])
                copy_current_data(db_path, result_dir, timestamp, ["stderr.txt", "stdout.txt", "LOG"])
                break
            except subprocess.TimeoutExpired:
                timestamp = timestamp + gap
                pass
        return result_dir
    except Exception:
        p = psutil.Process(db_bench_process.pid)
        print("stopping db_bench: " + str(db_bench_process.pid))
        p.terminate()  # or p.kill()
        return result_dir


def size_to_num(size, unit):
    return size * 1000000000


if __name__ == "__main__":

    TARGET_DB_SIZE = 40
    TARGET_DB_UNIT = "GB"
    TARGET_DB_SIZE_num = size_to_num(TARGET_DB_SIZE, TARGET_DB_UNIT)  # 20 GB
    # NoveLSM 16GB, quite small, 2000000000 to 8000000000 entries

    OUTPUT_PREFIX += "/" + str(TARGET_DB_SIZE) + TARGET_DB_UNIT + "_DB_RESULT"

    benchmark_options = ["fillpoisson", "fillnormal", "fillexp", "fillpoissonrd", "fillnormalrd", "fillexprd"]

    key_size_options = [16]  # 10 bits per filter
    value_size_options = [1024]  # block size, 1/8 block size 1/2^6 block size
    for benchmark in benchmark_options:
        for key_size_option in key_size_options:
            for value_size_option in value_size_options:
                entries = min(100000000 - 1, int(TARGET_DB_SIZE_num / value_size_option))
                result_dir = single_run(key_size_option, value_size_option,
                                        entries, benchmark, 1.5, db_path=DEFAULT_DB_PATH,
                                        db_bench_path="./")
                print(result_dir)
                plot_files(result_dir, result_dir, column=2, row=2)
                print("finish experiment with value size of " +
                      str(value_size_option) + " , total entries of " + str(entries))
