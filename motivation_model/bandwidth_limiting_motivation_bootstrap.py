# default path parameter

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_option import CPU_IN_TOTAL
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial
import os

if __name__ == '__main__':
    env = HardwareEnvironment()
    CPU_IN_TOTAL = 12
    io_bandwidth=[400,800,1200,1600,2000]
    path_suffix = [str(band)+"mb" for band in io_bandwidth] 
    
    env.config_CPU_by_list([8])
    env.config_Memory(min_mem=(64 * 1024 * 1024), set_size=1)

    env.add_storage_path("/home/jinghuan/rocksdb_nvme",StorageMaterial.NVMeSSD)
    # env.add_storage_path("/home/jinghuan/rocksdb_pmem",StorageMaterial.NVMeSSD)

    reset_CPUs()
   
    for bandwidth in io_bandwidth:
        os.system('cgset -r blkio.throttle.write_bps_device="259:0 '+str(bandwidth*1024*1024)+'" /')
        os.system('cgget / | grep blkio.throttle.write_bps_device')
        print("/home/jinghuan/fillrandom_bandwidth_limiting"+str(bandwidth)+"mb")
        DB_launcher(env,"/home/jinghuan/bandwidth_limiting/"+str(bandwidth)+"mb", db_bench=DEFAULT_DB_BENCH).run()

    reset_CPUs()
