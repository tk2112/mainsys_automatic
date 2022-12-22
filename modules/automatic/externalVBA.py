import xlwings as xw

class ExternalVBA:

    # 引数を参照してChromeからのダウンロード先を設定
    def run(self, fileFullPath=None, macroName=None):
        app = xw.App()
        wb = app.books.open(fileFullPath)

        macro = wb.macro(macroName)
        macro()

        wb.save()
        wb.close()
        app.quit()