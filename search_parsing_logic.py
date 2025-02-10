import pandas as pd
from json_keys_lists import search_keys_meta_list
from math import ceil
from utils import (
    time_print,
    random_sleep,
    load_offer_json,
    add_json_values
)

#url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&district%5B0%5D=10&electronic_trading=2&engine_version=2&minprice=40000000&object_type%5B0%5D=1&offer_type=flat&only_flat=1"

def process_single_offer_card(offer):
    single_ad_df = pd.DataFrame()

    #from json_keys_lists import keys_meta_list
    json_list = [offer, 
                 offer['geo'], 
                 offer['building'], 
                 offer['bargainTerms']
                ]

    for json, keys_list in zip(json_list, search_keys_meta_list):
        single_ad_df = add_json_values(single_ad_df, json, keys_list)

    single_ad_df['cian_price_range'] = offer['goodPrice']['estimationRange'] if 'goodPrice' in offer.keys() else None
    single_ad_df['photo_url_list'] = str([x['fullUrl'] for x in offer['photos']])

    return single_ad_df


def parse_all_search_results(scraper, url, sleep_mean = 30, sleep_var = 5):
    offers_json = load_offer_json(scraper, url, 'search_page')['results']
    max_page = ceil(offers_json['aggregatedOffers']/28)

    print(f"starting search page parsing, {max_page} pages in total")
    page_df_list = list()
    for i in range(max_page):

        time_print(f"processing page {i+1}")

        # after 1st page is done we need to load a new one
        if i > 0:
            offers_json = load_offer_json(scraper, f"{url}&p={i+1}", 'search_page')['results']

        offers_list = offers_json['offers']
        current_page_df = pd.concat([process_single_offer_card(offer) for offer in offers_list], ignore_index=True)
        page_df_list.append(current_page_df)
        time_print("finished")

        random_sleep(sleep_mean, sleep_var)

    full_df = pd.concat(page_df_list, ignore_index=True)
    
    return full_df
