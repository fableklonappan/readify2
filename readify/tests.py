from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'
    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        logd = driver.find_element(By.CSS_SELECTOR, "i#log-drop.bi.bi-person-gear.customSize.mr-3")
        logd.click()
        time.sleep(1)
        login = driver.find_element(By.CSS_SELECTOR, "a[href='/login/']")
        login.click()
        time.sleep(1)
        email = driver.find_element(By.CSS_SELECTOR, "input[type='email']#mail.form-control[name='email'][placeholder='Email address']")
        email.send_keys("fablelonappan@gmail.com")
        password = driver.find_element(By.CSS_SELECTOR, "input#pass[name='pwd']")
        password.send_keys("Lonson@2609")
        print('Typed email and password')
        time.sleep(1)
        login1 = driver.find_element(By.CSS_SELECTOR, "button#submit.btn.btn-primary.btn-block.mb-4.md-5.p-6.w-100")
        login1.click()
        print('Logged in')
        time.sleep(2)
        book = driver.find_element(By.CSS_SELECTOR, "a.sf-with-ul")
        book.click()
        time.sleep(2)
        pricopy = driver.find_element(By.CSS_SELECTOR, "a#printcopy[href='/libraryapp/books_view/']")
        pricopy.click()
        time.sleep(2)
        addwish = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-outline-danger.ml-50.w-25.mt-10 i.bi.bi-suit-heart-fill.pr-3")
        addwish.click()
        print('Added to Wishlist')
        time.sleep(2)
        addcart = driver.find_element(By.CSS_SELECTOR, "button.btn.btn-outline-info.w-25.ml-50.mt-10 i.bi.bi-cart-plus.pr-3")
        addcart.click()
        print('Added to Cart')
        time.sleep(2)
        book = driver.find_element(By.CSS_SELECTOR, "a.sf-with-ul")
        book.click()
        time.sleep(2)
        audiobook = driver.find_element(By.CSS_SELECTOR, "a#audbook[href='/libraryapp/audio_view/']")
        audiobook.click()
        time.sleep(2)
        audiobookdown = driver.find_element(By.CSS_SELECTOR, "a[href='/media/audiobooks/dont.mp3'][download].btn.btn-outline-info.btn-lg i.bi.bi-file-music-fill.ml-5")
        audiobookdown.click()
        print('Audio book downloaded')
        time.sleep(2)
        
if __name__ == '__main__':
    import unittest
    unittest.main()