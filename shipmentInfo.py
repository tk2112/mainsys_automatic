import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

def run(webd, url, id, passward):
    webd.get(url)

    # ID/PASSを打ち込みログイン
    time.sleep(3)
    webd.find_element(By.XPATH, '//*[@id="userid"]').send_keys(id, Keys.ENTER)
    webd.find_element(By.XPATH, '//*[@id="password"]').send_keys(passward, Keys.ENTER)