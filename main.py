# py -m pip install selenium
# py -m pip install pyinstaller

import sys
import os
import re
import json
import const
import shipmentInfo
import gui
from selenium import webdriver
from selenium.webdriver.chrome import service as chrome_service

const.VERSION = '1.0.0'

downloadDir = None
flgShipmentInfo = False

args = sys.argv
scriptFullpath = os.path.abspath(args[0])
currentDir = os.path.dirname(scriptFullpath)

def getWebd(downloadDir=None):
    # chromeを立ち上げる
    executable_path = currentDir + r'\bin\chromedriver.exe'
    cs = chrome_service.Service(executable_path)
    # Chromeのオプション設定
    ChromeOptions = webdriver.ChromeOptions()
    # ターミナルが出すエラーメッセージを消す
    ChromeOptions.add_experimental_option('excludeSwitches', ['enable-logging'])
    # 引数を参照してダウンロード先を設定
    if downloadDir is not None:
        if os.path.exists(downloadDir):       
            ChromeOptions.add_experimental_option(
                'prefs', {
                    'download.default_directory': downloadDir
                }
            )
        else:
            print('WARNING: not found what download directory: ' + downloadDir + '.')
            #makeQueue(False)
            #sys.exit()

    return webdriver.Chrome(service = cs, options = ChromeOptions)

if len(args) > 1:
    for arg in args:
        if arg == "-v":
            print(const.VERSION)

        elif re.match('^--download=.+', arg):
            downloadDir = arg.split('=')[1]

        elif arg == 'shipmentInfo':
            flgShipmentInfo = True

    profileFullpath = currentDir + '\ini\profile.json'

    jsonOpen = open(profileFullpath, 'r')
    jsonLoad = json.load(jsonOpen)

    if flgShipmentInfo:
        webd = getWebd(downloadDir)
        shipmentInfo.run(webd, jsonLoad['rootUrl'], jsonLoad['id'], jsonLoad['pass'])

else:
    gui.run()