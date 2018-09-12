from sr_operators import *
from adv_op import *
import multiprocessing as multi
import math
import numpy as np

def Maxs(alist):
    maxs=[]
    i=1
    if len(alist)<10:
        return [0]

    while True:
        if (alist[i]>alist[i-1]) & (alist[i+1]<alist[i]):
            maxs.append(alist[i])
        i+=1
        if i>= (len(alist)-1):
            break

    if maxs==[]:
        return [0]

    maxs.sort(reverse=True)
    return maxs

def Mins(alist):
    mins=[]
    i=1
    if len(alist)<10:
        return [0]

    while True:
        if (alist[i]<alist[i-1]) & (alist[i+1]>alist[i]):
            mins.append(alist[i])
        i+=1
        if i>= (len(alist)-1):
            break

    if mins==[]:
        return [0]

    mins.sort()
    return mins


def averageMax(alist):
    l=Maxs(alist)
    s = 0.
    n = 0.
    for i in l:
        s+=i
        n+=1
    return (s/n)

def averageMin(alist):
    l=Mins(alist)
    s = 0.
    n = 0.
    for i in l:
        s+=i
        n+=1
    return (s/n)


def average(alist):
    s=0.
    n=0.
    for i in alist:
        s+=i
        n+=1
    return (s/n)


def standardError(st, mean):
    s=0
    n =len(st)
    for i in st:
        s+=(i-mean)*(i-mean)
    dev = s/(n-1)
    return math.sqrt(dev/n)


def best_slop(xs, ys):
    x = np.array(xs, dtype = np.float64)
    y = np.array(ys, dtype = np.float64)
    slope = ( ((average(x)*average(y)) - (average(x*y) )) /
    (math.pow(average(x),2) - (average(x*x))) )
    return slope
