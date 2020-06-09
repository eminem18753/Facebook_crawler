import os
import re
import json
import csv
from mtranslate import translate

def is_Chinese(uchar):         
    if '\u4e00' <= uchar<='\u9fff':
        return True
    else:
        return False

def translate_dataset(word):
    if is_Chinese(word)==False and word!="?":
        result=translate(word, 'zh-TW','auto')
    else:
        result=word
    return result

output=open("facebook_dataset_final_version.csv","w",newline='',encoding="utf-8")
counter=0
with open('facebook_dataset_traditional_1_12.csv', newline='',encoding="utf-8") as csvfile:
    writer=csv.writer(output)
    writer.writerow(['姓名','暱稱','現居住地','家鄉','工作','學校','網址'])
    
    rows = csv.reader(csvfile)
    
    for row in rows:
        temp=[]
        if counter!=0:
            live_places=row[2]
            hometowns=row[3]
            jobs=row[4]
            schools=row[5]
    
            ch_live_places=translate_dataset(live_places)
            ch_hometowns=translate_dataset(hometowns)
            ch_jobs=translate_dataset(jobs)
            ch_schools=translate_dataset(schools)

            temp.append(row[0])
            temp.append(row[1])
            temp.append(ch_live_places)
            temp.append(ch_hometowns)
            temp.append(ch_jobs)
            temp.append(ch_schools)
            temp.append(row[-1])
            writer.writerow(temp)
            
        counter+=1
        print(counter)

        