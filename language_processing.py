import os
import re
import json
import csv
import urllib.request
import requests
import time
import pandas as pd

from selenium import webdriver

def fetch(url):
    time.sleep(0.4)
    response=requests.get(url=url)
    if response.status_code != 200:  #回傳200代表正常
        print('Invalid url:', response.url)
        return None
    else:
        return response

def get_ping_yin(driver,chinese_name):
    driver.get("https://crptransfer.moe.gov.tw/")
    
    driver.find_element_by_id('SN').send_keys(chinese_name)
    driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td/main/article/div/div[1]/form/ul/li/div[2]/label[2]/input").click()
    driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td/main/article/div/div[1]/form/ul/li/input[2]").click()
    
    all_children=driver.find_element_by_xpath("/html/body/table/tbody/tr[1]/td/main/article/div/table/tbody/tr[3]/td").find_elements_by_xpath(".//*")
    
    ping_yin_results=""
    space=""
    for i in range(0,len(all_children)):
        ping_yin_results+=space+all_children[i].text
        space=" "
    return ping_yin_results

def is_Chinese(uchar):         
    if '\u4e00' <= uchar<='\u9fff':
        return True
    else:
        return False
    
dataset=pd.read_csv("facebook_dataset_clean.csv",index_col=False)

options = webdriver.FirefoxOptions()

firefox_profile = webdriver.FirefoxProfile()#設定讀圖模式
firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')#不讀圖片，不讀flash driver

driver = webdriver.Firefox(executable_path=r'C:\\Program Files\Mozilla Firefox\geckodriver.exe', options=options,firefox_profile=firefox_profile)
#chinese to ping yin
chinese_name="陳冠宇"
ping_yin=get_ping_yin(driver,chinese_name)
#result string

output=open("facebook_dataset_final_1_12.csv","w",newline='',encoding="utf-8")
counter=0
with open('facebook_dataset_clean.csv', newline='',encoding="utf-8") as csvfile:
  rows = csv.reader(csvfile)
  writer=csv.writer(output)
  writer.writerow(['姓名','暱稱','現居住地','家鄉','工作','學校','網址'])
  
  for row in rows:
      temp=[]
      #判斷姓名是否包含暱稱
      if row[0].find("\n")!=-1:
          names=row[0].split("\n")
          names[1]=names[1].replace("(","")
          names[1]=names[1].replace(")","")
          temp.append(names[0])
          temp.append(names[1])
      else:
          temp.append(row[0])
          if is_Chinese(row[0])==False:
              temp.append("foreign")
          else:
              ping_yin=get_ping_yin(driver,row[0])
              temp.append(ping_yin)
              
      temp.append(row[1])    
      temp.append(row[2])    
      temp.append(row[3])    
      temp.append(row[4])    
      temp.append(row[-1])    
          
      writer.writerow(temp)
