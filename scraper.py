from threading import Thread, Lock
import sqlite3
import staff
import requests
from bs4 import BeautifulSoup
from Queue import Queue

emptyPage = u'\n\n<div class="row msht-app-list">\n    \n    \n</div>\n'

class Scraper:
    websiteAddress = "http://cafebazaar.ir/"
    categoryLink = "cat/%s/"
    listLink = "lists/%s/"
    searchLink = "search/?q=%s"
    page="p=%d"
    enabledPartial = "partial=true"

    bestSellingApps = "%s-best-selling-apps"
    topRatedApps = "%s-top-rated"
    newApps = "%s-new-apps"

    newBestGames = "ml-best-new-%s-games"
    topRatedGames = "all-time-great-%s-games"
    topSellingGames = "%s-top-sellers"
    topPaidSellingGames = "%s-top-sellers-iap"
    newGames = "new-%s-games"

    def __init__(self, lang='en'):
        self.lang = "l=%s" % (lang)
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
            address = staticAddress + "&" + (Scraper.page % (startPage*24))
            html = self.getHTML(address)
            if not html == emptyPage:
                self.getAppLinks(html, qAppLinks)
                startPage = startPage + 1
            else:
                break
        qAppLinks.join()
        output.join()

    def getAppList(self, category, startPage=0, endPage=0):
        staticAddress = Scraper.websiteAddress + (Scraper.listLink % (Scraper.topRatedApps % category)) + "?" + self.lang + "&" + Scraper.enabledPartial
        self.base(staticAddress, startPage, endPage)

    def getGameList(self, category, startPage=0, endPage=0):
        staticAddress = Scraper.websiteAddress + (Scraper.listLink % (Scraper.topRatedGames % category)) + "?" + self.lang + "&" + Scraper.enabledPartial
        self.base(staticAddress, startPage, endPage)

    def search(self, keyWord, startPage=0, endPage=1):
        staticAddress = Scraper.websiteAddress + (Scraper.searchLink % (keyWord)) + "&" + self.lang + "&" + Scraper.enabledPartial
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
        appPrice = int(appPrice)

        appURL = soup.find('meta', {'itemprop': 'url'})
        if appURL == None:
            raise "cant Find URL of App"
        appURL = appURL.attrs['content']
        appURL = staff.NormalizeURL(appURL)

        appPakage = staff.getPakageName(appURL)

        dic = {'name': appName, 'price': appPrice, 'pakage': appPakage , 'category': appCategory}
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
            cursor = conn.execute("SELECT * from APPS WHERE PAKAGE='%s'" % data['pakage'])
            query = ''
            if len(cursor.fetchall()) == 0:
                print "."
                query += "INSERT INTO APPS (NAME,PRICE,PAKAGE,CATEGORY) VALUES ("
                query += "'%s'," % (data['name'])
                query += "'%d'," % (data['price'])
                query += "'%s'," % (data['pakage'])
                query += "'%s'"  % (data['category'])
                query += ")"
            else:
                query += "UPDATE APPS set "
                query += "NAME='%s'," % (data['name'])
                query += "PRICE='%d'," % (data['price'])
                query += "CATEGORY='%s' "  % (data['category'])
                query += "WHERE PAKAGE='%s'" % data['pakage']
            conn.execute(query)
            conn.commit()
            q.task_done()
        conn.close()

if __name__ == '__main__':
    Scraper().getAppList('weather', endPage=2)
#print s.output
