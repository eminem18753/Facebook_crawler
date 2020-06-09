#####皆在windows系統上執行(windows 10) <br />
##分析與training環境: <br />
1.安裝selenium環境，並下載對應的firefox geckodriver.exe放在對應的路徑。 <br />
2.使用software client加上VPNGate避免ip被封鎖 <br />
3.安裝urllib.request套件 <br />
4.安裝requests_html套件以及bs4 <br />
5.安裝opencc(將簡體字轉換為繁體字) <br />
6.安裝mtranslate，提供在壓縮檔中 <br /><br />

##分析與training執行流程: <br />
1.執行facebook_crawling.py，產生用戶所有朋友的朋友的facebook個人檔案的url pickle檔 <br />
2.接著執行crawling_name.py讀取所有的url，取得使用者的每位朋友的包含工作、學校及家鄉等的個人資訊 <br />
3.再來執行dataset_questionmark_processing.py，將多餘的資料去除(即只有提供名字的資料需去除) <br />
4.執行language_processing.py，判斷使用者是否有使用暱稱。若無暱稱則暱稱為中文名轉為漢語拼音(eg.王小明->Wang Xiao Ming)。 <br />
5.接著執行simple_to_traditional.py，進行簡體字轉繁體。 <br />
6.執行translation.py，將所有的英文字通過mtranslate的API轉換為中文繁體。可以產生最終的輸出檔案:"facebook_dataset_final_version.csv" <br /><br />

##驗證碼訓練流程: <br />
1.cd到train_captcha當中 <br />
2.執行python train_captcha.py <br />
3.便可以獲得名為hack.pth的模型用做後續的驗證碼破解 <br /><br />

##線上搜尋程式(主程式)環境: <br />
1.使用tkinter圖像化介面開發 <br />
2.安裝urllib、requests以及bs4 <br />
3.安裝pandas <br />
4.安裝jieba中文斷字套件 <br />
5.使用importlib避免編碼問題 <br />
6.安裝python的opencv套件:需要import cv2 <br />
7.安裝face_recognition、face_recognition_model和dlib (19.8以上版本)，透過各自的setup.py，皆提供在壓縮檔中 <br />
8.需要安裝Visual studio 2015、Visual studio C++以及Cmake 3.13(最新版本)以便dlib進行安裝時的編譯 <br />
9.將captcha.py和hack.pth放在同1個資料夾 <br />
10.需要安裝gensim套件，以對相似字進行分析(用於載入wikipedia文字資料庫) <br />
11.需要安裝selenium代理機器人，下載對應的firefox geckodriver.exe放在對應的路徑 <br />
12.需要安裝windows上的pytorch環境(用作訓練驗證碼資料庫和破解) <br /><br />

##線上搜尋程式(主程式)執行流程: <br />
1.執行user_interface.py <br />
注意:若讀不到攝影機可以將user_interface.py中的第412行的cv2.VideoCapture(1)中的1改為0或是其他的camera id(看裝置管理員) <br /><br />

##環境: <br />
1.需安裝face_recognition_models <br />
->https://github.com/ageitgey/face_recognition_models/tree/master/face_recognition_models <br />
2.需安裝face_recognition <br />
->https://github.com/ageitgey/face_recognition <br />
->環境依賴為Click>=6.0、dlib>=19.3.0、numpy、Pillow以及scipy>=0.17.0 <br />
3.需安裝mtranslate <br />
->https://github.com/mouuff/mtranslate/tree/master/mtranslate <br />
4.需安裝opencc-python <br />
->https://github.com/yichen0831/opencc-python <br />
5.需安裝vpngate-client <br />
->https://www.vpngate.net/cn/download.aspx <br />
6.需安裝word2vec-tutorial <br />
->https://github.com/zake7749/word2vec-tutorial <br />
8.需下載geckodriver.exe
