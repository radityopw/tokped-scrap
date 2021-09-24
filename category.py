from bs4 import BeautifulSoup
import os
import config
from scrapingant_client import ScrapingAntClient
from os.path import exists
import sqlite3
import logging

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)


logging.info("starting category")

cache_file = config.cache_file("category")
db_file = config.db_file("tokped")

if not exists(cache_file) :

    logging.info("creating cache file")

    content = ""
    url = "https://tokopedia.com/p/"

    logging.info("using "+config.engine()+" engine")

    if config.engine() == "scrapingant" :

        client = ScrapingAntClient(token=config.scrapingant_token())
        result = client.general_request(url)
        content = result.content
        with open(cache_file,'w', encoding = 'utf-8') as f :
            if content is not "" :
                f.write(content)

    if config.engine() == "php" :
        os.system(config.php_scrap()+" "+url+" > "+cache_file)

    
with open(cache_file,'r', encoding = 'utf-8') as f :
    content = f.read()


soup = BeautifulSoup(content,features="html.parser")
all_links = soup.find_all('a')

con = sqlite3.connect(db_file)
cur = con.cursor()

sql = """
        CREATE TABLE IF NOT EXISTS category (
             id INTEGER PRIMARY KEY AUTOINCREMENT
            ,title TEXT COLLATE NOCASE NULL
            ,url TEXT COLLATE NOCASE
        );
      """

cur.execute(sql)

sql = "CREATE UNIQUE INDEX IF NOT EXISTS IX_url ON category(url);"

cur.execute(sql)



sql = """
        CREATE TABLE IF NOT EXISTS category_level (
             category_id INTEGER
            ,level INTEGER 
            ,title TEXT COLLATE NOCASE
            ,PRIMARY KEY(category_id,level)
            ,FOREIGN KEY(category_id) REFERENCES category(id)
        );
      """

cur.execute(sql)


for link in all_links:
    href = str(link['href']).strip().lower()
    title = str(link.contents[0]).strip().lower()
    header_link = "https://www.tokopedia.com/p/" 

    if href is not None and header_link in href  :

        href_short = href.replace(header_link,"")

        href_level = href_short.split("/")

        logging.info("process "+href+" and title "+title)

        logging.info("href level : "+str(href_level))


        sql = f"""
                SELECT id 
                FROM category
                WHERE url = ?
              """

        logging.debug(sql)

        row = cur.execute(sql,(href,)).fetchone()

        if row is None :

            logging.debug("insert mode")


            sql = f""" 
                    INSERT INTO category(title,url)
                    VALUES(?,?);
                """
            cur.execute(sql,(title,href))

            id = cur.lastrowid

        else :

            logging.debug("update mode")

            id = row[0] # baris pertama , kolom id -> lihat query row

            sql = """
                    UPDATE category
                    SET title = ?
                    WHERE id = ?
                  """
            cur.execute(sql,(title,id))

        sql = """
                DELETE FROM category_level 
                WHERE category_id = ?
              """
        cur.execute(sql,(id,))

        level = 1

        for level_title in href_level :

            sql = """
                    INSERT INTO category_level(category_id,level,title)
                    VALUES(?,?,?)
                  """
            cur.execute(sql,(id,level,level_title))

            level = level + 1


con.commit()

con.close()
