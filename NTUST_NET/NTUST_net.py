import os 
import time #取現在時間使用
import requests #做http Request
from bs4 import BeautifulSoup   #整理html

print("") #保持美觀，空一行
try:
    your_ip = requests.get("http://api.ipify.org/").text
    your_ip = str(your_ip) #get ip
    if len(your_ip)>100:
        your_ip = "抓不到本機ip,疑似被封鎖或網路線未接妥!!!"
        exit()
except:
    print("抓不到本機ip,疑似被封鎖或網路線未接妥!!!")
    exit()


#Get now time
time_now = time.localtime(time.time())
str_time = str(time_now[0]) + " 年 " + str(time_now[1]) + " 月 " + str(time_now[2]) + " 日 " #time string

#Print time and ip
print("今天是 : "+str_time)
print("您的ip為 : " + your_ip)

yn_ip = input("是否使用您的ip位置? (Y/N): ")
if yn_ip == 'n' or yn_ip == 'N':
    ip = input("請需要查詢的ip : ")
else:
    ip = your_ip

yn_date = input("是否使用現在日期?(Y/N) : ")
if yn_date == 'n' or yn_date == 'N':
    yy = input("請輸入查詢年份 : ")
    mm = input("請輸入查詢月份 : ")
    dd = input("請輸入查詢日期 : ")
else:
    yy = time_now[0]
    mm = time_now[1]
    dd = time_now[2]

url = "http://network.ntust.edu.tw/flowstatistical.aspx"    #台科的取流量網址
s = requests.session()  #紀錄session
res1 = s.get(url)   #第一次get學校網址，存session跟post雜項
bs1 = BeautifulSoup(res1.text,"html.parser")    #BS整理get的值

#Post Const
postdata = {}   #post出去的資料
postdata['__EVENTTARGET'] = ""  
postdata['__EVENTARGUMENT'] = ""    
postdata['__LASTFOCUS'] = ""    
postdata['ctl00$ContentPlaceHolder1$btnview'] = '檢視24小時流量'  
postdata['ctl00$ContentPlaceHolder1$dlcunit'] = '1'     #取bytes的單位

#Post Variable
postdata['__VIEWSTATE'] = ((bs1.select('#__VIEWSTATE')[0])['value'])
postdata['__VIEWSTATEGENERATOR'] = ((bs1.select('#__VIEWSTATEGENERATOR')[0])['value'])
postdata['__EVENTVALIDATION'] = ((bs1.select('#__EVENTVALIDATION')[0])['value'])


#將欲查詢的日期及時間存入Dict
postdata['ctl00$ContentPlaceHolder1$txtip'] = ip
postdata['ctl00$ContentPlaceHolder1$dlyear'] = yy
postdata['ctl00$ContentPlaceHolder1$dlmonth'] = mm
postdata['ctl00$ContentPlaceHolder1$dlday'] = dd

print("查詢中請稍後......\n")

#Post data to server
res2 = s.post(url,data = postdata)
bs2 = BeautifulSoup(res2.text,'html.parser')

#整理Table內容
table = bs2.find("table", {"class" : "CSSTableGenerator"})
cells = []
for row in table.findAll("tr"):
    cells = row.findAll("td")

#懶得用正規表達，直接把不必要的替換成空白(等於刪除)
total = str(cells[3])
total = total.replace(",","")
total = total.replace("<td>","")
total = total.replace("(bytes)","")
total = total.replace(" ","")
total = total.replace("</td>","")
total = total.replace("\n","")

total = int(total) #當前已使用的Bytes數

#用list記錄各單位的 單位、總量、5G亮
size = ['B','KB','MB','GB']
total_size = [total,total/1024,total/(1024*1024),total/(1024*1024*1024)]
fiveG_size = [5*1024*1024*1024,5*1024*1024,5*1024,5]


#print result
print("當前已使用了 : ")
for s in range(0,4):
    print(str(total_size[s])+ " " + size[s])

print("\n還剩下 :")
for s in range(0,4):
    print(str(fiveG_size[s]-total_size[s])+ " " + size[s])

#檢查停權
banurl = "http://network.ntust.edu.tw/Iprecover.aspx"
sb = requests.session()
sban1 = requests.get(banurl)
bsban1 = BeautifulSoup(sban1.text,"html.parser")
ban_data = {}
ban_data['ctl00$ContentPlaceHolder1$hidfield'] = ip
ban_data['ctl00$ContentPlaceHolder1$txtRecoverip'] = ip
ban_data['ctl00$ContentPlaceHolder1$btnOk'] = '送出'
ban_data['__VIEWSTATE'] = ((bsban1.select('#__VIEWSTATE')[0])['value'])
ban_data['__VIEWSTATEGENERATOR'] = ((bsban1.select('#__VIEWSTATEGENERATOR')[0])['value'])
ban_data['__EVENTVALIDATION'] = ((bsban1.select('#__EVENTVALIDATION')[0])['value'])
sban2 = requests.post(banurl,data = ban_data)
bsban2 = BeautifulSoup(sban2.text,"html.parser")
bantable = bsban2.find_all('td')
bantable  = str((bantable[3].select("span"))[0])
bantable = bantable[(bantable.find('>'))+1:]
bantable = bantable[:bantable.find('<')]
print ("\n",bantable)
print("\n感謝您使用台科大流量查詢軟體V1.0\n作者:游照臨\n")

os.system("pause")
