
# Import packages needed:
import visa
import numpy as np
import sys
import warnings
import time
import matplotlib.pyplot as plt
import multiprocessing as multi
import os
import time
import pandas as pd


# Import our classes
from sr_operators import *
from adv_op import *
import measure
import maths_op
from Setup import *
import saving
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

os.system("clear")
print (banner)
 #Set up the Lock-in Amplifier
rm =visa.ResourceManager()
print("Looking for the Sr830 DSP Lock-In Amplifier")
try:
    i=0
    while True:
        sr830 = rm.open_resource(str(rm.list_resources()[i]))
        i+=1
        if 'Stanford_Research_Systems,' in sr830.query('*IDN?'):

            print('\nSr830 DSP Lock-In Amplifier found.')
            break
except:
    warnings.warn('No Sr830 DSP Lock-In Amplifier found.')
    sys.exit(0)

try:
    i=0
    while True:
        source = rm.open_resource(str(rm.list_resources()[i]))
        i+=1
        if 'Agilent Technologies' in source.query('*IDN?'):

            print('\nAgilent waveform generator found\n\nStarting measurements...')
            break
except:
    warnings.warn('No Sr830 DSP Lock-In Amplifier found.')
    sys.exit(0)


os.system("mkdir results")
os.system("mkdir results/data")
os.system("mkdir results/Plots/")
os.system("clear")
print(banner)



try:
    parameters = setup()
    measure.data_V_I(sr830, source, parameters)

except KeyboardInterrupt:
    sr830.clear()
    os.system("clear")
    print(banner)
    print("Script exited by user")





saving.Latex()
os.system("clear")
sr830.clear()
