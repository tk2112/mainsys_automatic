from modules.automatic.mainSysAuto import MainSysAuto
import time
import glob
import csv
import os
import datetime
import shutil
import re
import modules.const as const
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

const.MYSEINO_DIR = r'\myseino'

class ShipmentNo(MainSysAuto):
    def __init__(self, myWebDriver):
        super().__init__(myWebDriver)

        self.__myseinoFulldir = ''

        if len(self.myWebDriver.currentDir) > 0:
            self.__myseinoFulldir = self.myWebDriver.currentDir + const.MYSEINO_DIR

        self.__today = datetime.date.today()
        self.__bkMyseinoDir = self.__myseinoFulldir  + '\\bk\\'
        self.__bkMyseinoDirCurrentDay = self.__bkMyseinoDir + str(self.__today.year) + '\\' + str(self.__today.month) + '\\' + str(self.__today.day) + '\\'
    
    def set(self):
        # 1周間以上前のバックアップデータを削除
        self.__deleteBeforeBkDataOneWeekAgo()
        
        fileList = glob.glob(self.__myseinoFulldir + "/*.wbp")
        shipmentNoDics = {}

        with open(self.__myseinoFulldir + '\swap.csv' ,'w+') as fSwap:

            for file in fileList:
                with open(file, 'r') as fOrigin:
                    # ファイル全体を読込、改行ごとに分割
                    swapReadings = fOrigin.read().split('\n')

                    # マイセイノーの最後の行は改行のみ空行なので、これを避ける
                    for n in range(1, len(swapReadings) - 1): 
                        fSwap.write(swapReadings[n] + '\n')                

                os.makedirs(self.__bkMyseinoDirCurrentDay, exist_ok=True)

                # ファイルをバックアップに移動
                shutil.move(file, self.__bkMyseinoDirCurrentDay + os.path.basename(file))

        swapCsv = self.__myseinoFulldir + '\swap.csv'

        with open(swapCsv ,'r') as fSwap:
            f = csv.reader(fSwap, delimiter=",", doublequote=True, lineterminator="\n", quotechar='"', skipinitialspace=True)

            for row in f:
                # rowはList
                # row[0]で必要な項目を取得することができる
                # 運送伝票番号
                currentShipmentNo = row[4].strip()
                # 管理番号
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

    # 1周間以上前のバックアップデータを削除
    def __deleteBeforeBkDataOneWeekAgo(self):
        # 1周間以上前の日付を取得
        aWeeksAgo = self.__today + datetime.timedelta(weeks=-1)
        # バックアップディレクトリを全て取得
        dirs = glob.glob(self.__myseinoFulldir + '\\bk\\**\\**\\**\\')
        # バックアップディレクトリの日付を取得する正規表現パターン
        bkMyseinoDir = self.__myseinoFulldir + r'\bk'
        pattern = r'(' +re.escape(bkMyseinoDir) + r'\\)(\d{4}\\\d{1,2}\\\d{1,2})'
        # バックアップディレクトリの日付配列
        bkDates = []

        for dir in dirs:
            matches = re.search(pattern ,dir)
            bkDates.append(re.sub(r'\\', '-', matches.group(2)))
        
        bkDates.sort(reverse=True)

        pattern = r'(\d{4})-(\d{2})-(\d{2})'

        for bkDate in bkDates:
            matches = re.search(pattern ,bkDate)
            matchesYear = matches.group(1)
            matchesMonth = matches.group(2)
            matchesDay = matches.group(3)
            swapBkDate = datetime.date(int(matchesYear), int(matchesMonth), int(matchesDay))
            
            # バックアップデータが1周間以上前
            if aWeeksAgo > swapBkDate:
                bkDateOnYear = bkMyseinoDir + '\\' + matchesYear + '\\'
                bkDateOnMonth = bkDateOnYear + matchesMonth + '\\'
                bkDateOnDay = bkDateOnMonth + matchesDay + '\\'

                # 日付階層のディレクトリを削除
                shutil.rmtree(bkDateOnDay)

                # 月階層下のディレクトリに何もなかった場合、その月階層を削除
                countBkDateOnDay = sum(os.path.isdir(os.path.join(bkDateOnMonth, name)) for name in os.listdir(bkDateOnMonth))

                if countBkDateOnDay > 0:
                    continue

                shutil.rmtree(bkDateOnMonth)

                # 年階層下のディレクトリに何もなかった場合、その年階層を削除
                countBkDateOnMonth = sum(os.path.isdir(os.path.join(bkDateOnYear, name)) for name in os.listdir(bkDateOnYear))

                if countBkDateOnMonth > 0:
                    continue

                shutil.rmtree(bkDateOnYear)