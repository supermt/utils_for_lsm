from enum import Enum

import numpy as np
import psutil


class StorageMaterial(Enum):
    PM = 1
    NVMeSSD = 2
    SATASSD = 3
    SATAHDD = 4


class HardwareEnvironment:
    # MemSetNo = 5
    # MemSetBase = 8
    # MemSetGap = 2
    #
    # CPUSetNo = 3
    # CPUSetBase = 0
    # CPUSetGap = 2

    MaxAvaliableCPU = psutil.cpu_count()
    MaxAvaliableMemory = psutil.virtual_memory().total

    CPU_experiment_set = []
    Memory_experiment_set = []
    path_list = []

    def __init__(self):
        return

    def config_CPU_by_list(self,cpu_set=[]):
        self.CPU_experiment_set=cpu_set

    def config_CPU(self, set_size, min_CPU=1, max_CPU=-1, log_scale=True):
        if log_scale:
            # use log scale to generate parameter set
            if (max_CPU < 0):
                max_CPU = self.MaxAvaliableCPU
            self.CPU_experiment_set = np.linspace(min_CPU, max_CPU, set_size, endpoint=True, dtype=int)
        else:
            if max_CPU < 0:
                max_CPU = self.MaxAvaliableCPU
            max_CPU += 1
            step = int((max_CPU - min_CPU) / set_size)
            self.CPU_experiment_set = list(range(min_CPU, max_CPU, step))

    def config_Memory(self, min_mem, set_size):
        # memory can not be given by default, for it's related to the Memtable copy number
        # use log scale to generate parameter set
        result = []
        for i in range(0,set_size):
            result.append(min_mem * (2**i))
        self.Memory_experiment_set = result

    def get_current_memory_experiment_set(self):
        return self.Memory_experiment_set

    def get_current_CPU_experiment_set(self):
        return self.CPU_experiment_set

    def add_storage_path(self, db_path, storage_material):
        self.path_list.append((db_path, storage_material))

    def get_storage_paths(self):
        return self.path_list
