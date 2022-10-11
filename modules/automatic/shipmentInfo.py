from modules.automatic.mainSysAuto import MainSysAuto
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

class ShipmentInfo(MainSysAuto):
    
    def get(self):
        # Webドライバーを介してログイン
        webd = self.myWebDriver.login()

        if not webd:
            return

        # 製品情報一覧から情報取得
        try:
            webd.get(self.myWebDriver.jsonLoad['urlProductControlList'])
            time.sleep(4)
            webd.find_element(By.XPATH, '//*[@id="processCompleteFlg1"]').click()
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').click()

            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="listitem0innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="listitem1innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="listitem2innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="listitem3innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="listitem4innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="listitem5innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="assemblePlaceList"]').send_keys(Keys.DOWN)
            webd.find_element(By.XPATH, '//*[@id="listitem6innerListBoxassemblePlaceList"]/div').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="ajaxsearch"]').click()
            time.sleep(30)
            webd.find_element(By.XPATH, '//*[@id="cpbtnCSV"]').click()
            time.sleep(1)
            webd.find_element(By.XPATH, '//*[@id="shippingDataOutput-confirm"]').click()
            time.sleep(60)

        except:
            self.myWebDriver.makeQueue(False)
            
        self.myWebDriver.makeQueue(True)