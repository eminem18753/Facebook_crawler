import csv
import pickle
counter=0

with open('all_friends_url.pickle', 'rb') as f:
    all_friends_url = pickle.load(f)

output=open("facebook_dataset_clean.csv","w",newline='',encoding="utf-8")
        
with open('facebook_dataset_12_31.csv', newline='',encoding="utf-8") as csvfile:
  rows = csv.reader(csvfile)
  writer=csv.writer(output)
  for row in rows:
      temp=row
      counter+=1
      flag=0
      for index in row:
          if index!="?":
              flag=1
              break
      if flag==1:
          if counter>=2:
              temp.append(all_friends_url[counter-2])
          writer.writerow(temp)
      #writer.writerow(temp)
