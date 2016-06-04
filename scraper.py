from threading import Thread, Lock
import sqlite3
import staff
import requests
from bs4 import BeautifulSoup
from Queue import Queue

emptyPage = u'\n\n<div class="row msht-app-list">\n    \n    \n</div>\n'

class Scraper:

    def __init__(self):
        self.output = Queue()
        self.qAppLinks = Queue()
        self.lock = Lock()



    def search(self, keyWord):
        page = 0
        address = 'http://cafebazaar.ir/search/?q=%s&l=fa&partial=true&p=%d' % (keyWord, page)
        html = self.getHTML(address)

        num_threads = 10
        if not html == emptyPage:
            for i in range(num_threads):
                worker = Thread(target=self.getFromQ)
                worker.setDaemon(True)
                worker.start()
            self.getAppLinks(html)
            t = Thread(target=self.saveToDB)
            t.setDaemon(True)
            t.start()
            self.qAppLinks.join()
            self.output.join()
        else:
            print "reached end of search"


    def getHTML(self,address):
        self.lock.acquire()
        res = requests.get(address)
        self.lock.release()
        res.raise_for_status()
        return res.text

    def getAppLinks(self, HTML):
        soup = BeautifulSoup(HTML, "html.parser")
        list = soup.findAll('div', {'class': 'msht-app'})
        for li in list:
            tmp = li.find('a').attrs['href']
            tmp2 = staff.NormalizeURL(staff.removeWhiteSpace(tmp))
            self.qAppLinks.put(tmp2)

    def getAppData(self, HTML):
        soup = BeautifulSoup(HTML, "html.parser")

        appName = soup.find('h1', {'itemprop': 'name'})
        if appName == None:
            raise "cant Find Name of App"
        appName = staff.removeWhiteSpace(appName.text)

        appCategory = soup.find('span', {'itemprop': 'applicationSubCategory'})
        if appCategory == None:
            raise "cant Find Category of App"
        appCategory = staff.removeWhiteSpace(appCategory.text)

        appPrice = soup.find('meta', {'itemprop': 'price'})
        if appPrice == None:
            raise "cant Find Price of App"
        appPrice = appPrice.attrs['content']

        appIcon = soup.find('img', {'class': 'app-img'})
        if appIcon == None:
            raise "cant Find Icon of App"
        appIcon = appIcon.attrs['src']
        appIcon = staff.NormalizeURL(appIcon)

        appURL = soup.find('meta', {'itemprop': 'url'})
        if appURL == None:
            raise "cant Find URL of App"
        appURL = appURL.attrs['content']
        appURL = staff.NormalizeURL(appURL)

        dic = {'name': appName, 'price': appPrice, 'icon': appIcon , 'url': appURL, 'category': appCategory}
        return dic
    def getFromQ(self):
        #conn = sqlite3.connect('database.db')
        while True:
            link = self.qAppLinks.get()
            try:
                html = self.getHTML(link)
                data = self.getAppData(html)
                self.output.put(data)
            except Exception as e:
                raise
            self.qAppLinks.task_done()
    def saveToDB(self):
        conn = sqlite3.connect('database.db')
        while True:
            data = self.output.get()
            query = "INSERT INTO APPS (NAME,PRICE,ICON,URL,CATEGORY) VALUES ("
            query = query + "'%s'," % (data['name'])
            query = query + "'%s'," % (data['price'])
            query = query + "'%s'," % (data['icon'])
            query = query + "'%s'," % (data['url'])
            query = query + "'%s'"  % (data['category'])
            query = query + ")"
            conn.execute(query)
            conn.commit()
            self.output.task_done()
        conn.close()

if __name__ == '__main__':
    s = Scraper()
    s.search('football')
#print s.output
