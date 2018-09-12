import sys
def setup():

    initial=2
    final=0
    C_step= abs(final-initial)/100
    C_osc=0.003
    Freq=133
    Length=0.45
    Diameter=58.6e-6
    Gain_Ac = 1000
    Gain_Dc = -1


    if initial > final:
        reverse =True
    else:
        reverse = False


    question="Do you want to run a default run?[Y/n]\n Initial current: {0}A\nFinal current: {1}A\nCurrent step: {2}A\nCurrent oscillation:{3}A\nFrequency of the oscillation: {4}Hz\nLength of wire: {5}\nDiameter of wire: {6} \nGain AC: {7}X\nGain DC: {8}X".format(initial,final,C_step,C_osc,Freq,Length,Diameter, Gain_Ac, Gain_Dc)
    if input(question)!="n":
        return[initial,final,C_step,C_osc,Freq,Length,Diameter, reverse, Gain_Ac, Gain_Dc]
    else:
        sys.exit(0)
    return parameters
