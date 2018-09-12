import pandas as pd
import os

def check0(I):
    for i in I:
        if i==0:
            return True
    return False



def shift():
    folders = os.listdir("../classifiedD")

    for folder in folders:
        files = os.listdir("../classifiedD/"+folder)
        for file in files:
            if ".h5" in file:

                hdf = pd.HDFStore("../classifiedD/"+folder+"/"+file)
                V = hdf['df']['V']
                I = hdf['df']['I']
                dR = hdf['df']['dR']
                k=0

                if check0(I):
                    for current in I:
                        if current==0:
                            break
                        k+=1
                    deltaV = (0-V[k])
                    deltaDR = (0-dR[k])
                else:
                    deltaV = 0
                    deltaDR = 0

                Vf = []
                for v in V:
                    Vf.append(v+deltaV)

                dRf =[]
                for r in dR:
                    dRf.append(r+deltaDR)

                data = hdf['df']
                data['V'] = Vf
                data['dR'] = dRf
                hdf.put(value = data, key = 'df', format='table', data_columns = True)



