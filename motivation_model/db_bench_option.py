import multiprocessing

SUDO_PASSWD = "sasomi"
OUTPUT_PREFIX = "/home/supermt/PycharmProjects/utils_for_lsm/thread_influence"
DEFAULT_DB_BENCH = "/media/supermt/hdd/rocksdb/db_bench"
DEFAULT_DB_PATH = "/home/supermt/rockdb_ssd"
DEFAULT_BLOOM_BITS = 10

# default Memory parameter
DEFAULT_MEMTABLE_SIZE = 256 * 1024 * 2014  # 256M, memtable size
DEFAULT_IMMU_COUNT = 1  # how many immutable tables
DEFAULT_IMMU_COMBIN = 1  # forget about this
DEFAULT_COMPACTION_TRIGGER = 4  # how many l0 compacted to l1
DEFAULT_L1_SIZE = DEFAULT_MEMTABLE_SIZE * DEFAULT_IMMU_COMBIN * DEFAULT_COMPACTION_TRIGGER  # L1 file shoule equal to this

# default disk options
DEFAULT_BLOCK_SIZE = 64 * 1024  # 64 KB block
DEFAULT_COMPRESSION = "none"

# default disk caching options, runtime memory overhead
DEFAULT_BLOOM_BIT = 10

# default entry options
DEFAULT_KEY_SIZE = 8
DEFAULT_VALUE_SIZE = 100
DEFAULT_DB_SIZE = int(45 * 1024 * 1024 * 1024)
DEFAULT_ENTRY_COUNT = int(DEFAULT_DB_SIZE / DEFAULT_VALUE_SIZE)

# default CPU options
DEFAULT_COMPACTION_WORKER = str(multiprocessing.cpu_count())
CPU_IN_TOTAL = 8


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
}


def parameter_tuning(db_bench, para_dic={}):
    """
    tuning the parameter, set the default value
    """
    if db_bench == "":
        db_bench = DEFAULT_DB_BENCH
    filled_para_list = [db_bench]

    # use para_dic to modify the default parameter
    for para in para_dic:
        parameter_list[para] = str(para_dic[para])

    # values need calculation
    # L1 file should equal to the total size of L0 files
    # use total DB size to control entry counts

    parameter_list["target_file_size_base"] = int(parameter_list["write_buffer_size"]) * int(
        parameter_list["min_write_buffer_number_to_merge"]) * int(parameter_list["level0_file_num_compaction_trigger"])
    parameter_list["num"] = str(int(DEFAULT_DB_SIZE / int(parameter_list["value_size"])))

    for parameter in parameter_list:
        filled_para = "--" + parameter + "=" + str(parameter_list[parameter])
        filled_para_list.append(filled_para)

    return filled_para_list
