# py -m pip install selenium
# py -m pip install pyinstaller

from modules.automatic.myWebDriver import MyWebDriver
import sys
import os
import re
import const
import gui

const.VERSION = '1.0.0'

sessionId = ''

flgShipmentInfo = False
flgShipmentNoSet = False

args = sys.argv
scriptFullpath = os.path.abspath(args[0])
currentDir = os.path.dirname(scriptFullpath)
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

    objMyWebDriver = MyWebDriver(sessionId, currentDir, downloadDir)

    if flgShipmentInfo:
        objMyWebDriver.getShipmentInfo()

    if flgShipmentNoSet:
        objMyWebDriver.setShipmentNo()
        
else:
    gui.run()