import os
import re
import json
import csv
import urllib.request
import requests
import time
import pickle
import pandas as pd
from requests_html import HTML
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException,NoSuchElementException
from selenium.webdriver.chrome.options import Options

#from splinter import Browser

requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += ':RC4-SHA'

proxyIP = "127.0.0.1"
proxyPort = 9151


def fetch(url):
    time.sleep(0.4)
    response=requests.get(url=url)
    if response.status_code != 200:  #回傳200代表正常
        print('Invalid url:', response.url)
        return None
    else:
        return response

def bs4soup(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup

def webdriver_crawl(driver, xpath):
    try:
        content = driver.find_element_by_xpath(xpath).text
        return content
    except NoSuchElementException:
        return "?"
    time.sleep(0.4)
def crawl_name(soup):
    name="?"
    try:
        name=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/div/h1/span[1]/a").text
    except NoSuchElementException:
        name="?"
    return name

def crawl_country(soup):
    p_tags = soup.findAll('div', class_ ='clearfix _h71')
    current = "?"
    hometown = "?"
    for p_tag in p_tags:
        contents = p_tag.findNext('ul', class_ = 'uiList fbProfileEditExperiences _4kg _4ks')
        for content in contents:
            try:
                prefix = content.find('div', class_ = 'fsm fwn fcg').text
                if prefix == '現居城市':
                    current = content.find('span', class_ = '_2iel _50f7').text
                elif prefix == '家鄉':
                    hometown = content.find('span', class_ = '_2iel _50f7').text
            except:
                pass
    return current, hometown

def crawl_work_education(soup):
    p_tags = soup.findAll('div', class_ ='clearfix _h71')
    work = []
    education = []
    for p_tag in p_tags:
        contents = p_tag.findNext('ul', class_ = 'uiList fbProfileEditExperiences _4kg _4ks')
        for content in contents:
            if p_tag.text == '工作經歷':
                try:
                    work.append(content.find('div', class_ = '_2lzr _50f5 _50f7').text)
                except:
                    pass
            elif p_tag.text == '學歷':
                try:
                    education.append(content.find('div', class_ = '_2lzr _50f5 _50f7').text)
                except:
                    pass
    if work == []:
        work = "?"
    if education == []:
        education = "?"
    return work, education

def crawl_relationship(soup):
    p_tags = soup.findAll('div', class_ ='clearfix _h71')
    relationship = '?'
    for p_tag in p_tags:
        contents = p_tag.findNext('ul', class_ = 'uiList fbProfileEditExperiences _4kg _4ks')
        for content in contents:
            if p_tag.text == '感情狀況':
                relationship = content.text
    if relationship == '沒有感情狀況資訊可顯示':
        relationship = '無'
    return relationship

def get_age_star(birthday):
    age = '?'
    star_sign = '?'
    if birthday == '?':
        return age, star_sign
    if '年' in birthday:
        year = int(birthday.split('年')[0])
        month = int(birthday.split('年')[1].split('月')[0])
        date = int(birthday.split('年')[1].split('月')[1].split('日')[0])
        age = 2018 - year
        star_sign = "?"
        return age, star_sign
    else:
        month = int(birthday.split('月')[0])
        date = int(birthday.split('月')[1].split('日')[0])
        star_sign = "?"
        return age, star_sign

def crawl_basic_info(soup):
    p_tags = soup.findAll('div', class_ ='clearfix _h71')
    birthday = '?'
    gender = '?'
    blood = '?'
    sex_orientation = '?'
    language = '?'
    religion = '?'

    for p_tag in p_tags:
        #contents = p_tag.findNext('ul', class_ = 'uiList fbProfileEditExperiences _4kg _4ks')
        if p_tag.text == '基本資料':
            contents = p_tag.findAllNext('div', class_ = '_4bl7 _3xdi _52ju')
            for content in contents:
                if content.text == '生日':
                    birthday = content.findNext('div', class_ = '_4bl7 _pt5').text
                elif content.text == '性別':
                    gender = content.findNext('div', class_ = '_4bl7 _pt5').text
                elif content.text == '血型':
                    blood = content.findNext('div', class_ = '_4bl7 _pt5').text
                elif content.text == '戀愛性向':
                    sex_orientation = content.findNext('div', class_ = '_4bl7 _pt5').text
                elif content.text == '語言':
                    language = content.findNext('div', class_ = '_4bl7 _pt5').text
                elif content.text == '宗教信仰':
                    religion = content.findNext('div', class_ = '_4bl7 _pt5').text
    return birthday, gender, blood, sex_orientation, language, religion

def information_per_user(soup):
    #姓名，現居住地，家鄉，工作，學校，感情，性別，血型，性向，語言，宗教，生日，年齡，星座
    overall=[]
    overall.append(crawl_name(soup))
    current_place,home_town=crawl_country(soup)
    overall.append(current_place)
    overall.append(home_town)
    
    work,education=crawl_work_education(soup)
    overall.append("/".join(work))
    overall.append("/".join(education))
    
    relation=crawl_relationship(soup)
    overall.append(relation)
    
    birthday, gender, blood, sex_orientation, language, religion = crawl_basic_info(soup)
    overall.append(gender)
    overall.append(blood)
    overall.append(sex_orientation)
    overall.append(language)
    overall.append(religion)
    overall.append(birthday)

    age, star_sign = get_age_star(birthday)
    overall.append(age)
    overall.append(star_sign)

    return overall
if __name__=='__main__':
    with open('all_friends_url.pickle', 'rb') as f:
        all_friends_url = pickle.load(f)
        
    session = requests.session()    
    r = session.get("http://httpbin.org/ip")
    print(r.text)
    
    options = webdriver.FirefoxOptions()

    firefox_profile = webdriver.FirefoxProfile()#設定讀圖模式
    firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')#不讀圖片，不讀flash driver

    driver = webdriver.Firefox(executable_path=r'C:\\Program Files\Mozilla Firefox\geckodriver.exe', options=options,firefox_profile=firefox_profile)

    total_user_information=[]
    for i in range(0,len(all_friends_url)):
        time.sleep(5)
        driver.get(all_friends_url[i])            
        current_soup=bs4soup(driver)
        current_user=information_per_user(current_soup)

        total_user_information.append(current_user)

    #姓名，現居住地，家鄉，工作，學校，感情，性別，血型，性向，語言，宗教，生日，年齡，星座
    
    with open("facebook_dataset_12_31.csv",'w',newline='',encoding='utf8') as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(['姓名','現居住地','家鄉','工作','學校','感情','性別','血型','性向','語言','宗教','生日','年齡','星座','網址'])
        counter=1
        current_row=[]
        current_row.append(counter)
        current_row.extend(total_user_information)
        writer.writerow(current_row)
        #start the friends
        for i in range(0,len(total_user_information)):
            for j in range(0,len(total_user_information[i])):
                if type(total_user_information[i][j])==str:
                    total_user_information[i][j].encode('utf8').decode('utf8')
            writer.writerow(total_user_information[i])

    file = open('total_user_information.pickle', 'wb')
    pickle.dump(total_user_information, file)
    file.close()
