from selenium import webdriver
import requests
import json
import time
import facebook
import urllib3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException,NoSuchElementException
from selenium.webdriver.chrome.options import Options
import csv
import pickle

from bs4 import BeautifulSoup
def fetch(url):
    time.sleep(0.4)
    response=requests.get(url=url)
    if response.status_code != 200:  #回傳200代表正常
        print('Invalid url:', response.url)
        return None
    else:
        return response

def retrieve_all_information(driver,profile_url):
    all_result=[]
    """
    姓名、FB帳號、ig帳號、年齡、生日、居住地區、來自地區、地址、畢業國中、高中、大學、研究所、星座、血型、gmail、手機號碼、父母名字、感情狀態
    """
    time.sleep(0.4)
    try:#可能包含英文名字
        chinese_name=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div/h1/span[1]/a").text
        all_result.append(chinese_name)
    except NoSuchElementException:
        all_result.append("?")
    time.sleep(0.4)

    try:
        English_name=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[1]/div/div/h1/span[1]/a/span").text
        all_result.append(English_name)
    except NoSuchElementException:
        all_result.append("?")
    time.sleep(0.4)
    
    all_result.append(profile_url)
    all_result.append("?")#ig URL
    all_result.append("?")#年齡
    
    try:
        driver.get(profile_url+"&sk=about")
        birthday=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/ul/li/div/div[2]/div/div/div[2]/ul/li[1]/div/div[2]/span/div[2]").text
        all_result.append(birthday)
    except NoSuchElementException:
        all_result.append("?")
    driver.get(profile_url)
    time.sleep(0.4)
    
    try:
        current_living_area=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/span/ol/li[2]/div/div[2]/div[2]/div[1]/ul/li[4]/div/div/div/div").text
        all_result.append(current_living_area)
    except NoSuchElementException:
        all_result.append("?")
    time.sleep(0.4)
      
    try:
        come_from_area=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[1]/div[1]/div[1]/div[2]/div/div/div/span/ol/li[2]/div/div[2]/div[2]/div[1]/ul/li[5]/div/div/div/div").text
        all_result.append(come_from_area)
    except NoSuchElementException:
        all_result.append("?")
    time.sleep(0.4)

    all_result.append("?")#地址
    all_result.append("?")#國中
    all_result.append("?")#高中
    all_result.append("?")#大學
    all_result.append("?")#研究所
    all_result.append("?")#星座
    
    try:
        driver.get(profile_url+"&sk=about&section=contact-info")
        blood_type=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/ul/li/div/div[2]/div/div/div[2]/div/ul/li[4]/div/div[2]/div/div/span").text
        all_result.append(blood_type)
    except NoSuchElementException:
        all_result.append("?")
    time.sleep(0.4)
    
    driver.get(profile_url)
    
    all_result.append("?")#gmail
    all_result.append("?")#手機號碼
    all_result.append("?")#父親名字
    all_result.append("?")#母親名字

    try:
        driver.get(profile_url+"&sk=about&section=overview")
        relationship_status=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[2]/div/div/div[1]/div[2]/div/ul/li/div/div[2]/div/div/div[1]/ul/li[4]/div/div/div/div[1]").text
        all_result.append(relationship_status)
    except NoSuchElementException:
        all_result.append("?")
    time.sleep(0.4)

    driver.get(profile_url)
    
    return all_result
    
token="EAALbnTifIKMBADeC06vX50ZA26BiJuHgo6b4IuEQwFFfiKRkaTIx7yIevwf38J3VWZC1Qrh5pvQmeDgQTlZCzgeuUSvelKZAtGdPQY4By7Dh4tb9DonC8mmTYorloyZBHuLl6iwng2fFBxZBh55FDnSEPNL3ArZBOMZCGAKaLJ0ZBahivZBbuXcgBtZAyqlQTbVlOMZD"
graph = facebook.GraphAPI(access_token = token)

options = webdriver.FirefoxOptions()

firefox_profile = webdriver.FirefoxProfile()#設定讀圖模式
firefox_profile.set_preference('permissions.default.image', 2)#不讀圖片
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')#不讀圖片，不讀flash driver

driver = webdriver.Firefox(executable_path=r'D:\\geckodriver.exe', options=options,firefox_profile=firefox_profile)
LOGIN_URL = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'

driver.get(LOGIN_URL)

# wait for the login page to load
wait=WebDriverWait(driver, 10)
wait.until(ec.visibility_of_element_located((By.ID, "email")))

driver.find_element_by_id('email').send_keys("品維的email")
driver.find_element_by_id('pass').send_keys("品維的密碼")
driver.find_element_by_id('loginbutton').click()

start_url=r"https://www.facebook.com/profile.php?id=100002703513934"
driver.get(start_url)

my_all_information=retrieve_all_information(driver,start_url)
print(my_all_information)

#friends start
driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div/div[3]/div/div[2]/div[2]/ul/li[3]/a").click()

flag=True
uls_beforeScroll =len(driver.find_elements_by_xpath("//div[@id='pagelet_timeline_app_collection_1155995189:2356318349:2']/ul"))

while(flag):#會抓到社團和粉絲專頁
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    time.sleep(4)
    uls_afterScroll = len(driver.find_elements_by_xpath("//div[contains(@id,'pagelet_timeline_app_collection_')]/ul"))
    if(uls_afterScroll == uls_beforeScroll):
        flag = False
    else:
        uls_beforeScroll = uls_afterScroll

name=""

names = driver.find_elements_by_xpath("//div[@class='fsl fwb fcb']")
overall_friends_url=[]
for name in names:
    print(name.find_element_by_tag_name("a").text)
    overall_friends_url.append(name.find_element_by_tag_name("a").get_attribute('href'))
#friends end
"""
all_friends_information=[]
for index in range(0,len(overall_friends_url)):
    driver.get(overall_friends_url[index])
    my_all_information=[]
    my_all_information=retrieve_all_information(driver,overall_friends_url[index])
    all_friends_information.append(my_all_information)
    #print(my_all_information)
    
with open("facebook_dataset.csv",'w',newline='',encoding='utf8') as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(['id','中文名字','英文名字','FB URL','ig URL','年齡','生日','現居地區','來自地區','地址','國中','高中','大學','研究所','星座','血型','gmail','手機號碼','父親名字','母親名字','感情狀態'])
    counter=1
    current_row=[]
    current_row.append(counter)
    current_row.extend(my_all_information)
    writer.writerow(current_row)
    #start the friends
    for i in range(0,len(all_friends_information)):
        for j in range(0,len(all_friends_information[i])):
            all_friends_information[i][j].encode('utf8').decode('utf8')
        writer.writerow(all_friends_information[i])
"""     
# pickle a variable to a file
file = open('all_friends_url.pickle', 'wb')
pickle.dump(overall_friends_url, file)
file.close()