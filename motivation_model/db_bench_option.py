import multiprocessing
from configparser import ConfigParser

default_cfg = ConfigParser()
default_cfg.read("default.ini")

SUDO_PASSWD = default_cfg.get("Permission","passwd")
DEFAULT_DB_BENCH = default_cfg.get("Paths","db_bench_path")

# default Memory parameter
DEFAULT_MEMTABLE_SIZE = 64 * 1024 * 2014  # 256M, memtable size
DEFAULT_IMMU_COUNT = 2  # how many immutable tables
DEFAULT_IMMU_COMBIN = 1  # forget about this
DEFAULT_COMPACTION_TRIGGER = 4  # how many l0 compacted to l1
DEFAULT_L1_SIZE = 64 * 1024 * 1024


# default disk options
DEFAULT_BLOCK_SIZE = 64 * 1024  # 64 KB block
DEFAULT_COMPRESSION = "none"

# default disk caching options, runtime memory overhead
DEFAULT_BLOOM_BIT = 10

# default entry options
DEFAULT_KEY_SIZE = 8
DEFAULT_VALUE_SIZE = 100
DEFAULT_DB_SIZE = int(default_cfg.get("Entry Control","db_size"))
DEFAULT_ENTRY_COUNT = int(DEFAULT_DB_SIZE / DEFAULT_VALUE_SIZE)

# default CPU options
DEFAULT_COMPACTION_WORKER = str(multiprocessing.cpu_count())
CPU_IN_TOTAL = int(default_cfg.get("CPU","cpu_in_total"))

parameter_list = {
    "db": DEFAULT_DB_BENCH,
    "benchmarks": "fillrandom",
    "num": DEFAULT_ENTRY_COUNT,
    "key_size": DEFAULT_KEY_SIZE,
    "value_size": DEFAULT_VALUE_SIZE,
    "block_size": str(DEFAULT_BLOCK_SIZE),
    "write_buffer_size": DEFAULT_MEMTABLE_SIZE,  # Memtable Size, 256 M
    "target_file_size_base": str(DEFAULT_L1_SIZE),  # L1 FILE
    "min_write_buffer_number_to_merge": DEFAULT_IMMU_COMBIN,
    "max_write_buffer_number": DEFAULT_IMMU_COUNT,
    "level0_file_num_compaction_trigger": DEFAULT_COMPACTION_TRIGGER,
    "max_background_compactions": DEFAULT_COMPACTION_WORKER,
    "max_background_flushes": 1,  # we are focus on single material environment
    "threads": 1,  # control the input pressure, increase all resource requirement
    "bloom_bits": str(DEFAULT_BLOOM_BIT),
    "compression_type": DEFAULT_COMPRESSION,
    "base_background_compactions": 1,
    "report_bg_io_stats": False,
    "subcompactions": 1,  # How many subcompactions will be applied to L0 Compaction
}


def tuning_strategy_l0_equals_l1():
    # parameter_list["max_bytes_for_level_base"] = int(parameter_list["target_file_size_base"]) * 10
    # parameter_list["min_write_buffer_number_to_merge"] = int(parameter_list["max_bytes_for_level_base"] / int(
    #     int(parameter_list["level0_file_num_compaction_trigger"]) * int(parameter_list["write_buffer_size"])))
    parameter_list["max_bytes_for_level_base"] = int(parameter_list["write_buffer_size"]) * int(parameter_list["min_write_buffer_number_to_merge"]) * int(parameter_list["level0_file_num_compaction_trigger"])

def basic_tuning():
    parameter_list["target_file_size_base"] = int(parameter_list["write_buffer_size"])
    # int(parameter_list["write_buffer_size"]) * int(
        # parameter_list["min_write_buffer_number_to_merge"]) * int(parameter_list["level0_file_num_compaction_trigger"])


def parameter_tuning(db_bench, para_dic={}):
    if db_bench == "":
        db_bench = DEFAULT_DB_BENCH
    #filled_para_list = ["cgexec -g blkio:test_group1",db_bench]
    # filled_para_list = ['/usr/bin/cgexec','-g','blkio:test_group1',db_bench]
    filled_para_list = [db_bench]
    # use para_dic to modify the default parameter
    for para in para_dic:
        parameter_list[para] = str(para_dic[para])

    # choose tuning strategy
    basic_tuning()
    tuning_strategy_l0_equals_l1()

    # some values need calculation
    parameter_list["num"] = str(int(DEFAULT_DB_SIZE / int(parameter_list["value_size"])))
    parameter_list["base_background_compactions"] = parameter_list["max_background_compactions"]
    parameter_list["max_background_jobs"] = int(parameter_list["max_background_compactions"]) + 1

    for parameter in parameter_list:
        filled_para = "--" + parameter + "=" + str(parameter_list[parameter])
        filled_para_list.append(filled_para)
    
    return filled_para_list


def parameter_printer(filled_para_list):
    command = ""
    for para in filled_para_list:
        command += (para + " ")
    return command
