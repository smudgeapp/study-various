import scrapy
import logging
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.remote_connection import LOGGER
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
from scrapy import signals
from selenium.webdriver.common.by import By
import time
import os
from os.path import exists
import json
import pickle
from crochet import setup
from tkinter import *


class LoadWrapper:
    chrome_options = Options()
    chrome_options.add_argument("--log-level=5")
    LOGGER.setLevel(logging.WARNING)
    driverpath = '[add crhomedriver path]'
    driver = webdriver.Chrome(executable_path=str(driverpath),\
                              options=chrome_options)
    url_list = []
    term = ""
    stat_lab = None
    url_file = "url_file"
    


    def __init__(self):
        self.driver.get("https://www.google.com")

    def setStatVar(self, label):
        self.stat_lab = label
        self.stat_lab.config(text="Stats show here.")

    def saveUrls(self):
        ex_urls = []
        if exists(self.url_file):
            with open(self.url_file, 'rb') as f:
                ex_urls = pickle.load(f)
        ex_urls = ex_urls + self.url_list
        nl = list(dict.fromkeys(ex_urls))
        with open(self.url_file, 'wb') as f:
            pickle.dump(nl, f)
        saved = u'Saved URLs = %s' % str(len(nl))
        self.stat_lab.config(text=saved)

    def updateUrls(self):
        ex_urls = []
        if exists(self.url_file):
            with open(self.url_file, 'rb') as f:
                ex_urls = pickle.load(f)
        self.url_list = self.url_list + ex_urls
        nl = list(dict.fromkeys(self.url_list))
        self.url_list = nl
        updated = u'URL List Updated = %s' % str(len(self.url_list))
        self.stat_lab.config(text=updated)
           
    def getUrls(self, link_no):
        xpath = '//*[contains(@class, "yuRUbf")]/a'
        pgNo = '1'
        try:
            pgNo = self.driver.find_element(By.CLASS_NAME, 'YyVfkd').text
        except:
            pgNo = '1'
        results = self.driver.find_elements(By.XPATH, xpath)
        link_list = self.getLinkList(link_no)        

        for i, link in enumerate(results):
            url = link.get_attribute('href')
            if len(link_list) > 0:
                if i in link_list:
                    print(url)
                    self.url_list.append(url)
            else:
                print(url)
                self.url_list.append(url)

        
        stat_str = u'Term = %s; URLs = %s; Page # %s' \
        % (self.term, str(len(self.url_list)), pgNo)
        if self.stat_lab:
            self.stat_lab.config(text=stat_str)
        
    def getLinkList(self, link_nos):
        link_str = link_nos.get()
        rngs = []
        if len(link_str) > 0:
            rngs = link_str.split(',')
        fin_rng = []
        for i, val in enumerate(rngs):
            if '-' in val:
                rng = [int(x) for x in val.split('-')]
                addrng = list(range(rng[0], rng[1]+1))
                fin_rng = fin_rng + addrng
            else:
                fin_rng.append(int(val))

        return fin_rng

    def executeSearch(self, term, before, after):
        self.term = term.get().split('|')[0]
        search_term = term.get() + " site:brecorder.com/news"
        if len(before.get()) > 0:
            search_term = search_term + " before:" + before.get()
        if len(after.get()) > 0:
            search_term = search_term + " after:" + after.get()
        print(search_term)
        s_input = self.driver.find_element(By.NAME, 'q')
        s_input.clear()
        s_input.send_keys(search_term)
        s_input.send_keys(Keys.ENTER)

    def runSpider(self):
        runner = CrawlerRunner(settings={
            "FEEDS": {        
                "br_corpus.json": {"format": "json",
                        "fields": ["count", "date", "url", "article"],
                        "item_export_kwargs": {
                               "export_empty_fields": False,
                            }}
                        },
            "BOT_NAME": "brspider",
            "CONCURRENT_REQUESTS_PER_DOMAIN": 16,
            "DOWNLOAD_DELAY": 5,
            "AUTOTHROTTLE_ENABLED": True
            })
        runner.crawl(brSpider, self.url_list)
       

    def reset(self):
        self.url_list.clear()
        self.stat_lab.config(text="URLs Reset.")
        print("\nList cleared ", len(self.url_list))

    def closeWrapper(self):
        self.driver.quit()

