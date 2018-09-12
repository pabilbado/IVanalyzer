import pandas as pd
import math
import matplotlib.pyplot as  plt
import os
import numpy as np
import math

from excel import excel
from shift import *

def r_squared(xs, ys):
    mean_y = average(ys)
    a=0
    b=0
    for y, x in zip(ys, xs):
        a+=math.pow(y,2)
        b+=math.pow(y-mean_y,2)
    print(1-a/b)
    return 1-(a/b)

def best_slop(xs, ys):
    y = np.array(ys, dtype=np.float64)
    x = np.array(xs, dtype=np.float64)
    slope = ( ((average(x)*average(y)) - (average(x*y) )) /
    (math.pow(average(x),2) - (average(x*x))) )
    return slope


def average(lists):
    k=0
    sum =0
    for value in lists:
        sum +=value
        k+=1
    return sum/k




def findSCurr(data):
    dR = data['dR'].tolist()
    I = data['I'].tolist()
    if I[0]>I[-1]:
        dR =dR[::-1]
        I = I[::-1]
    x=10
    while True:
        dRy = dR[:x]
        Ix = I[:x]
        slope = best_slop(Ix, dRy)
        if x >= (len(I)-1):
            return 0
        if slope >0.0001:
            return I[(x-1)]
        x+=1

def orderDia():
    files = os.listdir("results/data")
    os.system("mkdir classifiedD")
    for file in files:
        if "h5" in file:
            name = file.replace(" ", "\ ")
            hdf = pd.HDFStore("results/data/"+file)
            print(file)
            try:
                data = hdf['df']
                param = hdf['dp']
                try:
                    dia = str(param [param.keys()[6]] [0])[2:]
                except:
                    dia = "not_defined"
                os.system("mkdir classifiedD/"+dia)
                new = pd.HDFStore("classifiedD/" + dia+"/"+str(file)[8:])
                new.put(value = data, key = 'df', format='table', data_columns = True)
                new.put(value = param, key ='dp', format = 'table', data_columns = True)
                hdf.close()
                new.close()
            except:
                try:
                    data = hdf[str(hdf.keys()[0])]
                    param = hdf[str(hdf.keys()[1])]
                    dia = str(param [param.keys()[6]] [0])[2:]
                    os.system("mkdir classifiedD/"+dia)
                    new = pd.HDFStore("classifiedD/" + dia+"/"+str(name)[8:])
                    new.put(value = data, key = 'df', format='table', data_columns = True)
                    new.put(value = param, key ='dp', format = 'table', data_columns = True)
                    hdf.close()
                    new.close()
                except:
                    pass


def findSCurrI(data):
    dR = data['dR'].tolist()
    I = data['I'].tolist()
    if I[0]>I[-1]:
        dR =dR[::-1]
        I = I[::-1]
    prevS =0
    x=10
    while True:
        dRy = dR[:x]
        Ix = I[:x]
        slope = best_slop(Ix, dRy)
        if prevS==0:
            prevS=slope
        if abs(slope-prevS) >abs(2*prevS):
            plt.scatter(Ix,Vy, color = 'r')
            plt.scatter(I[x:], V[x:], color = 'b')
            plt.show()
            return I[x]
        if x %2 ==0:
            prevS=slope
        if x >= (len(I)-1):
            return 0
        x+=1


def addScurr(scurr, file):
    param = file['dp']
    param['Scurrent']=[scurr]
    file.put(value=param, key='dp', format='table', data_columns=True)

def all():
    folders = os.listdir("classifiedD")
    for folder in folders:
        files = os.listdir("classifiedD/"+folder)
        print(folder)
        for file in files:
            if ".h5" in file:
                print(file)
                hdf=pd.HDFStore("classifiedD/"+folder+"/"+file)
                data = hdf['df']
                scurr = findSCurr(data)
                addScurr(scurr,hdf)
                hdf.close()


def plots():
    folders = os.listdir("classifiedD")
    os.system("mkdir plots")
    for folder in folders:
        files = os.listdir("classifiedD/"+folder)
        os.system("mkdir plots/"+folder)
        for file in files:
            if ".h5" in file:
                hdf = pd.HDFStore("classifiedD/"+folder+"/"+file)
                dic = hdf['df']
                param = hdf['dp']

                fig, ax= plt.subplots()
                ax.grid(color='b', linestyle='--', linewidth=0.5)
                fig.suptitle('V-I Plot', fontsize=10)
                plt.ylabel('Voltage (V)')
                plt.xlabel('Current (A)')


                fig2, cx = plt.subplots()
                fig2.suptitle('Differential Resistance - Current Plot', fontsize=10)
                plt.xlabel('Current (A)')
                plt.ylabel('Dif Resistance (V/A)')
                cx.grid(color='b', linestyle='--', linewidth=0.5)


                for k in range(len(dic['I'])):
                    if dic['I'][k]<param['Scurrent'][0]:
                        ax.scatter(dic['I'][k], dic['V'][k], color='r')
                        cx.scatter(dic['I'][k], dic['dR'][k], color='r')
                    else:
                        ax.scatter(dic['I'][k], dic['V'][k], color='b')
                        cx.scatter(dic['I'][k], dic['dR'][k], color='b')

                fig.savefig("plots/"+folder+"/"+file[:-3]+"IV.png")
                fig2.savefig("plots/"+folder+"/"+file[:-3]+"R.png")

def moveFolder():
    os.system("mkdir data")
    os.system("mv /results/data/* /data")



orderDia()
shift()
all()
excel()
plots()
