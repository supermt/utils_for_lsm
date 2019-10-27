#!/usr/bin/python

f = open("/tmp/dbdump", "w")

for i in range(1000000):
    f.write("a" + str(i) + " ==> " + "value" + str(i) + "\n")

f.write("Keys in range: "+str(i+1)+"\n")

f.close()
