from modules.automatic.myWebDriver import MyWebDriver
from tkinter import *
from tkinter import ttk
import sys

class MyGui:
    def __init__(self, version, currentDir, downloadDir=None):
        self.__currentDir = currentDir
        self.__downloadDir = downloadDir
        self.__version = version

    # 引数メソッド名をコールバックとして呼び出す
    def handler(self, funcName):
        objMyWebDriver = MyWebDriver(0, self.__currentDir, self.__downloadDir)
        eval('objMyWebDriver.' + funcName)()
        objMyWebDriver.quit()

    def getShipmentInfo(self):
        self.handler(sys._getframe().f_code.co_name)

    def setShipmentNo(self):
        self.handler(sys._getframe().f_code.co_name)

    def run(self):
        # Tkオブジェクト生成
        root = Tk()
        # タイトル
        root.title("RPA ver:" + self.__version)
        # 画面の大きさの決定
        root.geometry("300x200+0+0")
        # ウィジェットの作成
        #frame1 = ttk.Frame(root)
        Static1 = ttk.Label(
            #frame1, 
            text='実行したいRPA処理をクリックして下さい')
        button1 = ttk.Button(
            #frame1,
            text='出荷情報抽出', 
            command=self.getShipmentInfo,
            width=20, 
            padding=5)
        button2 = ttk.Button(
            #frame1,
            text='運送伝票番号登録', 
            command=self.setShipmentNo,
            width=20, 
            padding=5)

        # レイアウト
        #frame1.pack()
        Static1.pack(side = TOP, pady = (10, 0))
        button1.pack(side = TOP, pady = (10, 0))
        button2.pack(side = TOP, pady = 10)

        root.mainloop() #イベントループ