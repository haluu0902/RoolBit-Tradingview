import atexit, sys, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep
import chromedriver_autoinstaller

class ChromeController():
    def __init__(self):
        #Open Chrome Browser
        chromedriver_autoinstaller.install()
        driver =  webdriver.Chrome(executable_path='./chromedriver')
        atexit.register(driver.close)
        driver.get("https://rollbit.com/trading")
        self.driver = driver

    def ChooseUp(self):
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Up")]').click()

    def ChooseDown(self):
        self.driver.find_element(By.XPATH, '//span[contains(text(), "Down")]').click()

    def GetBalance(self,symbol):
        try:
            return float(self.driver.find_element(By.CSS_SELECTOR,f"a[href='/trading/{symbol.upper()}']").text.replace("$",""))
        except:
            return float(self.driver.find_element(By.CSS_SELECTOR,f"a[href='/trading']").text.replace("$",""))

    def ChangeSymbol(self, symbol):
        driver = self.driver
        symbolUp = symbol.upper()
        if symbolUp != driver.current_url.split("/")[-1]:
            if  len(driver.current_url.split("/")) != 4 or (len(driver.current_url.split("/")) == 4 and symbol != "btc"):
                driver.find_element(By.CSS_SELECTOR,"svg[color='#B1B6C6']").click()
                driver.find_element(By.XPATH, '//div[contains(text(), "%s")]'%(symbolUp)).click()


    def PlaceOrder(self, symbol, side, percent, payout):
        try:
            driver = self.driver
            #Choose side to place the order
            self.ChangeSymbol(symbol)
            if side == "up":
                self.ChooseUp()
            else:
                self.ChooseDown()
            balance = self.GetBalance(symbol)
            #Calculator place value order by percent input
            orderValue = round(balance*percent/100, 2)
            #Send value to in put place
            inputValue = driver.find_element(By.TAG_NAME, "input")
            inputValue.send_keys(Keys.CONTROL, 'a')
            inputValue.send_keys(orderValue)
            #Send payout to input place
            multiple = driver.find_elements(By.TAG_NAME, "input")[1]
            multiple.send_keys(Keys.CONTROL, 'a')
            multiple.send_keys(payout)
            #Place order
            driver.find_element(By.XPATH, '//button[contains(text(), "Place Bet")]').click()
            return {
                "result":True,
                "status": "success",
                "message":"Success!"
                }
        except:
            excType, excObj, excTb = sys.exc_info()
            fname = os.path.split(excTb.tb_frame.f_code.co_filename)[1]
            err = str(excType) + "-" + str(fname) + "-" +str(excTb.tb_lineno)
            return {
                "result":False,
                "status": "fail",
                "message": err
                }
            
        