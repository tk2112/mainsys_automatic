import os
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service as chrome_service

class MyWebDriver:
    def __init__(self, sessionId, currentDir, downloadDir=None):
        # chromeを立ち上げる
        executablePath = currentDir + r'\bin\chromedriver.exe'
        self.__cs = chrome_service.Service(executablePath)
        # Chromeのオプション設定
        self.__chromeOptions = webdriver.ChromeOptions()
        # ターミナルが出すエラーメッセージを消す
        self.__chromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
        # 引数を参照してダウンロード先を設定
        if downloadDir is not None:
            if os.path.exists(downloadDir):       
                self.__chromeOptions.add_experimental_option(
                    'prefs', {
                        'download.default_directory': downloadDir
                    }
                )
            else:
                print('WARNING: not found what download directory: ' + downloadDir + '.')

        # ルートURL・ID・PASS設定
        profileFullpath = currentDir + '\ini\profile.json'

        jsonOpen = open(profileFullpath, 'r')
        
        self.jsonLoad = json.load(jsonOpen)
        self.rootUrl = self.jsonLoad['rootUrl']
        self.id = self.jsonLoad['id']
        self.password = self.jsonLoad['pass']
        self.currentDir = currentDir
        self.sessionId = sessionId
        self.islogin = False
        self.__webd = None
        
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

        userDir = os.environ['USERPROFILE']
        tempDir = userDir + r'\AppData\Local\Temp' + '\\'
        queueFullpath = tempDir + os.path.basename(__file__) + '.' + self.sessionId + r'.tmp'
        queue = open(queueFullpath, 'w')

        if isSuccess:
            queue.write('success')
        else:
            queue.write('failure')

        queue.close()

    def getShipmentInfo(self):
        from modules.automatic.shipmentInfo import ShipmentInfo

        objShipmentInfo = ShipmentInfo(self)
        objShipmentInfo.get()

    def setShipmentNo(self):
        from modules.automatic.shipmentNo import ShipmentNo

        objShipmentNo = ShipmentNo(self)
        objShipmentNo.set()