# default path parameter

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial

if __name__ == '__main__':
    env = HardwareEnvironment()
    env.config_CPU_by_list([8])
    env.config_Memory(min_mem=(64 * 1024 * 1024), set_size=1)

    env.add_storage_path("/home/jinghuan/rocksdb_nvme",StorageMaterial.PM)
    env.add_storage_path("/home/jinghuan/rocksdb_pmem",StorageMaterial.NVMeSSD)

    reset_CPUs()
    runner = DB_launcher(env,"/home/jinghuan/fillrandom_detailed_tuned", db_bench=DEFAULT_DB_BENCH)

    runner.run()
    reset_CPUs()
