import sqlite3
import requests
from bs4 import BeautifulSoup
import urllib.request
import smtplib
import re
import time
import datetime
from email.message import EmailMessage
import matplotlib.pyplot as plt
import matplotlib.dates

class DB():
    def __init__(self):
        self.conn=sqlite3.connect("pro_data.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS data(name TEXT, time TEXT,price INTEGER)")

    def add(self, name, time, price):
        try:
            self.c.execute("INSERT INTO data(name, time, price) VALUES (?,?,?)",(name, time, price))
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            print("error occured while inserting values in DB")

    def retrieve(self, title):
        self.c.execute("SELECT time, price from data WHERE name=?",[str(title)])
        self.data=self.c.fetchall()
        self.c.close()
        self.conn.close()
        return(self.data)
        
def scrapescrape(url, price):
    
    req = urllib.request.Request(url, headers={"User-Agent":"Defined"})
    page = urllib.request.urlopen(req).read()
    pattern = re.compile(r'<span id="(priceblock_ourprice|priceblock_dealprice)" class="a-size-medium a-color-price"><span class="currencyINR">&nbsp;&nbsp;</span> (\d{0,2},?\d{0,2}\,?\d{1,3}).00</span>')
    matches = pattern.finditer(str(page))
    for match in matches:
        #print('Current Price: INR ' + str(match.group(2)))
        cost = (int)(match.group(2).replace(',',''))
    #print("Current price is Rs." + str(cost))
    
        
    '''pattern = re.compile(r'<span id="productTitle" class="a-size-large">\s+(Apple)\s+</span>\s+<span  id="titleEDPPlaceHolder" ></span>')
    matches = pattern.finditer(str(page))
    for match in matches:
        print(match.group(0))'''

    price = int(price)
    page = requests.get(url,headers={"User-Agent":"Defined"})
    soup = BeautifulSoup(page.content, "html.parser")
    
    title = soup.find(id = 'productTitle').get_text(strip = True)
   
    print(title + " currently available at: INR "+ str(cost))
    timestamp = datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S')
    db_data = DB()
    writer = db_data.add(str(title), str(timestamp), int(cost))
    
    x = []
    y = []
    db_data = DB()
    reader = db_data.retrieve(str(title))
    for row in reader:
        x.append(datetime.datetime.strptime(row[0],'%d-%m-%Y %H:%M:%S'))
        y.append(int(row[1]))
            
      
    dates = matplotlib.dates.date2num(x)
    plt.plot_date(dates, y,'b-')
    plt.xlabel('Time')
    plt.ylabel('Price in INR')
    plt.title('Price Graph of ' + str(title))
    plt.ion()
    plt.show()
    plt.pause(15)
    plt.close()
    if int(cost) <= int(price):
      
        subject = 'Message from Price Monitoring system'
        content = 'Subject:{Message from Price Monitoring system}\n\nPrice of ' + title + ' has been lowered!'.format(subject)
        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('ayush.eshan@gmail.com','')#login using your own gmail ID and password
        mail.sendmail('ayush.eshan@gmail.com','ayush.eshan@gmail.com',content)#sender, receiver and content
        mail.close()
