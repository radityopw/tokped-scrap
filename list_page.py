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


try :

    cur = con.cursor()

    sql = """
            CREATE TABLE IF NOT EXISTS list_page (
                 id INTEGER PRIMARY KEY AUTOINCREMENT
                ,category_id INTEGER
                ,title TEXT COLLATE NOCASE NULL
                ,url TEXT COLLATE NOCASE
                ,FOREIGN KEY(category_id) REFERENCES category(id)
            );
          """
          
    cur.execute(sql)

    sql = """
            CREATE UNIQUE INDEX IF NOT EXISTS IX_url ON list_page(url);
          """
          
    cur.execute(sql)


    sql = "SELECT id,url FROM category"
    list_category = cur.execute(sql).fetchall()

    for category in list_category :
        category_id = category[0]
        category_url = category[1]
        cache_file = config.cache_file("list_page_"+str(category_id))
        
        logging.info("scrapping id "+str(category_id)+" "+category_url)

        content = ""

        if not exists(cache_file) :
            scrap.scrap_this(category_url,cache_file)
       
        with open(cache_file,'r', encoding = 'utf-8') as f :
            content = f.read()
            
        soup = BeautifulSoup(content,features="html.parser")
        all_links = soup.find_all('a')
        
        for link in all_links:
        
            #logging.debug(link)
            
            href = str(link['href']).strip().lower()
            
            try :
                title = str(link.contents[0]).strip().lower()
            except Exception as e :
                continue
            
            if href is not None and "?whid=0" in href :
            
                href = href.split("?")[0]
                
                logging.debug("process "+href)
            
                sql = """
                        SELECT id
                        FROM list_page
                        WHERE url = ?
                      """
                row = cur.execute(sql,(href,)).fetchone()
                
                if row is None :
                    logging.debug("INSERT MODE")
                    
                    sql = """
                            INSERT INTO list_page(category_id,title,url)
                            VALUES(?,?,?)
                          """
                    
                    cur.execute(sql,(category_id,title,href))
                    
                    id = cur.lastrowid
                    
                else : 
                    logging.debug("UPDATE MODE")
                    
                    id = row[0]
                    
                    
                    sql = """
                            UPDATE list_page
                            SET title = ?
                            WHERE id = ?
                          """
                    
                    cur.execute(sql,(title,id))
                

    con.commit()

except Exception as ex1 :
    logging.error(ex1)
    con.rollback()

finally :
    con.close()