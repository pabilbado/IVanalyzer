
import visa
import numpy as np
import sys
import warnings
import time
import matplotlib.pyplot as plt

import pickle
import os

from sr_operators import *
from adv_op import *
import maths_op
import saving
from Agilent_operators import *


banner= """\
       ___                                     _   ___      _    _
      / __|___ ___ _ _ __ _ ___   __ _ _ _  __| | | _ \__ _| |__| |___ ___
     | (_ / -_) _ \ '_/ _` / -_) / _` | ' \/ _` | |  _/ _` | '_ \ / _ (_-<
      \___\___\___/_| \__, \___| \__,_|_||_\__,_| |_| \__,_|_.__/_\___/__/
                      |___/
                                ___         _
                               / __|___  __| |___
                              | (__/ _ \/ _` / -_)
                               \___\___/\__,_\___|

###################################################################################
"""
exit= """\
 ____,___,_______,____
/  :::|///./||'||     |
|  :::|//.//|| || H)  |
|  :::|/.///|!!!|     |
|   _______________   |
|  |:::::::::::::::|  |
|  |_______________|  |
|  |_______________|  |
|  |_______________|  |
|  |_______________|  |
||_|     Saved     ||_|
|__|_______________|__|
"""






def Current_list(minimun,maximum,step, reverse):

    c = 1.74195#ratio between input voltage and curent output
    b=2.565e-2

    if reverse:
        C_F = minimun
        C_0 = maximum
    else:
        C_F= maximum
        C_0= minimun



    c_list = []
    k=0
    while True:
        a = k*step + C_0
        k+=1
        if a > C_F:
            break
        c_list.append(a)

    volt_list=[]
    for I in c_list:
        volt_list.append(I*c +b)
    if reverse:
        c_list.reverse()
        volt_list.reverse()

    return [volt_list, c_list]



#This is for a the voltage characteritic measurement set up.
def data_V_I(sr830, source, parameters):
    data ={'V':[],'dV':[], 'eV':[], 'edV':[], 'I':[], 'dI':[], 'dC':[], 'edC':[], 'dR':[], 'edR':[]}

    measureI, Ilist = Current_list(parameters[0],parameters[1],parameters[2],parameters[7])
    # xe=abs((Ilist[-1]-Ilist[-2]))*0.01
    xe = 0.0001
    initial(sr830, source ,vo=measureI[0], channel = 2, amp=parameters[3], freq = parameters[4])
    c = 0.585316544#ratio between input voltage and curent output

    plt.ion()
    fig, ax= plt.subplots()
    ax.grid(color='b', linestyle='--', linewidth=0.5)
    fig.suptitle('V-I Plot', fontsize=10)
    plt.ylabel('Voltage (V)')
    plt.xlabel('Current (A)')

    fig1, bx = plt.subplots()
    fig1.suptitle('Differential conductance - Current Plot', fontsize=10)
    plt.xlabel('Current (A)')
    plt.ylabel('Dif Conductance (A/V)')
    bx.grid(color='b', linestyle='--', linewidth=0.5)

    fig2, cx = plt.subplots()
    fig2.suptitle('Differential Resistance - Current Plot', fontsize=10)
    plt.xlabel('Current (A)')
    plt.ylabel('Dif Resistance (V/A)')
    cx.grid(color='b', linestyle='--', linewidth=0.5)

    i =0
    try:
        localtime=""
        for V in measureI:
            print("Setting the current to {0}A ".format((Ilist[i])))
            SetAux(sr830, 2, V)
            checkStat(sr830, 1)
            print("Performing measurement at that point")
            d=Voltage_measured(sr830)
            data['dI'].append(Get_Amp_source(source))
            data['I'].append(Ilist[i])
            data['V'].append(d[1]/parameters[9])
            data['dV'].append(d[0]/parameters[8])
            data['eV'].append(d[2]/parameters[9])
            data['edV'].append(Read_noise(sr830)*data['dV'][-1])
            if data['dV'][-1] ==0:
                data['dC'].append(0)
                data['edC'].append(0)
                bx.errorbar(data['I'][i], data['dC'][-1], yerr=data['edC'][-1] , xerr=xe , color='y', fmt='o' ,capthick=2 )
            else:
                data['dC'].append(data['dI'][-1]/data['dV'][-1])
                data['edC'].append(data['dC'][-1]*math.sqrt(math.pow(0.000001/data['dV'][-1],2)+math.pow((data['dI'][-1]/(d[0]))*data['edV'][-1],2)))
                bx.errorbar(data['I'][i], data['dC'][-1], yerr=data['edC'][-1] , xerr=xe , color='r', fmt='o' ,capthick=2 )

            data['dR'].append(data['dV'][-1]/data['dI'][-1])
            try:
                data['edR'].append(data['dR'][-1]*math.sqrt(math.pow(data['edV'][-1]/data['dI'],2)+math.pow(data['dR'][-1]*1e-6,2)))
            except:
                data['edR'].append(0)
            os.system('clear')
            print(banner)
            print("Measurement taken:\n  {0}I at {1}V".format(data['I'][-1],data['V'][-1]))
            ax.errorbar(data['I'][i], data['V'][-1], yerr=data['eV'][-1], xerr=xe , color='b', fmt='o' ,capthick=2 )
            cx.errorbar(data['I'][i], data['dR'][-1], yerr=data['edR'][-1], xerr=xe, color='g', fmt='o', capthick=2)
            fig1.canvas.draw()
            fig.canvas.draw()
            fig2.canvas.draw()

            if localtime=="":
                localtime = saving.writehdf5(data,parameters,fig,fig1,fig2)
            else:
                saving.writehdf5(data,parameters,fig,fig1,fig2,localtime)
            i+=1


        print("Slope of the VI graph is {0} V/A".format(maths_op.best_slop(data['I'],data['V'])))
        print("The average of the conductance is {0}".format(maths_op.average(data['dC'])))
        print("The average of the resistance is {0}".format(maths_op.average(data['dR'])))
        input("Final Results (press enter to continue)")

    except KeyboardInterrupt:
        os.system("clear")
        print(banner)
        print("User interrupted the measurements")


    saving.writehdf5(data,parameters, fig, fig1,fig2, localtime)
    print(exit)
    initial(sr830, source ,vo=0, channel = 2, amp=parameters[3], freq = parameters[4], measuring =False)

    return data


def Voltage_measured(sr830):
    measurement=[]
    measurement2=[]
    while True:
        measurement.append(ReadCurrent(sr830,3))
        measurement2.append(ReadVin(sr830,1))
        if len(measurement)>= 100:
            break


    dv = maths_op.average(measurement)
    v = maths_op.average(measurement2)
    ev= maths_op.standardError(measurement2,v)

    return [dv, v,ev]
