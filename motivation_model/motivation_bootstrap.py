# default path parameter

from db_bench_option import DEFAULT_DB_BENCH
from db_bench_runner import DB_launcher
from db_bench_runner import reset_CPUs
from parameter_generator import HardwareEnvironment
from parameter_generator import StorageMaterial
from db_bench_runner import clean_cgroup
from configparser import ConfigParser
import json

def load_config_file(filename='template.json'):
    f = open(filename,) 
    return json.load(f)

def set_parameters_to_env(cfg,env):
    try:
        env.config_CPU_by_list(cfg['cpu_set'])
        mem_list = cfg['memtable_size_set']
        
        mem_size_list = []

        for mem_size in mem_list:
            if type(mem_size) == str:
                mem_size_list.append(eval(mem_size))
            else:
                mem_size_list.append(mem_size)
        print(mem_size_list)
        env.config_Memory_by_list(mem_size_list)
        for storage_path in cfg['storage_paths']:
            env.add_storage_path(storage_path['path'],StorageMaterial[storage_path['media_type']])
    except KeyError as errormsg:
        print("Missing configuration entry or error configuration entry: "+str(errormsg)+" please read the template.json file as a reference")
    else:
        print("All parameter set")

if __name__ == '__main__':
    env = HardwareEnvironment()
    set_parameters_to_env(load_config_file(),env)
    
    runner = DB_launcher(env,"/home/jinghuan/basic_results", db_bench=DEFAULT_DB_BENCH)

    runner.run()
    reset_CPUs()
    clean_cgroup()
