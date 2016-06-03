from threading import Thread
#import buffer
import staff
import requests
from bs4 import BeautifulSoup
from Queue import Queue


class SThread(Thread):
    def __ini__(self):
        Thread.__init__(self)
    def run(self):
        pass

emptyPage = u'\n\n<div class="row msht-app-list">\n    \n    \n</div>\n'

class Scraper:

    def __init__(self):
        self.output = []
        self.qAppLinks = Queue()
        pass

    def start(self, keyWord):
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
            self.qAppLinks.join()
        else:
            print "reached end of search"


    def getHTML(self,address):
        res = requests.get(address)
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
        while True:
            link = self.qAppLinks.get()
            html = self.getHTML(link)
            data = self.getAppData(html)
            self.output.append(data)
            self.qAppLinks.task_done()

#s = Scraper()
#s.start('football')
#print s.output
