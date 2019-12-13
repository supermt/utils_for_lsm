#!/usr/bin/env python3
""" generated source for module ZipfianGenerator """
from __future__ import print_function
from functools import wraps
from threading import RLock
import random

def lock_for_object(obj, locks={}):
    return locks.setdefault(id(obj), RLock())

def synchronized(call):
    assert call.__code__.co_varnames[0] in ['self', 'cls']
    @wraps(call)
    def inner(*args, **kwds):
        with lock_for_object(args[0]):
            return call(*args, **kwds)
    return inner

ZIPFIAN_CONSTANT = 0.99

def zetastatic(n, theta,st=0, initialsum=0):
    """ generated source for method zetastatic_0 """
    sum = initialsum
    i = st
    while i < n:
        sum += 1 / (pow(i + 1, theta))
        i += 1
    # print("countforzeta="+countforzeta);
    return sum

class ZipfianGenerator(object):

    # 
    # 	 * Number of items.
    # 	 
    items = int()
    # 
    # 	 * Min item to generate.
    # 	 
    base = int()

    # 
    # 	 * The zipfian constant to use.
    # 	 
    zipfianconstant = float()

    # 
    # 	 * Computed parameters for generating the distribution.
    # 	 
    alpha = float()
    zetan = float()
    eta = float()
    theta = float()
    zeta2theta = float()

    # 
    # 	 * The number of items used to compute zetan the last time.
    # 	 
    countforzeta = int()
    lastVal = None

    def setLastValue(self, last):
        """ generated source for method setLastValue """
        self.lastVal = last

    def lastValue(self):
        """ generated source for method lastValue """
        return self.lastVal

    allowitemcountdecrease = False

    def nextLong(self, itemcount):
        """ generated source for method nextLong """
        # from "Quickly Generating Billion-Record Synthetic Databases", Jim Gray et al, SIGMOD 1994
        if itemcount != self.countforzeta:
            # have to recompute zetan and eta, since they depend on itemcount
            with lock_for_object(self):
                if itemcount > self.countforzeta:
                    # System.err.println("WARNING: Incrementally recomputing Zipfian distribtion. (itemcount="+itemcount+" countforzeta="+countforzeta+")");
                    # we have added more items. can compute zetan incrementally, which is cheaper
                    self.zetan = self.zeta(self.countforzeta, itemcount, self.theta, self.zetan)
                    self.eta = (1 - pow(2.0 / self.items, 1 - self.theta)) / (1 - self.zeta2theta / self.zetan)
                elif (itemcount < self.countforzeta) and (self.allowitemcountdecrease):
                    # have to start over with zetan
                    # note : for large itemsets, this is very slow. so don't do it!
                    # TODO: can also have a negative incremental computation, e.g. if you decrease the number of items, then just subtract
                    # the zeta sequence terms for the items that went away. This would be faster than recomputing from scratch when the number of items
                    # decreases
                    System.err.println("WARNING: Recomputing Zipfian distribtion. This is slow and should be avoided. (itemcount=" + itemcount + " countforzeta=" + self.countforzeta + ")")
                    self.zetan = self.zeta(itemcount, self.theta)
                    self.eta = (1 - pow(2.0 / self.items, 1 - self.theta)) / (1 - self.zeta2theta / self.zetan)
        u = random.random()
        uz = u * self.zetan
        if uz < 1.0:
            return self.base
        if uz < 1.0 + pow(0.5, self.theta):
            return self.base + 1
        ret = self.base + int(((itemcount) * pow(self.eta * u - self.eta + 1, self.alpha)))
        self.setLastValue(ret)
        return ret

    def nextValue(self):
        """ generated source for method nextValue """
        return self.nextLong(self.items)


    def zeta(self, n, theta, st=0, initialsum=0):
        """ generated source for method zeta_0 """
        self.countforzeta = n
        return zetastatic(st, n, theta, initialsum)
    
    def __init__(self, _max, item_count=1000, _min=0 , _zipfianconstant=ZIPFIAN_CONSTANT):
        _zetan=zetastatic(_max - _min + 1, _zipfianconstant)
        """ generated source for method __init___3 """
        self.items = item_count
        self.base = _min
        self.zipfianconstant = _zipfianconstant
        self.theta = self.zipfianconstant
        self.zeta2theta = self.zeta(2, self.theta)
        self.alpha = 1.0 / (1.0 - self.theta)
        # zetan=zeta(items,theta);
        self.zetan = _zetan
        self.countforzeta = self.items
        self.eta = (1 - pow(2.0 / self.items, 1 - self.theta)) / (1 - self.zeta2theta / self.zetan)
        # print("XXXX 3 XXXX");
        self.nextValue()
        # print("XXXX 4 XXXX");

    def next(self):
        """ generated source for method next """
        return 1


def generate_zipfian(item_count,zipfian_alpha=ZIPFIAN_CONSTANT,start_point=0,end_point=0):
    if end_point == 0:
        end_point = start_point + item_count
    result_list=[]
    zip_g = ZipfianGenerator(item_count=item_count,_max=end_point,_min=start_point,_zipfianconstant=zipfian_alpha)
    for i in range(0,item_count):
        result_list.append(zip_g.nextValue())
    return result_list

if __name__ == '__main__':
    print(generate_zipfian(30000))
