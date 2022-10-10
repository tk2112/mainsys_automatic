from modules.automatic.mainSysAuto import MainSysAuto
import time
import glob
import csv
import modules.const as const
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

const.MYSEINO_DIR = '\myseino'

class ShipmentNo(MainSysAuto):
    
    def set(self):
        myseinoFulldir = ''
        shipmentNoDics = {}
        
        if len(self.myWebDriver.currentDir) > 0:
            myseinoFulldir = self.myWebDriver.currentDir + const.MYSEINO_DIR

        fileList = glob.glob(myseinoFulldir + "/*.wbp")

        with open(myseinoFulldir + '\swap.csv' ,'w+') as fSwap:

            for file in fileList:
                with open(file, 'r') as fOrigin:
                    swapReadings = fOrigin.read().split('\n') # ファイル全体を読込、改行ごとに分割

                    for n in range(1, len(swapReadings) - 1): # マイセイノーの最後の行は改行のみ空行なので、これを避ける
                        fSwap.write(swapReadings[n] + '\n')

        with open(myseinoFulldir + '\swap.csv' ,'r') as fSwap:
            f = csv.reader(fSwap, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)

            for row in f:
                #rowはList
                #row[0]で必要な項目を取得することができる
                currentShipmentNo = row[4].strip()
                currentControlNo = row[26]

                if not currentControlNo in shipmentNoDics:
                    shipmentNoDics[currentControlNo] = currentShipmentNo