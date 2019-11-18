import matplotlib.pyplot as plt

input = open("numbers","r")

numbers = input.readlines()
xs = []

for number in numbers:
    xs.append(int(10000 * float(number.replace("\n",""))))

xs.sort()

values = set()

for x in xs:
    values.add(x)
print(len(values))
print(len(xs))

plt.plot(list(values))
plt.show()