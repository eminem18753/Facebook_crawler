# coding: utf-8

import requests
import re
from bs4 import BeautifulSoup
import time
import sys
from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException,NoSuchElementException
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO
from skimage import io
import numpy as np
from captcha import *
import cv2
import urllib
import urllib.request

    
def get_school(name='吳明倫', birthday='84/11/05'):
    birth = birthday
    year = int(birth.split('/')[0])
    month = int(birth.split('/')[1])
    entrance_year = year + 18
    if month >= 9:
        entrance_year += 1
    url = 'https://www.com.tw/cross/namequery' + str(entrance_year) + '.html'

    options = webdriver.FirefoxOptions()
    firefox_profile = webdriver.FirefoxProfile()
    driver = webdriver.Firefox()
    driver.get(url)

    #images = driver.find_element_by_id('captchaImg')
    #img_src = driver.find_element_by_xpath('//*[@id="captchaImg"]')
    img_tag = driver.find_element_by_id('captchaImg')
    img_src = img_tag.get_attribute('src')
    
    #captcha_img=io.imread(img_src)
    captcha_img = urllib.request.urlopen(img_src)
    arr = np.asarray(bytearray(captcha_img.read()), dtype=np.uint8)
    captcha_img = cv2.imdecode(arr, -1) # 'Load it as it is'

    #captcha_img = cv2.cvtColor(captcha_img, cv2.COLOR_BGR2RGB)
    #cv2.imshow("h",captcha_img)
    #cv2.waitKey(0)
    captcha = CAPTCHA(img_file = captcha_img, model_path = './hack.pth')
    prediction = captcha.classification()
    captcha_str = ""
    for s in prediction:
        captcha_str += str(s)
    print("The captcha is: "+captcha_str)
    wait = WebDriverWait(driver, 10)
    wait.until(ec.visibility_of_element_located((By.ID, 'captcha')))
    driver.find_element_by_id('name').send_keys(name)
    driver.find_element_by_id('captcha').send_keys(captcha_str)
    driver.find_element_by_id('submit').click()

    school = []
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', id = 'mainContent')
    body = table.find('tbody')
    p_tags = body.findAll('div', {'align': 'center'})
    for p_tag in p_tags:
        all_school = p_tag.findAll('tr')
        for sch in all_school:
            crown = sch.find('div', {'align': 'right'})
            if crown.contents != ['\n']:
                school_str = sch.find('a').text.splitlines()
                school_name = ""
                for i in school_str:
                    school_name += i
                school.append(school_name)
    return school

school = get_school('楊承翰', '84/10/25')
print(school)

