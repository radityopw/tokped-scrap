from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import os

# Instantiate options
opts = Options()
# opts.add_argument(" — headless") # Uncomment if the headless version needed
opts.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

# Set the location of the webdriver
chrome_driver = r"C:\apps\chromedriver\chromedriver.exe"

# Instantiate a webdriver
driver = webdriver.Chrome(options=opts, executable_path=chrome_driver)

# Load the HTML page
driver.get("https://tokopedia.com/p/")

# Parse processed webpage with BeautifulSoup
soup = BeautifulSoup(driver.page_source)
all_links = soup.find_all('a')

driver.close()

print(all_links)