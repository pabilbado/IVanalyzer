import time
import math
# Writing commands


def SetAux(sr830,channel,target, measuring =True):
    val = ReadVOut(sr830, channel)
    diff = abs(val-target)

    if measuring:
        while  val >target:
            sr830.write('AUXV{0},{1}'.format(channel, val-.001))
            val = ReadVOut(sr830, channel)
            if measuring:
                time.sleep(.05)

        while  val <target:
            sr830.write('AUXV{0},{1}'.format(channel, val+.001))
            val = ReadVOut(sr830, channel)
            if measuring:
                time.sleep(.05)

    else:
        sr830.write('AUXV{0},{1}'.format(channel,target))

    sr830.clear()

    return print("Voltage out {0} set to {1}V".format(channel, target))

def ChangeAux(sr830,channel,value):
    measure = sr830.query_ascii_values('AUXV?{0}'.format(channel))
    final = value+measure[0]
    return sr830.write('AUXV{0},{1}'.format(channel, final))

def SetRef_Freq(sr830,f):
    return sr830.write('FREQ{0}'.format(f))

def SetRef_Amp(sr830,A):
    return sr830.write('SLVL{0}'.format(A))

def ChangeRef_Freq(sr830,df):
    measure = sr830.query_ascii_values('FREQ?')
    final = df+measure[0]
    return sr830.write('FREQ{0}'.format(final))

def ChangeRef_Amp(sr830,dA):
    measure = sr830.query_ascii_values('SLVL?')
    final = dA+measure[0]
    return sr830.write('SLVL{0}'.format(final))


# Reading commands

def ReadFreq(sr830):
    return  sr830.query_ascii_values('FREQ?')[0]

def ReadAmp(sr830):
    return sr830.query_ascii_values('SLVL?')[0]
# #Voltage measurement mode
def Read_Current_Amp(sr830):
    return (sr830.query_ascii_values('SLVL?')/1e3)[0]

def ReadVOut(sr830, channel):
    while True:
        try:
            return sr830.query_ascii_values('AUXV?{0}'.format(channel))[0]
        except KeyboardInterrupt:
            raise ValueError('KeyboardInterrupt')
        except:
            print("An error occured wait while it is being solved")
            sr830.clear()
            time.sleep(1)
            print("Error solved dw")

def Read_Current_Out(sr830, channel):
    return (sr830.query_ascii_values('AUXV?{0}'.format(channel))/1e3)[0]

def ReadVin(sr830, channel):
    return sr830.query_ascii_values('OAUX?{0}'.format(channel))[0]

def ReadCurrent(sr830, port):
    while True:
        try:
            return sr830.query_ascii_values('OUTP?{0}'.format(port))[0]
        except KeyboardInterrupt:
            raise ValueError('KeyboardInterrupt')
        except:
            print("An error occured wait while it is being solved")
            sr830.clear()
            time.sleep(1)
            print("Error solved dw")

def Read_noise(sr830):
    pdisplay = int(sr830.query_ascii_values('DDEF?{0}'.format(1))[0])
    pydisplay = int(sr830.query_ascii_values('DDEF?{0}'.format(2))[0])
    sr830.write('DDEF{0},2,0'.format(1))
    sr830.write('DDEF{0},2,0'.format(2))
    noisex = sr830.query_ascii_values('OUTR?{0}'.format(1))[0]/100
    noisey = sr830.query_ascii_values('OUTR?{0}'.format(2))[0]/100
    while pdisplay != int(sr830.query_ascii_values('DDEF?{0}'.format(1))[0]):
        sr830.write('DDEF{0},{1},0'.format(1,pdisplay))
    while pydisplay != int(sr830.query_ascii_values('DDEF?{0}'.format(2))[0]):
        sr830.write('DDEF{0},{1},0'.format(2,pydisplay))
    x=ReadCurrent(sr830,1)
    y=ReadCurrent(sr830,2)
    noise=math.sqrt(math.pow(x*noisex,2)+math.pow(y*noisey,2))
    sr830.clear()
    return noise

# Writing commands
def Set_AC_source(source, amp, freq):
    ampo=amp*1e3
    return source.write("APPL:SIN {0}, {1} VRMS, 0".format(freq,ampo))

def Get_Amp_source(source):
    return source.query_ascii_values("VOLT?")[0]/1e3
