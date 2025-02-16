import pandas as pd
from offer_parsing_logic import parse_offer_page
import cloudscraper
from utils import get_current_datetime
pd.options.mode.copy_on_write = True

def robust_value_extraction(df, col):
    return df.get(col, pd.Series([None])).tolist()[0]

def combine_df(df_old, df_new):
    for col in df_old.columns:
        val1 = robust_value_extraction(df_old, col)
        val2 = robust_value_extraction(df_new, col)
        df_new[col] = val1 if val2 is None else val2
    
    return df_new  

search_df = pd.read_csv("data_load\\test_search_page_parsing.csv")
total_df = pd.read_csv("data_load\\old_flats_sale.csv")
already_done = set(total_df['url'])

scraper = cloudscraper.create_scraper()
for url in search_df['url']:

    if url in already_done:
        print(f"skipping {url}")
        continue

    print(f"starting {url}")
    old_df = search_df.query(f"url == '{url}'")
    photos_url = set(eval(old_df['photo_url_list'].tolist()[0])) 
    
    new_df = parse_offer_page(scraper, url, photos_url, mean_sleep = 30)
    new_df['url'] = url
    new_df['offer_page_load_dttm'] = get_current_datetime()

    fin_df = combine_df(old_df, new_df)
    total_df = pd.concat([total_df, new_df], ignore_index = True)
    
    total_df.to_csv("data_load\\old_flats_sale.csv", index = False)
