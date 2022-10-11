from modules.automatic.mainSysAuto import MainSysAuto
import time
import glob
import csv
import os
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
                    # ファイル全体を読込、改行ごとに分割
                    swapReadings = fOrigin.read().split('\n')

                    # マイセイノーの最後の行は改行のみ空行なので、これを避ける
                    for n in range(1, len(swapReadings) - 1): 
                        fSwap.write(swapReadings[n] + '\n')

        swapCsv = myseinoFulldir + '\swap.csv'

        with open(swapCsv ,'r') as fSwap:
            f = csv.reader(fSwap, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)

            for row in f:
                #rowはList
                #row[0]で必要な項目を取得することができる
                currentShipmentNo = row[4].strip()
                currentControlNo = row[26]

                if not currentControlNo in shipmentNoDics:
                    shipmentNoDics[currentControlNo] = currentShipmentNo

        # Webドライバーを介してログイン
        webd = self.myWebDriver.login()

        try:
            for key, value in shipmentNoDics.items():
                currentUrl = self.myWebDriver.jsonLoad['urlProductInfoDetal'] + key
                webd.get(currentUrl)
                time.sleep(4)
                # クリック：編集ボタン：編集可
                webd.find_element(By.XPATH, '/html/body/div[1]/div/div[1]/button[1]').click()
                # 入力：運送伝票番号
                webd.find_element(By.XPATH, '//*[@id="infoBean.shippingReportNo"]').clear()
                time.sleep(1)
                webd.find_element(By.XPATH, '//*[@id="infoBean.shippingReportNo"]').send_keys(value)
                # クリック：保存ボタン
                webd.find_element(By.XPATH, '//*[@id="cpbtnSave"]').click()
                time.sleep(6)

        except:
            self.myWebDriver.makeQueue(False)
            
        self.myWebDriver.makeQueue(True)
        os.remove(swapCsv)