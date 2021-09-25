from scrapingant_client import ScrapingAntClient
import config
import os
import logging


def scrap_this(url,cache_file):

    logging.info("creating cache file for "+url+" to "+cache_file)

    content = ""
    
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


