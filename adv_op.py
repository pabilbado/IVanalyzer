from sr_operators import *
import maths_op
import time
import math
import multiprocessing as multi

def initial(sr830, source, channel=2, vo=0, amp=0.00005, freq=33, measuring=True):
    SetAux(sr830, channel, vo, measuring)
    Set_AC_source(source, amp, freq)
    print("Lock-in Amplifier set to initial conditions:\nAux{0}:{1} volts.\nAlternating current: {2}Hz and {3} volts.\n".format(channel, vo, freq, amp))
    return

def SetCond(sr830, channel, volt, amp, freq):
    SetAux(sr830,channel, volt)
    SetRef_Freq(sr830,freq)
    SetRef_Amp(sr830,amp)
    print("Lock-in Amplifier set to:\nAux{0}:{1} volts.\nAlternating current: {2}Hz and {3} volts.\n".format(channel, volt, freq, amp))
    return

def checkStat(sr830, i):
    print("Waiting for the Lock-In amplifier reading to stabilize")
    lmeasure = ReadCurrent(sr830, i)
    time.sleep(.5)
    measure = ReadCurrent(sr830, i)
    threshold=1e-5
    diff = diff=math.fabs(lmeasure-measure)
    while diff>threshold:
        lmeasure=measure
        time.sleep(.1)
        measure = ReadCurrent(sr830, i)
        diff=math.fabs(lmeasure-measure)
    return print("Lock-In {0} value stationary at {1}".format(i, measure))
