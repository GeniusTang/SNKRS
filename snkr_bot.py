import json
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from time import sleep
from time import time
from datetime import datetime
from functools import partial

class snkr_bot(object):
    def __init__(self, json_file):
        self._read_json(json_file)
        self._start_driver()
     
    def _read_json(self, json_file):
        """
        Load chrome driver path, chrome cookie path,
        shoes url, shoes size, credit card cvv, release time
        from JSON file.
        """
        with open(json_file, 'r') as f:
            data = json.load(f)
            self.chrome_driver = data["chrome_driver"]
            self.profile_path = data["profile_path"]
            self.url = data["url"]
            self.size = data["size"]
            self.cvv = data["cvv"]
            self.time = datetime.strptime(data["time"], '%Y-%m-%d %H:%M:%S')

    def _start_driver(self):
        """
        Start driver from cookie.
        """
        options = webdriver.ChromeOptions()
        options.add_argument("user-data-dir={}".format(self.profile_path))
        self.driver = webdriver.Chrome(self.chrome_driver, chrome_options=options)
        self.driver.maximize_window()

    def _wait(self, action, freq=0.1, time_out=2, message='Succeeded', err_message='Failed'):
        """
        A wrapper to try an action until succeed.
        action: a callable function,
        freq: how frequent you try,
        time_out: maximum time you want to try,
        message: print if this action succeeds,
        err_message: print if this action fails
        """ 
        FLAG = False
        begin = time()
        while not FLAG and (time()-begin) < time_out:
            try:
                action()
            except Exception as e:
                print(e)
                sleep(freq)
            else:
                FLAG = True
        print(message if FLAG else err_message)
        if not FLAG:
            raise Exception('Program Failed!')
 
    def _find_size(self):
        """
        Try to find size.
        """
        print('Try to find size {}.'.format(self.size))
        find_size = self.driver.find_element_by_xpath('//button[contains(text(), "{}")]'.format(self.size))
        self.driver.execute_script("arguments[0].scrollIntoView(true);", find_size)
        find_size.click()

    def _add_to_cart(self):
        """
        Try to add to cart.
        """
        print('Try to add to cart.')
        add_cart = self.driver.find_element_by_xpath('//button[contains(translate(text(), "CART", "cart"),"cart")]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", add_cart)
        add_cart.click()

    def _quick_buy(self):
        """
        Try to buy without adding to cart.'
        """
        print('Try to quick buy.')
        quick_buy = self.driver.find_element_by_xpath('//button[contains(translate(text(), "BUY", "buy"), "buy")]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", quick_buy)
        quick_buy.click()
 
    def _go_to_url(self, url):
        """
        Navigate to a url.
        """
        print('Try to navigate to {}'.format(url))
        self.driver.get(url)

    def _find_cvv_iframe(self):
        """
        Find and switch domain to the iframe with cvv info.
        """
        print('Try to find credit card iframe.')
        iframe =self.driver.find_element_by_class_name("credit-card-iframe-cvv")
        self.driver.switch_to.frame(iframe)  

    def _enter_cvv(self):
        """
        Enter cvv and switch back to main domain.
        """
        print('Try to enter cvv.')
        cvv = self.driver.find_element_by_id("cvNumber") 
        self.driver.execute_script("arguments[0].scrollIntoView(true);", cvv)
        cvv.send_keys(self.cvv)
        self.driver.switch_to_default_content()

    def _save(self):
        """
        Save credit card info.
        """
        print('Try to save and continue.')
        self.driver.find_element_by_xpath('//button[contains(translate(text(), "SAVE", "save"), "save")]').click()

    def _place_order(self):
        """
        Place order.
        """
        print('Try to place order.')
        self.driver.find_element_by_xpath('//button[contains(translate(text(), "ORDER", "order"), "order")]').click()

    def _test(self):
        """
        Test adding to card and checking out.
        Remember to use a wrong cvv number.
        """
        self._wait(partial(self._go_to_url, self.url))
        self._wait(self._find_size)
        self._wait(self._add_to_cart)
        self._wait(partial(self._go_to_url, 'https://www.nike.com/us/en/checkout'))
        self._wait(self._find_cvv_iframe)
        self._wait(self._enter_cvv)
        self._wait(self._place_order)

    def _buy(self):
        """
        Buy it.
        """
        self._wait(partial(self._go_to_url, self.url))
        self._wait(self._find_size)
        self._wait(self._quick_buy)
        self._wait(self._find_cvv_iframe)
        self._wait(self._enter_cvv)
        self._wait(self._place_order)

    def _start(self, action):
        """
        Start an action at a specific time.
        """
        while True:
            now = datetime.now()
            if now >= self.time:
                action()
                break
            else:
                sleep(0.1)

    def start_test(self):
        """
        Start testing.
        """
        self._start(self._test)

    def start_buy(self):
        """
        Start buying.
        """
        self._start(self._buy)


    def _buy_deprecated(self):
        """
        This function has been deprecated.
        """
        self.driver.get(self.url)
        #wait = WebDriverWait(self.driver, 10, poll_frequency=0.05)
        flag = False
        while not flag:
            try:
                print('try to find size')
                find_size = self.driver.find_element_by_xpath('//button[contains(text(), "{}")]'.format(self.size))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", find_size)
                find_size.click()
                flag = True
            except:
                sleep(0.05)
        #find_size = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[text()="{}"]'.format(self.size))))
        #find_size.click()
        flag = False
        while not flag:
            try:
                print('try to add to cart')
                #add_cart = self.driver.find_element_by_xpath('//button[text()="ADD TO CART"]')
                add_cart = self.driver.find_element_by_xpath('//button[contains(translate(text(), "CART", "cart"),"cart")]')
                #add_cart = wait.until(EC.visibility_of_element_located((By.XPATH, '//button[text()="ADD TO CART"]')))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add_cart)
                add_cart.click()
                flag = True
            except:
                sleep(0.05)
        sleep(0.1) 
        self.driver.get('https://www.nike.com/us/en/checkout') 
        sleep(2)
        iframe =self.driver.find_element_by_class_name("credit-card-iframe-cvv")
        self.driver.execute_script("arguments[0].scrollIntoView(true);", iframe)
        self.driver.switch_to.frame(iframe)
        sleep(2)
        self.driver.find_element_by_id("cvNumber").send_keys("9999") 
        sleep(2)
        self.driver.switch_to_default_content()
        self.driver.find_element_by_xpath('//button[contains(translate(text(), "ORDER", "order"), "order")]').click()

    def _purchase_deprecated(self):
        """
        This funcion has been deprecated.
        """
        self.driver.get(self.url)
        flag = False
        while not flag:
            try:
                print('try to find size')
                find_size = self.driver.find_element_by_xpath('//button[contains(text(), "{}")]'.format(self.size))
                self.driver.execute_script("arguments[0].scrollIntoView(true);", find_size)
                find_size.click()
                flag = True
            except:
                sleep(0.05)

        flag = False
        while not flag:
            try:
                print('try to add to cart')
                #add_cart = self.driver.find_element_by_xpath('//button[contains(text(),"Purchase")]')
                add_cart = self.driver.find_element_by_xpath('//button[contains(translate(text(), "BUY", "buy"), "buy")]')
                self.driver.execute_script("arguments[0].scrollIntoView(true);", add_cart)
                add_cart.click()
                flag = True
            except:
                sleep(0.05)

        flag = False
        while not flag:
            try:
                print('try to place order')
                #self.driver.find_element_by_xpath("//input[contains(@placeholder,'XXX')]").send_keys("9273")
                self.driver.find_element_by_xpath('//input[@placeholder="XXX"]').send_keys("9273")
                #self.driver.find_element_by_xpath("//input[contains(@value,'Place')]").click()
                self.driver.find_element_by_xpath('//input[contains(translate(@value, "PLACE", "place"), "place")]').click()
                flag = True
            except:
                sleep(0.05)
        
if __name__ == "__main__":
    json_file = 'test.json'
    bot = snkr_bot(json_file)
    bot.start_test()

