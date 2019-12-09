# default path parameter
import multiprocessing

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_runner import DB_launcher
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial
from db_bench_runner import reset_CPUs

if __name__ == '__main__':
    env = HardwareEnvironment()
    # db_bench_options = parameter_tuning(DEFAULT_DB_BENCH, para_dic={})
    env.config_CPU(set_size=4)
    env.config_Memory(set_size=8, min_mem=(128 * 1024 * 1024), max_mem=(128 * 128 * 1024 * 1024))

    env.add_storage_path("/home/supermt/rockdb_ssd", StorageMaterial.SATASSD)
    env.add_storage_path("/media/supermt/hdd/rocksdb/db", StorageMaterial.SATAHDD)

    reset_CPUs()
    runner = DB_launcher(env, db_bench=DEFAULT_DB_BENCH)

    runner.run()
    reset_CPUs()