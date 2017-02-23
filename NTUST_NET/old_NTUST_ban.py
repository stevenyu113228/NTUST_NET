import time #取現在時間使用
import requests #做http Request
from bs4 import BeautifulSoup   #整理html




banurl = "http://network.ntust.edu.tw/Iprecover.aspx"
sb = requests.session()
sban1 = requests.get(banurl)
bsban1 = BeautifulSoup(sban1.text,"html.parser")

ban_data = {
    
}

ban_data['ctl00$ContentPlaceHolder1$hidfield'] = '140.118.170.49'
ban_data['ctl00$ContentPlaceHolder1$txtRecoverip'] = '140.118.170.49'
ban_data['ctl00$ContentPlaceHolder1$btnOk'] = '送出'
ban_data['__VIEWSTATE'] = ((bsban1.select('#__VIEWSTATE')[0])['value'])
ban_data['__VIEWSTATEGENERATOR'] = ((bsban1.select('#__VIEWSTATEGENERATOR')[0])['value'])
ban_data['__EVENTVALIDATION'] = ((bsban1.select('#__EVENTVALIDATION')[0])['value'])

sban2 = requests.post(banurl,data = ban_data)
bsban2 = BeautifulSoup(sban2.text,"html.parser")
bantable = bsban2.find_all('td')
bantable  = str((bantable[3].select("span"))[0])
bantable = bantable[bantable.find('>')+1:]
bantable = bantable[:bantable.find('<')]
print (bantable)