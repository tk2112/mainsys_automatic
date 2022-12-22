import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as chrome_service
from subprocess import CREATE_NO_WINDOW

class MyWebDriver:
    def __init__(self, currentDir, sessionId=None, downloadDir=None):
        # chromeを立ち上げる
        executablePath = currentDir + r'\bin\chromedriver.exe'
        self.__cs = chrome_service.Service(executablePath)
        self.__cs.creationflags = CREATE_NO_WINDOW
        # Chromeのオプション設定
        self.__chromeOptions = webdriver.ChromeOptions()
        # ターミナルが出すエラーメッセージを消す
        self.__chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        # ルートURL・ID・PASS設定
        profileFullpath = currentDir + '\ini\profile.json'

        jsonOpen = open(profileFullpath, 'r', encoding='utf-8')
        
        self.jsonLoad = json.load(jsonOpen)
        self.rootUrl = self.jsonLoad['rootUrl']
        self.id = self.jsonLoad['id']
        self.password = self.jsonLoad['pass']
        self.currentDir = currentDir
        self.sessionId = sessionId
        self.islogin = False
        self.__webd = None

        # Chromeからのダウンロード先を設定
        self.downloadDir = None
        self.setChromeDownloadDir(downloadDir)

    # 引数を参照してChromeからのダウンロード先を設定
    def setChromeDownloadDir(self, downloadDir=None):
        if downloadDir is None:
            downloadDir = self.currentDir + r'\tmp'

        elif not os.path.exists(downloadDir):
            print('WARNING: not found what download directory: ' + downloadDir + '.')

            downloadDir = self.currentDir + r'\tmp'

        self.__chromeOptions.add_experimental_option(
            'prefs', {
                'download.default_directory': downloadDir
            }
        )

        self.downloadDir = downloadDir
        
    # webDriverを返す
    def getWebd(self):
        return webdriver.Chrome(service = self.__cs, options = self.__chromeOptions)

    def quit(self):
        if self.__webd:
            self.__webd.quit()

    # ログインしてwebDriverを返す
    def login(self):
        if not self.islogin:
            try:
                webd = webdriver.Chrome(service = self.__cs, options = self.__chromeOptions)

                webd.get(self.rootUrl)

                # ID/PASSを打ち込みログイン
                time.sleep(3)
                webd.find_element(By.XPATH, '//*[@id="userid"]').send_keys(self.id, Keys.ENTER)
                webd.find_element(By.XPATH, '//*[@id="password"]').send_keys(self.password, Keys.ENTER)

                time.sleep(1)

                self.islogin = True
                self.__webd = webd

            except:
                print('ERROR: Not Cannot Login WebDriver.')

                return None

        return self.__webd

    # キューメッセージ作成
    def makeQueue(self, isSuccess = False):
        if not self.sessionId:
            return

        queueBaseName = self.jsonLoad['queue']['baseName']
        userDir = os.environ['USERPROFILE']
        tempDir = userDir + r'\AppData\Local\Temp' + '\\'
        queueFullpath = tempDir + queueBaseName + '.' + self.sessionId + r'.tmp'
        queue = open(queueFullpath, 'w')

        if isSuccess:
            queue.write(self.jsonLoad['queue']['successWord'])
        else:
            queue.write(self.jsonLoad['queue']['failureWord'])

        queue.close()

    # 製品情報一覧から出荷情報を取得
    def getShipmentInfo(self):
        from modules.automatic.shipmentInfo import ShipmentInfo

        objShipmentInfo = ShipmentInfo(self)
        objShipmentInfo.get()

    # マイセイノーの運送伝票番号を登録
    def setShipmentNo(self):
        from modules.automatic.shipmentNo import ShipmentNo

        objShipmentNo = ShipmentNo(self)
        objShipmentNo.set()

    # XM039を動かす
    def runOverseasShipmentForVBA(self):
        from modules.automatic.externalVBA import ExternalVBA

        excelFullpath = self.jsonLoad['excelIni']['XM039']['fullpath']
        macroName = self.jsonLoad['excelIni']['XM039']['autoRunMacroName']
        
        objExternalVBA = ExternalVBA()
        objExternalVBA.run(excelFullpath, macroName)

    # 日本出荷の海外物件をまとめ、EXCELを作る（使わない？）
    def storeOverseasWithSvrDatabase(self):
        from modules.automatic.svrDatabase import SvrDatabase

        objSvrDatabase = SvrDatabase(self)
        objSvrDatabase.storeOverseas()