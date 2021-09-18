from bs4 import BeautifulSoup
import os
import config
from scrapingant_client import ScrapingAntClient
from os.path import exists

cache_file = config.cache_file("category")

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


for link in all_links:
    print(link)
    print(link['href'])
    print(link.contents[0])
