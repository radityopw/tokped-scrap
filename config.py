import os

def dir_location():
    return "/tmp"

def cache_file(filename):
    return dir_location()+"/tokped_scrap_"+filename

def db_file(filename):
    return dir_location()+"/tokped_scrap_db_"+filename

def engine():
    # scrapingant
    # php
    return "php"

def scrapingant_token():
    return os.environ['TOKPED_SCRAP_SCRAPINGANT_TOKEN']

def php_scrap():
    return "php -f scrap.php"
