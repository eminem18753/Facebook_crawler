import tkinter as tk
from tkinter import *
import os
import re
import json
import csv
import urllib.request
import requests
import time
import pickle
import pandas as pd
import jieba
import sys
import importlib
import numpy as np
import cv2
import urllib
import face_recognition
import dlib

from face_recognition import api
from face_recognition import face_recognition_cli
from face_recognition import face_detection_cli

from captcha import *

from bs4 import BeautifulSoup
from gensim.models.keyedvectors import KeyedVectors
from selenium import webdriver
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException,NoSuchElementException
from selenium.webdriver.chrome.options import Options
import warnings
"""
img_a1 = api.load_image_file("D:/test_images/eric1.jpg")
img_a2 = api.load_image_file("D:/test_images/jay1.jpg")
img_a3 = api.load_image_file("D:/test_images/wang1.jpg")

img_b1 = api.load_image_file("D:/test_images/eric2.jpg")
"""
"""
img_a1 = api.load_image_file("eric1.jpg")
img_a2 = api.load_image_file("jay1.jpg")
img_a3 = api.load_image_file("wang1.jpg")

img_b1 = api.load_image_file("eric2.jpg")

face_encoding_a1 = api.face_encodings(img_a1)[0]
face_encoding_a2 = api.face_encodings(img_a2)[0]
face_encoding_a3 = api.face_encodings(img_a3)[0]
face_encoding_b1 = api.face_encodings(img_b1)[0]

faces_to_compare = [
    face_encoding_a2,
    face_encoding_a3,
    face_encoding_b1]

distance_results = api.face_distance(faces_to_compare, face_encoding_a1)
"""

warnings.filterwarnings(action = 'ignore', category = UserWarning, module = 'gensim')
word_vectors = KeyedVectors.load_word2vec_format('Wiki50.txt', binary=False)

importlib.reload(sys)

options = webdriver.FirefoxOptions()

firefox_profile = webdriver.FirefoxProfile()#設定讀圖模式
#firefox_profile.set_preference('permissions.default.image', 2)#不讀圖片
#firefox_profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', 'false')#不讀圖片，不讀flash driver

driver = webdriver.Firefox(executable_path=r'C:\\Program Files\Mozilla Firefox\geckodriver.exe', options=options,firefox_profile=firefox_profile)
face_distances=[]

