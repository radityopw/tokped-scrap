from bs4 import BeautifulSoup
import os
import config
from scrapingant_client import ScrapingAntClient
from os.path import exists
import sqlite3
import logging
import scrap


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


logging.info("starting list_page")

db_file = config.db_file("tokped")
  

con = sqlite3.connect(db_file)
cur = con.cursor()


sql = "SELECT id,url FROM category"
list_category = cur.execute(sql).fetchall()

for category in list_category :
    id = category[0]
    url = category[1]
    cache_file = config.cache_file("list_page_"+str(id))

    if not exists(cache_file) :
        scrap.scrap_this(url,cache_file)
   
    #with open(cache_file,'r', encoding = 'utf-8') as f :
    #    content = f.read()




con.commit()

con.close()
