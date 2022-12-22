# py -m pip install selenium
# py -m pip install pyinstaller
# https://chromedriver.chromium.org/downloads -> bin/

from modules.automatic.myWebDriver import MyWebDriver
from modules.gui import MyGui
import sys
import os
import re
import modules.const as const

const.VERSION = '1.1.0'

sessionId = ''

flgShipmentInfo = False
flgShipmentNoSet = False
flgStoreOverseasWithSvrDatabase = False
flgRunOverseasShipmentForVBA = False

args = sys.argv
scriptFullpath = os.path.abspath(args[0])
currentDir = os.path.dirname(scriptFullpath)
sessionId = None
downloadDir = None

if len(args) > 1:
    for arg in args:
        if arg == "-v":
            print(const.VERSION)

        elif re.match('^--session=.+', arg):
            sessionId = arg.split('=')[1]

        elif re.match('^--download=.+', arg):
            downloadDir = arg.split('=')[1]

        elif arg == 'getShipmentInfo':
            flgShipmentInfo = True

        elif arg == 'setShipmentNo':
            flgShipmentNoSet = True

        elif arg == 'storeOverseasWithSvrDatabase':
            flgStoreOverseasWithSvrDatabase = True

        elif arg == 'runOverseasShipmentForVBA':
            flgRunOverseasShipmentForVBA = True

    objMyWebDriver = MyWebDriver(currentDir, sessionId, downloadDir)

    if flgShipmentInfo:
        objMyWebDriver.getShipmentInfo()

    if flgShipmentNoSet:
        objMyWebDriver.setShipmentNo()

    if flgStoreOverseasWithSvrDatabase:
        objMyWebDriver.storeOverseasWithSvrDatabase()

    if flgRunOverseasShipmentForVBA:
        objMyWebDriver.runOverseasShipmentForVBA()

    objMyWebDriver.quit()
        
else:
    gui = MyGui(const.VERSION, currentDir, downloadDir)
    gui.run()