def bs4soup(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    return soup

def crawl_name(soup):
    name="?"
    try:
        name=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[3]/div/div[1]/div/div/h1/span[1]/a").text
        if name.find("\n")!=-1:
            names=name.split("\n")
            names[1]=names[1].replace("(","")
            names[1]=names[1].replace(")","")
            return names[0], names[1]
        else:
            return name, '?'
    except NoSuchElementException:
        name="?"
    return name, "?"

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

def get_age(birthday):
    age = '?'
    star_sign = '?'
    if birthday == '?':
        return age, star_sign
    if '年' in birthday:
        year = int(birthday.split('年')[0])
        month = int(birthday.split('年')[1].split('月')[0])
        date = int(birthday.split('年')[1].split('月')[1].split('日')[0])
        age = 2018 - year
        return age
    else:
        month = int(birthday.split('月')[0])
        date = int(birthday.split('月')[1].split('日')[0])
        return age
    
def information_per_user(soup):
    #姓名，暱稱，現居地，家鄉，工作，學校
    overall=[]
    name, nickname = crawl_name(soup)
    overall.append(name)
    overall.append(nickname)
    current_place,home_town=crawl_country(soup)
    overall.append(current_place)
    overall.append(home_town)
    
    work,education=crawl_work_education(soup)
    overall.append("/".join(work))
    overall.append("/".join(education))

    return overall

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
    
    captcha = CAPTCHA(img_file = captcha_img, model_path = './hack.pth')
    prediction = captcha.classification()
    captcha_str = ""
    for s in prediction:
        captcha_str += str(s)

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


def segment(words):
    words_seg = jieba.cut(words, cut_all=False)
    word_list = []
    for word in words_seg:
        word_list.append(word)
    return word_list

def cosine_similarity(src, trg):
    input_raw = segment(src)
    target_raw = segment(trg)
    input = []
    target = []
    #skip_list = [' ', ',', '國立', '中學', '大學']
    skip_list = [' ', ',','/']
    confuse_list = ['國立', '中學', '大學']
    for i in input_raw:
        if i not in skip_list:
            input.append(i)
    for i in target_raw:
        if i not in skip_list:
            target.append(i)
    for i in confuse_list:
        if i in input and i in target:
            input.remove(i)
            target.remove(i)
    input_len = len(input)
    target_len = len(target)
    if input_len > target_len:
        min_len = target_len
        short_list = target[:]
        long_list = input[:]
    else:
        min_len = input_len
        short_list = input[:]
        long_list = target[:]
    #print(min_len)

    matching = []

    for i in short_list:
        max_match = 0
        for j in long_list:
            try:
                res = word_vectors.similarity(i, j)
                if res > max_match:
                    max_match = res
            except:
                pass
        matching.append(max_match)
    matching.sort()
    matching_list = matching[-(min_len):]
    if min_len == 0:
        avg_matching = 0.
    else:
        avg_matching = sum(matching_list)/float(min_len)
    #print("Matching List: ", matching_list)
    #print("Average matching score: ", avg_matching)
    return avg_matching



def main_function():
    orig_name=name_var.get()
    nickname=nickname_var.get()
    home=home_var.get()
    hometown=hometown_var.get()
    work=work_var.get()
    school=school_var.get()
    birthday=birthday_var.get()
    choice=webcam_var.get()
    
    input_info_ = [orig_name, nickname, home, hometown, work, school, birthday]
    print("Input data: ", input_info_)
    
    find_name = orig_name

    URL = 'https://www.facebook.com/public/' + find_name

    driver.get(URL)

    # wait for the login page to load
    wait=WebDriverWait(driver, 10)
    flag=True
    uls_beforeScroll= driver.find_elements_by_xpath("//*[@id='contentCol']")
    last=uls_beforeScroll[0].size['height']
    counter = 0
    while(flag):#會抓到社團和粉絲專頁
        counter += 1
        if counter >= 1:
            flag = False
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        uls_afterScroll = driver.find_elements_by_xpath("//*[@id='contentCol']")
        current=uls_afterScroll[0].size['height']
        
        if(current == last):
            flag = False
        else:
            last = current

    names = driver.find_elements_by_class_name('_32mo')
    url_list = []
    for name in names:
        url_list.append(name.get_attribute('href'))
    
    total_user_information = []
    search_num = 15
    count = 0.
    counter=0
    
    for i in range(0,search_num):
        if os.path.exists(str(i+1)+".jpg"):
            os.remove(str(i+1)+".jpg")
        
    for url in url_list[:search_num]:
        count = count + 1.
        counter=counter+1
        print('Searching......  %.2f' % float((count/int(search_num))*100), '%')
        time.sleep(5)
        driver.get(url)            
        current_soup=bs4soup(driver)
        current_user=information_per_user(current_soup)
        total_user_information.append(current_user)    
        if choice=='a' or choice=='b':
            try:
                image_path=driver.find_element_by_xpath("/html/body/div[1]/div[3]/div[1]/div/div[2]/div[2]/div[1]/div/div[1]/div[1]/div[3]/div/div[2]/div[3]/div/div/div/img")
                image_url=image_path.get_attribute('src')
                urllib.request.urlretrieve(image_url, str(counter)+".jpg")
            except:
                pass
    # Add school information from 'www.com.tw'
    input_info = input_info_[:]
    if input_info[-1] != '?' and input_info[-1] != '':
        school = get_school(input_info[0], input_info[-1])
        if school is not []:
            for i in school:
                input_info[-2]+='/'+i
        print("Adding school information......")
        print('New data: ', input_info)
    
    score_list = []
    feature_weight = [1.8, 1., 1., 1., 1., 1.]
    for i in range(len(total_user_information)):
        score = 0.
        feature_cnt = 0
        for idx in range(len(input_info[:-1])):
            if total_user_information[i][idx] != 0 and total_user_information[i][idx] != '?':
                if input_info[idx] != '?' and input_info[idx] != '':
                    feature_cnt += 1
                    score += feature_weight[idx]*cosine_similarity(total_user_information[i][idx], input_info[idx])
        similar_score = (score + 0.6*feature_cnt/len(input_info[:-1])) / float(feature_cnt + 1)
        score_list.append(similar_score)
    predict_idx = score_list.index(max(score_list))
    
    print('Score without images: ', score_list)
    print('Result without images: ', url_list[predict_idx])

    if choice=='a':#webcam
        cap = cv2.VideoCapture(0)
        while True:
            ret , frame = cap.read()
            cv2.putText(frame,"press s for saving photos",(50,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),1)
            cv2.imshow('frame',frame)
            if cv2.waitKey(1)&0xFF==ord('s'):  #按s键退出
                ret , frame = cap.read()
                check_detection=len(api.face_encodings(frame))>0
                if check_detection==True:
                    break
            
        cap.release()
        cv2.destroyAllWindows()            
        cv2.imwrite("webcam.jpg",frame)

        
        overall_images=[]
        overall_encodings=[]
        with_images=[]
        for i in range(0,search_num):
            if os.path.exists(str(i+1)+".jpg"):
                overall_images.append(api.load_image_file(str(i+1)+".jpg"))
            else:
                overall_images.append(-1)
        print(len(overall_images))
        for i in range(0,search_num):
            if type(overall_images[i])!=int:
                if len(api.face_encodings(overall_images[i]))>0:
                    overall_encodings.append(api.face_encodings(overall_images[i])[0])
                    with_images.append(i+1)

        original_image=api.load_image_file("webcam.jpg")
        
        if len(api.face_encodings(original_image))>0:
            face_encoding_original=api.face_encodings(original_image)[0]
        else:
            print("No face found!")
            return
        faces_to_compare = overall_encodings
        
        distance_results = api.face_distance(faces_to_compare, face_encoding_original)
        face_distances=distance_results
        for i in range(0,len(with_images)):      
            print(str(with_images[i])+":"+str(distance_results[i]))

        #face similarity starts
        mean_distance=float(float(sum(distance_results))/float(len(distance_results)))
        with_images_index={}
        for i in range(0,len(with_images)):
            with_images_index[with_images[i]]=i
        real_distance=[0.]*len(score_list)
        for i in range(0,len(score_list)):
            if (i+1) in with_images:
                real_distance[i]=distance_results[with_images_index[i+1]]
            else:
                real_distance[i]=mean_distance
                
        face_similarity=[]
        for i in range(0,len(real_distance)):
            face_similarity.append(1-real_distance[i])
        #face similarity ends
        score_list = []
        feature_weight = [1.8, 1., 1., 1., 1., 1.]
        for i in range(len(total_user_information)):
            score = 0.
            feature_cnt = 0
            for idx in range(len(input_info[:-1])):
                if total_user_information[i][idx] != 0 and total_user_information[i][idx] != '?':
                    if input_info[idx] != '?' and input_info[idx] != '':
                        feature_cnt += 1
                        score += feature_weight[idx]*cosine_similarity(total_user_information[i][idx], input_info[idx])

            similar_score = (score + 0.6*feature_cnt/len(input_info[:-1])+face_similarity[i]) / float(feature_cnt + 1+1)
            score_list.append(similar_score)
        predict_idx = score_list.index(max(score_list))
        print('Score with images: ', score_list)
        print('Result with images: ', url_list[predict_idx])
        #print(distance_results)
    elif choice=='b':
        overall_images=[]
        overall_encodings=[]
        with_images=[]
        for i in range(0,search_num):
            if os.path.exists(str(i+1)+".jpg"):
                overall_images.append(api.load_image_file(str(i+1)+".jpg"))
            else:
                overall_images.append(-1)
        print(len(overall_images))
        for i in range(0,search_num):
            if type(overall_images[i])!=int:
                if len(api.face_encodings(overall_images[i]))>0:
                    overall_encodings.append(api.face_encodings(overall_images[i])[0])
                    with_images.append(i+1)

        original_image=api.load_image_file("original.jpg")
        if len(api.face_encodings(original_image))>0:
            face_encoding_original=api.face_encodings(original_image)[0]
        else:
            print("No face found!")
            return
        faces_to_compare = overall_encodings
        
        distance_results = api.face_distance(faces_to_compare, face_encoding_original)
        face_distances=distance_results
        for i in range(0,len(with_images)):      
            print(str(with_images[i])+":"+str(distance_results[i]))

        #face similarity starts
        mean_distance=float(float(sum(distance_results))/float(len(distance_results)))
        with_images_index={}
        for i in range(0,len(with_images)):
            with_images_index[with_images[i]]=i
        real_distance=[0.]*len(score_list)
        for i in range(0,len(score_list)):
            if (i+1) in with_images:
                real_distance[i]=distance_results[with_images_index[i+1]]
            else:
                real_distance[i]=mean_distance
                
        face_similarity=[]
        for i in range(0,len(real_distance)):
            face_similarity.append(1-real_distance[i])
        #face similarity ends
        score_list = []
        feature_weight = [1.8, 1., 1., 1., 1., 1.]
        for i in range(len(total_user_information)):
            score = 0.
            feature_cnt = 0
            for idx in range(len(input_info[:-1])):
                if total_user_information[i][idx] != 0 and total_user_information[i][idx] != '?':
                    if input_info[idx] != '?' and input_info[idx] != '':
                        feature_cnt += 1
                        score += feature_weight[idx]*cosine_similarity(total_user_information[i][idx], input_info[idx])

            similar_score = (score + 0.6*feature_cnt/len(input_info[:-1])+face_similarity[i]) / float(feature_cnt + 1+1)
            score_list.append(similar_score)
        predict_idx = score_list.index(max(score_list))
        print('Score with images: ', score_list)
        print('Result with images: ', url_list[predict_idx])
        #print(distance_results)

window=tk.Tk()

#第2步，给窗口的可视化起名字
window.title('information collection')

#第3步，设定窗口的大小(长＊宽)
window.geometry('360x240')  #这里的乘是小

orig_name="?"
nickname="?"
home="?"
hometown="?"
work="?"
school="?"
birthday="?"

name_var=tk.StringVar(window)
nickname_var=tk.StringVar(window)
home_var=tk.StringVar(window)
hometown_var=tk.StringVar(window)
work_var=tk.StringVar(window)
school_var=tk.StringVar(window)
birthday_var=tk.StringVar(window)
webcam_var=tk.StringVar(window)
#第4步，在图形界面上设定标签
Label(window, text="姓名").grid(row=0)
Label(window, text="暱稱").grid(row=1)
Label(window, text="現居住地").grid(row=2)
Label(window, text="家鄉").grid(row=3)
Label(window, text="工作").grid(row=4)
Label(window, text="學校").grid(row=5)
Label(window, text="生日(yy/mm/dd)").grid(row=6)
Label(window, text="影像:a.鏡頭 b.圖片 c.無").grid(row=7)

e1 = Entry(window,textvariable = name_var)
e2 = Entry(window,textvariable = nickname_var)
e3 = Entry(window,textvariable = home_var)
e4 = Entry(window,textvariable = hometown_var)
e5 = Entry(window,textvariable = work_var)
e6 = Entry(window,textvariable = school_var)
e7 = Entry(window,textvariable = birthday_var)
e8 = Entry(window,textvariable = webcam_var)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)
e5.grid(row=4, column=1)
e6.grid(row=5, column=1)
e7.grid(row=6, column=1)
e8.grid(row=7,column=1)

button1 =Button(window,text="Submit",fg="green",width=30,command=main_function)
button1.grid(row=8, column=1)
button2 =Button(window,text="Quit",fg="red",width=30,command=window.destroy)
button2.grid(row=9, column=1)

#第6步，
window.mainloop()

