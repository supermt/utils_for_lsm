#!/usr/bin/env python
""" generated source for module ZipfianGenerator """
from __future__ import print_function
from functools import wraps
from threading import RLock

def lock_for_object(obj, locks={}):
    return locks.setdefault(id(obj), RLock())

def synchronized(call):
    assert call.__code__.co_varnames[0] in ['self', 'cls']
    @wraps(call)
    def inner(*args, **kwds):
        with lock_for_object(args[0]):
            return call(*args, **kwds)
    return inner

#                                                                                                                                                                                 
#  * Copyright (c) 2010 Yahoo! Inc. All rights reserved.                                                                                                                             
#  *                                                                                                                                                                                 
#  * Licensed under the Apache License, Version 2.0 (the "License"); you                                                                                                             
#  * may not use this file except in compliance with the License. You                                                                                                                
#  * may obtain a copy of the License at                                                                                                                                             
#  *                                                                                                                                                                                 
#  * http://www.apache.org/licenses/LICENSE-2.0                                                                                                                                      
#  *                                                                                                                                                                                 
#  * Unless required by applicable law or agreed to in writing, software                                                                                                             
#  * distributed under the License is distributed on an "AS IS" BASIS,                                                                                                               
#  * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or                                                                                                                 
#  * implied. See the License for the specific language governing                                                                                                                    
#  * permissions and limitations under the License. See accompanying                                                                                                                 
#  * LICENSE file.                                                                                                                                                                   
#  
# 
#  * A generator of a zipfian distribution. It produces a sequence of items, such that some items are more popular than others, according
#  * to a zipfian distribution. When you construct an instance of this class, you specify the number of items in the set to draw from, either
#  * by specifying an itemcount (so that the sequence is of items from 0 to itemcount-1) or by specifying a min and a max (so that the sequence is of 
#  * items from min to max inclusive). After you construct the instance, you can change the number of items by calling nextInt(itemcount) or nextLong(itemcount).
#  * 
#  * Note that the popular items will be clustered together, e.g. item 0 is the most popular, item 1 the second most popular, and so on (or min is the most 
#  * popular, min+1 the next most popular, etc.) If you don't want this clustering, and instead want the popular items scattered throughout the 
#  * item space, then use ScrambledZipfianGenerator instead.
#  * 
#  * Be aware: initializing this generator may take a long time if there are lots of items to choose from (e.g. over a minute
#  * for 100 million objects). This is because certain mathematical values need to be computed to properly generate a zipfian skew, and one of those
#  * values (zeta) is a sum sequence from 1 to n, where n is the itemcount. Note that if you increase the number of items in the set, we can compute
#  * a new zeta incrementally, so it should be fast unless you have added millions of items. However, if you decrease the number of items, we recompute
#  * zeta from scratch, so this can take a long time. 
#  *
#  * The algorithm used here is from "Quickly Generating Billion-Record Synthetic Databases", Jim Gray et al, SIGMOD 1994.
#  
class ZipfianGenerator(object):
    """ generated source for class ZipfianGenerator """
    ZIPFIAN_CONSTANT = 0.99

    # 
    # 	 * Number of items.
    # 	 
    items = long()
    random = Random()

    # 
    # 	 * Min item to generate.
    # 	 
    base = long()

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
    countforzeta = long()
    lastVal = None

    def setLastValue(self, last):
        """ generated source for method setLastValue """
        self.lastVal = last

    def lastValue(self):
        """ generated source for method lastValue """
        return self.lastVal

    # 
    # 	 * Flag to prevent problems. If you increase the number of items the zipfian generator is allowed to choose from, this code will incrementally compute a new zeta
    # 	 * value for the larger itemcount. However, if you decrease the number of items, the code computes zeta from scratch; this is expensive for large itemsets.
    # 	 * Usually this is not intentional; e.g. one thread thinks the number of items is 1001 and calls "nextLong()" with that item count; then another thread who thinks the 
    # 	 * number of items is 1000 calls nextLong() with itemcount=1000 triggering the expensive recomputation. (It is expensive for 100 million items, not really for 1000 items.) Why
    # 	 * did the second thread think there were only 1000 items? maybe it read the item count before the first thread incremented it. So this flag allows you to say if you really do
    # 	 * want that recomputation. If true, then the code will recompute zeta if the itemcount goes down. If false, the code will assume itemcount only goes up, and never recompute. 
    # 	 
    allowitemcountdecrease = False

    #  Constructors 
    # 
    # 	 * Create a zipfian generator for the specified number of items.
    # 	 * @param _items The number of items in the distribution.
    # 	 
    @overloaded
    def __init__(self, _items):
        """ generated source for method __init__ """
        self.__init__(0, _items - 1)

    # 
    # 	 * Create a zipfian generator for items between min and max.
    # 	 * @param _min The smallest integer to generate in the sequence.
    # 	 * @param _max The largest integer to generate in the sequence.
    # 	 
    @__init__.register(object, long, long)
    def __init___0(self, _min, _max):
        """ generated source for method __init___0 """
        self.__init__(_min, _max, self.ZIPFIAN_CONSTANT)

    # 
    # 	 * Create a zipfian generator for the specified number of items using the specified zipfian constant.
    # 	 * 
    # 	 * @param _items The number of items in the distribution.
    # 	 * @param _zipfianconstant The zipfian constant to use.
    # 	 
    @__init__.register(object, long, float)
    def __init___1(self, _items, _zipfianconstant):
        """ generated source for method __init___1 """
        self.__init__(0, _items - 1, _zipfianconstant)

    # 
    # 	 * Create a zipfian generator for items between min and max (inclusive) for the specified zipfian constant.
    # 	 * @param min The smallest integer to generate in the sequence.
    # 	 * @param max The largest integer to generate in the sequence.
    # 	 * @param _zipfianconstant The zipfian constant to use.
    # 	 
    @__init__.register(object, long, long, float)
    def __init___2(self, min, max, _zipfianconstant):
        """ generated source for method __init___2 """
        self.__init__(min, max, _zipfianconstant, zetastatic(max - min + 1, _zipfianconstant))

    # 
    # 	 * Create a zipfian generator for items between min and max (inclusive) for the specified zipfian constant, using the precomputed value of zeta.
    # 	 * 
    # 	 * @param min The smallest integer to generate in the sequence.
    # 	 * @param max The largest integer to generate in the sequence.
    # 	 * @param _zipfianconstant The zipfian constant to use.
    # 	 * @param _zetan The precomputed zeta constant.
    # 	 
    @__init__.register(object, long, long, float, float)
    def __init___3(self, min, max, _zipfianconstant, _zetan):
        """ generated source for method __init___3 """
        self.items = max - min + 1
        self.base = min
        self.zipfianconstant = _zipfianconstant
        self.theta = self.zipfianconstant
        self.zeta2theta = zeta(2, self.theta)
        self.alpha = 1.0 / (1.0 - self.theta)
        # zetan=zeta(items,theta);
        self.zetan = _zetan
        self.countforzeta = self.items
        self.eta = (1 - pow(2.0 / self.items, 1 - self.theta)) / (1 - self.zeta2theta / self.zetan)
        # print("XXXX 3 XXXX");
        nextValue()
        # print("XXXX 4 XXXX");

    # /
    # 
    # 	 * Compute the zeta constant needed for the distribution. Do this from scratch for a distribution with n items, using the 
    # 	 * zipfian constant theta. Remember the value of n, so if we change the itemcount, we can recompute zeta.
    # 	 * 
    # 	 * @param n The number of items to compute zeta over.
    # 	 * @param theta The zipfian constant.
    # 	 
    @overloaded
    def zeta(self, n, theta):
        """ generated source for method zeta """
        self.countforzeta = n
        return zetastatic(n, theta)

    # 
    # 	 * Compute the zeta constant needed for the distribution. Do this from scratch for a distribution with n items, using the 
    # 	 * zipfian constant theta. This is a static version of the function which will not remember n.
    # 	 * @param n The number of items to compute zeta over.
    # 	 * @param theta The zipfian constant.
    # 	 
    @classmethod
    @overloaded
    def zetastatic(cls, n, theta):
        """ generated source for method zetastatic """
        return cls.zetastatic(0, n, theta, 0)

    # 
    # 	 * Compute the zeta constant needed for the distribution. Do this incrementally for a distribution that
    # 	 * has n items now but used to have st items. Use the zipfian constant theta. Remember the new value of 
    # 	 * n so that if we change the itemcount, we'll know to recompute zeta.
    # 	 * 
    # 	 * @param st The number of items used to compute the last initialsum
    # 	 * @param n The number of items to compute zeta over.
    # 	 * @param theta The zipfian constant.
    #      * @param initialsum The value of zeta we are computing incrementally from.
    # 	 
    @zeta.register(object, long, long, float, float)
    def zeta_0(self, st, n, theta, initialsum):
        """ generated source for method zeta_0 """
        self.countforzeta = n
        return self.zetastatic(st, n, theta, initialsum)

    # 
    # 	 * Compute the zeta constant needed for the distribution. Do this incrementally for a distribution that
    # 	 * has n items now but used to have st items. Use the zipfian constant theta. Remember the new value of 
    # 	 * n so that if we change the itemcount, we'll know to recompute zeta. 
    # 	 * @param st The number of items used to compute the last initialsum
    # 	 * @param n The number of items to compute zeta over.
    # 	 * @param theta The zipfian constant.
    #      * @param initialsum The value of zeta we are computing incrementally from.
    # 	 
    @classmethod
    @zetastatic.register(object, long, long, float, float)
    def zetastatic_0(cls, st, n, theta, initialsum):
        """ generated source for method zetastatic_0 """
        sum = initialsum
        i = st
        while i < n:
            sum += 1 / (pow(i + 1, theta))
            i += 1
        # print("countforzeta="+countforzeta);
        return sum

    # /
    # 
    # 	 * Generate the next item as a long.
    # 	 * 
    # 	 * @param itemcount The number of items in the distribution.
    # 	 * @return The next item in the sequence.
    # 	 
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
        u = ZipfianGenerator.random.nextFloat()
        uz = u * self.zetan
        if uz < 1.0:
            return self.base
        if uz < 1.0 + pow(0.5, self.theta):
            return self.base + 1
        ret = self.base + long(((itemcount) * pow(self.eta * u - self.eta + 1, self.alpha)))
        self.setLastValue(ret)
        return ret

    # 
    # 	 * Return the next value, skewed by the Zipfian distribution. The 0th item will be the most popular, followed by the 1st, followed
    # 	 * by the 2nd, etc. (Or, if min != 0, the min-th item is the most popular, the min+1th item the next most popular, etc.) If you want the
    # 	 * popular items scattered throughout the item space, use ScrambledZipfianGenerator instead.
    # 	 
    def nextValue(self):
        """ generated source for method nextValue """
        return self.nextLong(self.items)

    @classmethod
    def main(cls, args):
        """ generated source for method main """
        ZipfianGenerator(100)

    @classmethod
    def next(cls):
        """ generated source for method next """
        return 1


if __name__ == '__main__':
    import sys
    ZipfianGenerator.main(sys.argv)

