from bs4 import BeautifulSoup
import os
import config
from scrapingant_client import ScrapingAntClient
from os.path import exists
import sqlite3

cache_file = config.cache_file("category")
db_file = config.db_file("tokped")

if not exists(cache_file) :


    client = ScrapingAntClient(token='b3fac55e1b354ad0be818ba9c80248bd')
    result = client.general_request('https://tokopedia.com/p/')
    content = result.content

    with open(cache_file,'w', encoding = 'utf-8') as f :
        f.write(content)

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
            ,parent_id INTEGER NULL
        );
      """

cur.execute(sql)

sql = "CREATE UNIQUE INDEX IF NOT EXISTS IX_url ON category(url);"

cur.execute(sql)

for link in all_links:
    #print(link)
    #print(link['href'])
    #print(type(link['href']))
    #print(link.contents[0])
    #print(type(link.contents[0]))

    href = str(link['href']).strip()
    title = str(link.contents[0]).strip()

    if href is not None and href != ""  :

        print(href)
        print(title)

        sql = f"""
                SELECT id 
                FROM category
                WHERE url = ?
              """
        row = cur.execute(sql,(href,)).fetchone()

        if row is None :


            sql = f""" 
                    INSERT INTO category(title,url)
                    VALUES(?,?);
                """
            cur.execute(sql,(title,href))

        else :

            id = row[0][0] # baris pertama , kolom id -> lihat query row

            sql = """
                    UPDATE category
                    SET title = ?
                    WHERE id = ?
                  """
            cur.execute(sql,(title,id))


con.commit()

con.close()
