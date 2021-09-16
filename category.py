from bs4 import BeautifulSoup
import requests

r = requests.get('https://www.tokopedia.com/p')
soup = BeautifulSoup(r.text, 'html.parser')


