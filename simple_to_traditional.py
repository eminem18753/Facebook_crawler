import os
import re
import json
import csv
import requests
import time
import pandas as pd

from opencc import OpenCC

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

dataset=pd.read_csv("facebook_dataset_final_1_12.csv", na_filter=False)
clean_data=open("facebook_dataset_processed_1_12.csv","w",newline='',encoding="utf-8")
updating=csv.writer(clean_data)

for index, row in dataset.iterrows():
    if row[0]!="":
        updating.writerow(row)
        
cc = OpenCC('s2t')

output=open("facebook_dataset_traditional_1_12.csv","w",newline='',encoding="utf-8")
counter=0

with open('facebook_dataset_processed_1_12.csv', newline='',encoding="utf-8") as csvfile:
  rows = csv.reader(csvfile)
  writer=csv.writer(output)
  writer.writerow(['姓名','暱稱','現居住地','家鄉','工作','學校','網址'])
  
  for row in rows:
      temp=[]
      #判斷姓名是否包含暱稱
      for index in row:
          to_convert =index
          converted = cc.convert(index)
          temp.append(converted)
          
      writer.writerow(temp)
