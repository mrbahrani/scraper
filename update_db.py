from baazar import appCategoryList,gameCategoryList
from sqlite3 import *
from shutil import copyfile
from threading import Thread
from scraper import Scraper


class acThread(Thread):
    def __init__(self,catagory):
        Thread.__init__(self)
        self.cat = catagory

    def run(self):
        #try:
        print "y"
        s = Scraper('en')
            #s.getCategory(self.cat)
        s.getAppList(self.cat, endPage=0)
        #except:
        #    print "n"

class gcThread(Thread):
    def __init__(self,catagory):
        Thread.__init__(self)
        self.cat = catagory

    def run(self):
        try:
            print "y"
            s = Scraper('en')
            #s.getCategory(self.cat)
            s.getGameList(self.cat, endPage=0)
        except:
            print "n"

def update_db():
    tList = []
    for itr in appCategoryList:
        t = acThread(itr)
        tList.append(t)
        t.start()
    for itr in gameCategoryList:
        t = gcThread(itr)
        tList.append(t)
        t.start()
    for itr in tList:
        itr.join()
        print "j"

update_db()
