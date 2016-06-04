from baazar import appCategoryList,gameCategoryList
from sqlite3 import *
from shutil import copyfile
from threading import Thread
from scraper import Scraper


class cThread(Thread):
    def __init__(self,catagory):
        Thread.__init__(self)
        self.cat = catagory

    def run(self):
        try:
            print "y"
            s = Scraper('fa')
            s.getCategory(self.cat)
        except:
            print "n"

def update_db():
    tList = []
    for itr in appCategoryList+gameCategoryList:
        t = cThread(itr)
        tList.append(t)
        t.start()
    for itr in tList:
        itr.join()
        print "j"

update_db()