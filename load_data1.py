import web_scrape1
import schedule
import sqlite3
class DB():
    def __init__(self):
        self.conn=sqlite3.connect("url_data.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS data(url TEXT,price INTEGER)")

    def add(self, url, price):
        try:
            self.c.execute("INSERT INTO data(url, price) VALUES (?,?)",(url, price))
            self.conn.commit()
            self.c.close()
            self.conn.close()
        except Exception:
            print("error occured while inserting values in DB")

    def retrieve(self):
        self.c.execute("SELECT * from data")
        self.data=self.c.fetchall()
        self.c.close()
        self.conn.close()
        return(self.data)
        
def fun():
    db = DB()
    data = db.retrieve()
    for row in data:
        web_scrape1.scrapescrape(row[0], row[1])

if __name__ == '__main__':
    print('Press y to enter a new url in the database or press n to continue scraping the data')
    n = 'y'
    while True:
        n = input('Enter(y/n):')
        if n == 'y' or n == 'yes':
            url = input('Enter url here: ')
            price = input('Enter price you want it at here: ')
            db = DB()
            db.add(url,price)
        else:
            print('Monitoring price...')
            fun()
            break
    schedule.every(5).seconds.do(fun)
    while 1:
        schedule.run_pending()
        #time.sleep(1)
