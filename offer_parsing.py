import pandas as pd
from offer_parsing_logic import parse_offer_page
import cloudscraper
import requests
from utils import get_current_datetime, random_sleep, time_print
pd.options.mode.copy_on_write = True

def robust_value_extraction(df, col):
    return df.get(col, pd.Series([None])).tolist()[0]

def combine_df(df_old, df_new):
    for col in df_old.columns:
        val1 = robust_value_extraction(df_old, col)
        val2 = robust_value_extraction(df_new, col)
        df_new[col] = val1 if val2 is None else val2
    
    return df_new  

def try_parse_offer_page(scraper, url, photos_url, mean_sleep = 3, try_cnt = 0):
    try:
        return parse_offer_page(scraper, url, photos_url, mean_sleep = mean_sleep)

    except (requests.exceptions.ConnectionError, KeyError) as e:
            
        is_con_error = 'Remote end closed connection without response' in str(e) 
        is_key_agent_error = str(e) == "'agent'"
        time_print(f"error: {str(e)}")

        if (is_con_error or is_key_agent_error) and try_cnt < 1:
            time_print("retrying after some sleep")
            random_sleep(-100, 5)
            return try_parse_offer_page(scraper, url, photos_url, mean_sleep = mean_sleep, try_cnt = try_cnt + 1)

        raise


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
    
    new_df = try_parse_offer_page(scraper, url, photos_url)
    new_df['url'] = url
    new_df['offer_page_load_dttm'] = get_current_datetime()

    fin_df = combine_df(old_df, new_df)
    total_df = pd.concat([total_df, fin_df], ignore_index = True)
    
    total_df.to_csv("data_load\\old_flats_sale.csv", index = False)
