import os
import pandas as pd
import shutil
import cloudscraper
from search_parsing_logic import(
    parse_all_search_results
)

search_pages_dict = {"test_search": "https://www.cian.ru/cat.php?currency=2&deal_type=sale&district%5B0%5D=10&electronic_trading=2&engine_version=2&minprice=40000000&object_type%5B0%5D=1&offer_type=flat&only_flat=1"}

df = pd.read_csv("data_load\\test_search_page_parsing.csv")
already_parsed = df['search_alias']
search_pages_dict_filtered = {alias: url 
                              for alias, url in search_pages_dict.items() 
                              if alias not in already_parsed
                             }

scraper = cloudscraper.create_scraper()
path = "data_load\\old_flats_sale_search"
for search_alias, url in search_pages_dict_filtered.items():
        
    df = parse_all_search_results(scraper, url, search_alias, save_to = "data_load\\old_flats_sale_search", sleep_mean=-40)
    df['search_alias'] = search_alias
    
    df.to_csv("data_load\\test_search_page_parsing.csv", index=False)
