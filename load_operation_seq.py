import numpy as np

import jpype as jp
from collections import Counter
from collections import OrderedDict


import matplotlib.pyplot as plt

from ZipfianGenerator import generate_zipfian

op_list = generate_zipfian(item_count=240*1024,zipfian_alpha=0.99,start_point=10000,end_point=99999)

# counting_map = Counter(op_list)

f = open("op_time.csv","w")

f.write("time,op\n")

for i in range(len(op_list)):
    f.write(str(i) + "," + str(op_list[i])+"\n")

f.close()

print("op_list finished")

# sorted_counting_map = sorted(counting_map.items(), key=lambda kv: kv[1])
# op_frequency = OrderedDict(sorted_counting_map)

# # plt.hist(op_list)
# # plt.show()


# plt.plot(op_frequency.values())
# plt.show()