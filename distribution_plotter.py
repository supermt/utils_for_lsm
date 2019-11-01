import matplotlib.pyplot as plt

input = open("numbers","r")

numbers = input.readlines()
xs = []

for number in numbers:
    xs.append(int(10000 * float(number.replace("\n",""))))

xs.sort()
plt.plot(xs)
plt.show()