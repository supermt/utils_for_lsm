# default path parameter

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial

if __name__ == '__main__':
    env = HardwareEnvironment()
    # db_bench_options = parameter_tuning(DEFAULT_DB_BENCH, para_dic={})
    # env.config_CPU(set_size=4, max_CPU=8)
    env.config_CPU_by_list([1,2,4,8])
    env.config_Memory(min_mem=(128 * 1024 * 1024), set_size=8)

    env.add_storage_path("/home/supermt/rockdb_ssd", StorageMaterial.SATASSD)
    env.add_storage_path("/media/supermt/hdd/rocksdb/db", StorageMaterial.SATAHDD)

    reset_CPUs()
    runner = DB_launcher(env, db_bench=DEFAULT_DB_BENCH)

    runner.run()
    reset_CPUs()
    # db_option = ['/media/supermt/hdd/rocksdb/db_bench', '--db=/media/supermt/hdd/rocksdb/db', '--benchmarks=fillseq',
    #  '--num=483183820', '--key_size=8', '--value_size=100', '--block_size=65536', '--write_buffer_size=1342177280',
    #  '--target_file_size_base=5368709120', '--min_write_buffer_number_to_merge=1', '--max_write_buffer_number=1',
    #  '--level0_file_num_compaction_trigger=4', '--max_background_compactions=1', '--max_background_flushes=1',
    #  '--threads=1', '--bloom_bits=10', '--compression_type=none']
