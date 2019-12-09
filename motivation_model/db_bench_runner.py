import os
import pathlib
from shutil import rmtree

from db_bench_option import *
from db_bench_option import CPU_IN_TOTAL
from parameter_generator import HardwareEnvironment


def turn_on_cpu(id):
    # command = "echo 1 | sudo tee /sys/devices/system/cpu/cpu1/online"
    os.system('echo %s | echo 1 | sudo tee /sys/devices/system/cpu/cpu%s/online' % (SUDO_PASSWD, id))


def turn_off_cpu(id):
    # command = "echo 1 | sudo tee /sys/devices/system/cpu/cpu1/online"
    os.system('echo %s | echo 0 | sudo tee /sys/devices/system/cpu/cpu%s/online' % (SUDO_PASSWD, id))


def restrict_cpus(count):
    reset_CPUs()
    if (count > CPU_IN_TOTAL):
        # too many cores asked
        print("no that many cpu cores")
        return
    else:
        for id in range(count, CPU_IN_TOTAL):
            turn_off_cpu(id)


def reset_CPUs():
    for id in range(1, CPU_IN_TOTAL):
        turn_on_cpu(id)
    print("Reset all cpus")


def start_db_bench(db_bench_path, db_path, options={}):
    """
    Starting the db_bench thread by subprocess.popen(), return the Popen object
    ./db_bench --benchmarks="fillrandom" --key_size=16 --value_size=1024 --db="/media/supermt/hdd/rocksdb"
    """
    db_bench_path = os.path.abspath(db_bench_path)
    db_path = os.path.abspath(db_path)
    options["db"] = db_path
    with open(db_path + "/stdout.txt", "wb") as out, open(db_path + "/stderr.txt", "wb") as err:
        print("DB_BENCH starting, with parameters:")
        db_bench_options = parameter_tuning(db_bench_path, para_dic=options)
        print(db_bench_options)
        db_bench_process = ""
        #     os.subprocess.Popen(
        #     db_bench_options, stdout=out, stderr=err)
        # # in case there are too many opened files
        # os.system('echo %s|sudo -S %s' % (SUDO_PASSWD, "prlimit --pid " +
        #                                   str(db_bench_process.pid) + " --nofile=20480:40960"))

    return db_bench_process


def create_target_dir(target_path):
    try:
        pathlib.Path(target_path).mkdir(parents=True, exist_ok=False)
    except:
        print("Path Exists, clearing the files")
        rmtree(target_path)
        pathlib.Path(target_path).mkdir(parents=True, exist_ok=False)


class DB_TASK:
    db_bench_path = ""
    result_dir = ""
    parameter_list = {}

    def __init__(self, para_list):
        self.parameter_list = para_list

    def set_path(self, db_bench_path, result_dir):
        self.db_bench_path = db_bench_path
        self.result_dir = result_dir

    def run(self):
        restrict_cpus(self.parameter_list["max_background_compactions"])
        start_db_bench(self.db_bench_path, self.parameter_list["db"], self.parameter_list)

        reset_CPUs()
        return


class DB_launcher:
    db_bench_tasks = []
    db_bench_path = ""

    def __init__(self, env: HardwareEnvironment, db_bench=DEFAULT_DB_BENCH):
        # for parameter_set in parameter_sets:
        #     running_process = start_db_bench(db_bench, parameter_set["storage_path"],
        #                                      parameter_set["running_parameter"])
        #     self.db_bench_processes.append(running_process)
        self.db_bench_path = db_bench
        print(env.get_storage_paths())
        print(env.get_current_CPU_experiment_set())
        print(env.get_current_memory_experiment_set())

        self.prepare_directories(env)

        return

    def prepare_directories(self, env: HardwareEnvironment, work_dir="./db"):
        work_dir = os.path.abspath(work_dir)
        # do not clean this directory
        pathlib.Path(work_dir).mkdir(parents=True, exist_ok=True)

        # check all parameters, prepare the directories and init the tasks

        sub_path = work_dir + "/"

        temp_para_dict = {}

        for material in env.path_list:
            material_dir = sub_path + str(material[1])
            pathlib.Path(material_dir).mkdir(parents=True, exist_ok=True)
            temp_para_dict["db"] = str(material[0])
            for cpu_count in env.get_current_CPU_experiment_set():
                result_dir = material_dir + "/" + str(cpu_count) + "CPU"
                temp_para_dict["max_background_compactions"] = str(cpu_count)
                for memory_budget in env.get_current_memory_experiment_set():
                    temp_para_dict["write_buffer_size"] = memory_budget
                    target_dir = result_dir + "/" + str(int(memory_budget / 1024 / 1024)) + "MB"
                    create_target_dir(target_dir)
                    self.db_bench_tasks.append(DB_TASK(temp_para_dict))

        return

    def run(self):
        for task in self.db_bench_tasks:
            task.run()
