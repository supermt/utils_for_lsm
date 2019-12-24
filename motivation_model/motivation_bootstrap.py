# default path parameter

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial

if __name__ == '__main__':
    env = HardwareEnvironment()
    # db_bench_options = parameter_tuning(DEFAULT_DB_BENCH, para_dic={})
#    env.config_CPU(set_size=4, max_CPU=8)
    env.config_CPU_by_list([2,4,8])
    env.config_Memory(min_mem=(16 * 1024 * 1024), set_size=4)

    print(env.get_current_memory_experiment_set())

#    env.add_storage_path("/home/supermt/rockdb_ssd", StorageMaterial.SATASSD)
#    env.add_storage_path("/media/supermt/hdd/rocksdb/db", StorageMaterial.SATAHDD)
    env.add_storage_path("/home/jinghuan/rocksdb_pmem",StorageMaterial.PM_NOVA)
    env.add_storage_path("/home/jinghuan/rocksdb_nvme",StorageMaterial.NVMeSSD)
#    env.add_storage_path("/home/jinghuan/rocksdb_satassd",StorageMaterial.SATASSD)

    
    reset_CPUs()
    runner = DB_launcher(env,"/home/jinghuan/fillrandom_fixed_sstable_data", db_bench=DEFAULT_DB_BENCH)

    runner.run()
    reset_CPUs()
