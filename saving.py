
import pandas as pd
import matplotlib.pyplot as plt

import os
import time

intro= """\
\\documentclass[a4paper]{article}

%% Language and font encodings
\\usepackage[english]{babel}
\\usepackage[utf8x]{inputenc}
\\usepackage[T1]{fontenc}

%% Sets page size and margins
\\usepackage[a4paper,top=3cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}

%% Useful packages
\\usepackage{amsmath}
\\usepackage{graphicx}
\\usepackage[colorinlistoftodos]{todonotes}
\\usepackage[colorlinks=true, allcolors=blue]{hyperref}


\\title{Your Paper}
\\author{You}

\\begin{document}
\\maketitle
\\newpage
"""



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




def writehdf5(dic,parameters,fig,fig1,fig2,localtime=""):
    if localtime=="":
        localtime = str(time.asctime( time.localtime(time.time())))
    datafile=localtime.replace(" ","")
    os.system("mkdir results/Plots/"+datafile)

    fig.savefig("results/Plots/"+datafile+"/IV.png")
    fig1.savefig("results/Plots/"+datafile+"/Cond.png")
    fig2.savefig("results/Plots/"+datafile+"/Resistance.png")

    hdf = pd.HDFStore("results/data/{0}.h5".format(localtime))
    data = pd.DataFrame(data=dic)
    hdf.put(value=data, key='df', format='table', data_columns=True)
    parametersdic={'Minimum_current':[parameters[0]],'Maximum_current':[parameters[1]],'Step_current':[parameters[2]], 'Amplitude_oscillation':[parameters[3]], 'Frequency_oscillation':[parameters[4]], 'Lengt_wire':[parameters[5]], 'Diameter_wire':[parameters[6]], 'Ac_Gain':[parameters[8]],'Dc_gain': [parameters[9]]}
    dp = pd.DataFrame(data=parametersdic)
    hdf.put(value=dp, key='dp', format='table', data_columns=True)
    hdf.close()
    return localtime

def readhdf5():
    hdf = pd.HDFStore("results/data.h5")
    return hdf['{0}'.format(input("Name of the dataframe to load within the file:"))]

def Latex():
    datafiles = os.listdir("results/data")


    with open('results/Log.tex','w') as log:
        log.write(intro)
        os.system("mkdir results/Plots/")
        for datafile in datafiles:
            print(datafile)



            # fig, ax= plt.subplots()
            # ax.grid(color='b', linestyle='--', linewidth=0.5)
            # fig.suptitle('V-I Plot', fontsize=10)
            # plt.ylabel('Voltage (V)')
            # plt.xlabel('Current (A)')
            # ax.errorbar(dic['I'], dic['V'], yerr=dic['eV'], color='b', fmt='o' ,capthick=2 )
            #
            # fig1, bx = plt.subplots()
            # fig1.suptitle('Differential conductance - Current Plot', fontsize=10)
            # plt.xlabel('Current (A)')
            # plt.ylabel('Dif Conductance (A/V)')
            # bx.grid(color='b', linestyle='--', linewidth=0.5)
            # bx.errorbar(dic['I'], dic['dC'], yerr=dic['edC'], color='r', fmt='o' ,capthick=2 )
            #
            #
            # fig2, cx = plt.subplots()
            # fig1.suptitle('Differential Resistance - Current Plot', fontsize=10)
            # plt.xlabel('Current (A)')
            # plt.ylabel('Dif Resistance (V/A)')
            # cx.grid(color='b', linestyle='--', linewidth=0.5)
            # cx.errorbar(dic['I'], dic['dR'], yerr=dic['edR'], color='g', fmt='o', capthick=2)

            print(datafile)
            try:
                hdf = pd.HDFStore("results/data/"+datafile)
                datafile = datafile[:-3].replace(" ","")
                parameters=hdf['dp']
                log.write("\\section{"+datafile+"}\n")
                os.system("clear")
                log.write("\\begin{figure}[h] \n\\centering \n")
                log.write("\\includegraphics[width=0.4\\textwidth]{Plots/"+datafile+"/IV.png}\n")
                log.write("\\includegraphics[width=0.4\\textwidth]{Plots/"+datafile+"/Cond.png}\n")
                log.write("\\includegraphics[width=0.4\\textwidth]{Plots/"+datafile+"/Resistance.png}\n")
                log.write("\\end{figure}\\\\\\\\\n\n")
                os.system("clear")
                log.write("All values are given in SI units\\\\ \n")
                for parameter in parameters.keys():
                    log.write(parameter+": $"+str(parameters[parameter][0])+"$\\\\ \n")
                log.write("File data stored in results/data/"+datafile+".h5")
                os.system("clear")
                hdf.close()
            except:
                log.write("\\section{"+datafile+"}\n")
                log.write("Data corrupt or format not expected. File should be checked manually.")



            log.write("\\newpage\n")
            os.system("clear")
            print(banner)
            print("Generating Latex class:")
            print(datafile +"Added")


        log.write("\\end{document}")

    os.system("clear")
    print("All data has been saved")

    return

Latex()
