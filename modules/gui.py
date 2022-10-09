from tkinter import *
from tkinter import ttk

def run():
    #終了処理
    def Quit():
        root.quit()
        root.destroy()

    root = Tk() #Tkオブジェクト生成
    root.title("RPA") #GUIのタイトル名の決定
    #root.geometry("300x300") #画面の大きさの決定

    # ウィジェットの作成
    frame1 = ttk.Frame(root, padding=16)
    label1 = ttk.Label(frame1, text='Your name')

    # レイアウト
    frame1.pack()
    label1.pack(side=LEFT)

    root.mainloop() #イベントループ