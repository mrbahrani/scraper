from threading import Thread
#import buffer
import staff
import requests
from bs4 import BeautifulSoup
import json
import Queue


class SThread(Thread):
    def __ini__(self):
        Thread.__init__(self)
    def run(self):
        pass
emptyPage = """
<html><head>
<meta http-equiv="content-type" content="text/html; charset=UTF-8"></head><body><div class="row msht-app-list">


</div>
</body></html>
"""
#emptyPage is Not correct
class Scraper:

    def __init__(self):
        self.output = []
        pass

    def start(self, keyWord):
        page = 0
        address = 'http://cafebazaar.ir/search/?q=%s&l=fa&partial=true&p=%d' % (keyWord, page)
        html = self.getHTML(address)
        if not html == emptyPage:
            linkList = self.getAppLinks(html)
            for link in linkList:
                try:
                    html = self.getHTML(link)
                    out = self.getAppData(html)
                    self.output.append(out)
                except Exception as e:
                    raise
                else:
                    pass


    def getHTML(self,address):
        res = requests.get(address)
        res.raise_for_status()
        return res.text

    def getAppLinks(self, HTML):
        soup = BeautifulSoup(HTML, "html.parser")
        list = soup.findAll('div', {'class': 'msht-app'})
        output = []
        for li in list:
            tmp = li.find('a').attrs['href']
            output.append(staff.NormalizeURL(staff.removeWhiteSpace(tmp)))
        return output

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

# = Scraper()
#s.start('football')
#print s.output
