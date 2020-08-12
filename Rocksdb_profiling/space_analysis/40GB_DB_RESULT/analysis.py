#!/usr/bin/python3
import glob
import os

from plot_util import plot_file_list_ratio


def resolve_dir_names(dir_list):
    """
    :param dir_list: the file list need to resolve
    :return: the parameter information dict
    """
    # key_size * value_size * entry_counts
    result_dict = {}
    parameter_lists = [set(), set(), set()]

    for file_name in dir_list:
        i = 0
        for value in (file_name.split("/")[-1]).split("*"):
            parameter_lists[i].add(value)
            i += 1
    result_dict["key_size"] = parameter_lists[0]
    result_dict["value_size"] = parameter_lists[1]
    result_dict["entry_counts"] = parameter_lists[2]
    for key in result_dict:
        result_dict[key] = list(result_dict[key])
        result_dict[key].sort(key=float)

    result_dict["entry_counts"].reverse()
    return result_dict


def sort_files_by_parameter(file_list):
    """
    :param file_list: unordered list
    :return: ordered list
    """
    result = []
    param_dict = resolve_dir_names(file_list)
    for key_size in param_dict["key_size"]:
        i = 0
        for value_size in param_dict["value_size"]:
            entry_no = param_dict["entry_counts"][i]
            result.append(key_size + "*" + value_size + "*" + entry_no)
            i += 1
    return result


def collect_footprints(input_dir):
    memory_footprint_dir = [dir for dir in os.listdir(input_dir) if os.path.isdir(dir)]
    sorted_dir = sort_files_by_parameter(memory_footprint_dir)
    footprints = []
    for dir in sorted_dir:
        footprints.extend(glob.glob(dir + "/MEMORY_USAGE*"))
    return footprints


if __name__ == '__main__':
    files = collect_footprints("./")
    # print(files)
    plot_figure_list = plot_file_list_ratio(files, "./", 5, 3)
    print("Plot Finished")
