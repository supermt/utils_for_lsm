# default path parameter

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from db_bench_option import parameter_list as pdl
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial

if __name__ == '__main__':
    env = HardwareEnvironment()
    env.config_CPU_by_list([12])
    env.config_Memory(min_mem=(64 * 1024 * 1024), set_size=1)

    env.add_storage_path("/home/jinghuan/rocksdb_nvme",StorageMaterial.NVMeSSD)
    env.add_storage_path("/home/jinghuan/rocksdb_hdd",StorageMaterial.SATAHDD)
    env.add_storage_path("/home/jinghuan/rocksdb_ssd",StorageMaterial.SATASSD)
    
#    env.add_storage_path("/home/jinghuan/rocksdb_pmem",StorageMaterial.NVMeSSD)

    reset_CPUs()
    pdl["use_direct_io_for_flush_and_compaction"]=False
    runner = DB_launcher(env,"/home/jinghuan/none_direct_io", db_bench=DEFAULT_DB_BENCH)
    runner.run()

    # set db_option here
    pdl["use_direct_io_for_flush_and_compaction"]=True
    runner = DB_launcher(env,"/home/jinghuan/with_direct_io", db_bench=DEFAULT_DB_BENCH)
    runner.run()

    reset_CPUs()