class brSpider(scrapy.Spider):
    name = "brspider"
    start_urls = []
    articleCt = 0
    

    def __init__(self, urls=None):
        logging.getLogger('scrapy').setLevel(logging.WARNING)
        print("init enter")
        setup()
        if urls:
            self.start_urls = urls
            
        print("end init")

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super(brSpider, cls).from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.spiderFinished, signal=signals.spider_closed)
        return spider


    def spiderFinished(self):
        print("\nspider finished")
        
    

    def start_requests(self):
        print("start reqs = ", len(self.start_urls))
        
        for url in self.start_urls:
            yield scrapy.Request(url=url, callback=self.parse_article)  


    def parse_article(self, response):
        print("---in parse article---", self.articleCt)
       
        content = ""
        story = response.xpath("//div[contains(normalize-space(@class)," + 
                "'story__content')]/p/text()")
        if story:
            print("story found", self.articleCt)
            date = response.xpath("//span[contains(normalize-space(@class)," + 
                "'story__time')]/span[contains(normalize-space(@class)," + 
                "'timestamp--date')]/text()").get()
            for p in story:
                if len(p.get()) < 35:
                    continue
                else:                    
                    content += p.get() + ' '
            if len(content) > 0:
                self.articleCt += 1
                yield {
                    "count": self.articleCt,
                    "date": date,
                    "url": response.url,
                    "article": content 
                    }
        else:
            print("story not found")


def closeProgram():
    loader.closeWrapper()
    top.destroy()


loader = LoadWrapper()

top = Tk()
top.title('BR Scraper')
top.protocol('WM_DELETE_WINDOW', closeProgram)

top.geometry("400x600")
top.grid_columnconfigure(1, weight=1)
top.grid_columnconfigure(2, weight=1)

srch_term = StringVar()
before = StringVar()
after = StringVar()
links = StringVar()



term = Entry(top, textvariable=srch_term)
term.grid(row=0, column=2, columnspan=2, sticky='WE', pady=10)

term_lab = Label(top, text='Search')
term_lab.grid(row=0, column=1, columnspan=1, sticky='WE', pady=10)

before_ent = Entry(top, textvariable=before)
before_ent.grid(row=1, column=2, columnspan=2, sticky='WE', pady=10)

before_lab = Label(top, text='Before')
before_lab.grid(row=1, column=1, columnspan=1, sticky='WE', pady=10)

after_ent = Entry(top, textvariable=after)
after_ent.grid(row=2, column=2, columnspan=2, sticky='WE', pady=10)

after_lab = Label(top, text='After')
after_lab.grid(row=2, column=1, columnspan=1, sticky='WE', pady=10)

search = Button(top, text="Search",
            command=lambda : loader.executeSearch(srch_term, before, after),
                pady=10)
search.grid(row=3, column=1, columnspan=2, stick='EW', pady=10)

linkNo_lab = Label(top, text='Link No.s')
linkNo_lab.grid(row=4, column=1, columnspan=1, sticky='WE', pady=10)

linkNo = Entry(top, textvariable=links)
linkNo.grid(row=4, column=2, columnspan=2, stick='WE', pady=10)

getLinks = Button(top, text="Get URLs",
                  command=lambda: loader.getUrls(links), pady=10)
getLinks.grid(row=5, column=1, columnspan=2, sticky='EW', pady=10)

save_urls = Button(top, text="Save URLs", command=loader.saveUrls, pady=10)
save_urls.grid(row=6, column=1, columnspan=1, sticky='WE', pady=10)

update_urls = Button(top, text="Update URLs", command=loader.updateUrls, pady=10)
update_urls.grid(row=6, column=2, columnspan=1, sticky='WE', pady=10)

runSpider = Button(top, text="Get Articles", command=loader.runSpider, pady=10)
runSpider.grid(row=7, column=1, columnspan=2, sticky='EW', pady=10)

reset = Button(top, text="Reset", command=loader.reset, pady=10)
reset.grid(row=8, column=1, columnspan=2, sticky='EW', pady=10)

stat_lab = Label(top, text="")
stat_lab.grid(row=9, column=1, columnspan=2, sticky='WE', pady=10)

loader.setStatVar(stat_lab)

