from threading import Thread, Lock
import sqlite3
import staff
import requests
from bs4 import BeautifulSoup
from Queue import Queue

emptyPage = u'\n\n<div class="row msht-app-list">\n    \n    \n</div>\n'

class Scraper:

    def __init__(self, lang='en'):
        self.websiteAddress = "http://cafebazaar.ir/"
        self.categoryLink = "cat/%s/"
        self.listLink = "lists/%s/"
        self.bestSelling = "-best-selling-apps"
        self.topRated = "-top-rated"
        self.newApps = "weather-new-apps"
        self.searchLink = "search/?q=%s"
        self.lang = "l=%s" % (lang)
        self.enabledPartial = "partial=true"
        self.icon = "1/upload/icons/%s.png"
        self.page="&p=%d"
        self.lock = Lock()

    def base(self, staticAddress, startPage, endPage):
        output = Queue()
        qAppLinks = Queue()

        num_threads = 10
        for i in range(num_threads):
            worker = Thread(target=self.getFromQ, args=(qAppLinks, output,))
            worker.setDaemon(True)
            worker.start()

        t = Thread(target=self.saveToDB, args=(output,))
        t.setDaemon(True)
        t.start()

        while startPage <= endPage:
            address = staticAddress + (self.page % startPage)
            html = self.getHTML(address)
            if not html == emptyPage:
                self.getAppLinks(html, qAppLinks)
                startPage = startPage + 1
            else:
                break
        qAppLinks.join()
        output.join()

    def getCategory(self, category, startPage=0, endPage=0):
        staticAddress = self.websiteAddress + (self.listLink % (category+self.topRated)) + "?" + self.lang + "&" + self.enabledPartial
        self.base(staticAddress, startPage, endPage)

    def search(self, keyWord, startPage=0, endPage=1):
        staticAddress = self.websiteAddress + (self.searchLink % (keyWord)) + "&" + self.lang + "&" + self.enabledPartial
        self.base(staticAddress, startPage, endPage)


    def getHTML(self,address):
        self.lock.acquire()
        res = requests.get(address)
        self.lock.release()
        res.raise_for_status()
        return res.text

    def getAppLinks(self, HTML, q):
        soup = BeautifulSoup(HTML, "html.parser")
        list = soup.findAll('div', {'class': 'msht-app'})
        for li in list:
            tmp = li.find('a').attrs['href']
            tmp2 = staff.NormalizeURL(staff.removeWhiteSpace(tmp))
            q.put(tmp2)

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

    def getFromQ(self, qIn, qOut):
        #conn = sqlite3.connect('database.db')
        while True:
            link = qIn.get()
            try:
                html = self.getHTML(link)
                data = self.getAppData(html)
                qOut.put(data)
            except Exception as e:
                raise
            qIn.task_done()
    def saveToDB(self, q):
        conn = sqlite3.connect('database.db')
        while True:
            data = q.get()
            query = "INSERT INTO APPS (NAME,PRICE,ICON,URL,CATEGORY) VALUES ("
            query = query + "'%s'," % (data['name'])
            query = query + "'%s'," % (data['price'])
            query = query + "'%s'," % (data['icon'])
            query = query + "'%s'," % (data['url'])
            query = query + "'%s'"  % (data['category'])
            query = query + ")"
            conn.execute(query)
            conn.commit()
            q.task_done()
        conn.close()

if __name__ == '__main__':
    s = Scraper('fa')
    s.getCategory('weather')
#print s.output
