import pandas as pd
import os


def excel():
    folders = os.listdir("classifiedD")
    for folder in folders:
        files = os.listdir("classifiedD/"+folder)
        print(folder)
        for file in files:
            if ".h5" in file:
                print(file)
                hdf = pd.HDFStore("classifiedD/"+folder+"/"+file)
                excel = pd.ExcelWriter("classifiedD/"+folder+"/"+file[:-3]+".xlsx")
                hdf['df'].to_excel(excel, 'Sheet1')
                hdf['dp'].to_excel(excel,'Sheet2')
                excel.save()
        os.system("clear")
