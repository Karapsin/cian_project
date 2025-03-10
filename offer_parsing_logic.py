from json_keys_lists import keys_meta_list
import re
import pandas as pd
from utils import (
    forced_mkdir,
    random_sleep,
    get_url_based_name,
    load_offer_json,
    add_json_values
)

def parse_offer_page(scraper, 
                     url, 
                     search_photos_url,
                     mean_sleep = 30,
                     var_sleep = 5
    ):

    # creating a directory in which info about current url will be saved
    path = f"data_load\\old_flats_sale\\{get_url_based_name(url, 'data')}" 
    forced_mkdir(path)

    ########################################################################################################
    # get json which will be parsed further
    offer_json = load_offer_json(scraper, url, 'offer_page', path)
    single_ad_df = pd.DataFrame()
    single_ad_df['url'] = url

    # just a shorthand notation to improve readability further 
    ad_data = offer_json['offerData']['offer']

    ########################################################################################################
    # values which can be parsed easily
    
    # loaded json have a complicated nested structure
    # this section adds to our one row df a lot of values
    # from a various internal jsons (the ones which are in the json_list object) 

    # for every such internal json we have a lot of keys to check,
    # to improve readability all of them are combined in the keys_meta_list obejcts
    
    #from json_keys_lists import keys_meta_list
    json_list = [ad_data['newbuilding'], 
                 ad_data['building'], 
                 offer_json['offerData'].get("bti", {}).get("houseData", {}), 
                 ad_data
                ]

    # the next step is to apply add_json_values function for every json - key list pair,
    # that function simply creates a column in the df 
    # which name is the same as the current key
    # and the value is extracted from the json using the mentioned key
    # (values is set to None if there is no such key in the current json)

    for json, keys_list in zip(json_list, keys_meta_list):
        single_ad_df = add_json_values(single_ad_df, json, keys_list)

    single_ad_df['object_guid'] = offer_json['offerData']['offer']['objectGuid']
    single_ad_df['coords'] = [str(ad_data['geo']['coordinates'])]
    
    #######################################################################################################
    # some values which needs to be parsed separately

    # if we failed to get a buildYear at the previous step
    # we add it here
    if single_ad_df['buildYear'][0] is None and "bti" in offer_json['offerData']:
        single_ad_df['buildYear'] = offer_json['offerData']['bti']['houseData']['yearRelease']

    # constructing address string from multiple keys in the ad_data['geo']['address']
    parsed_address = ', '.join([x['fullName'] 
                               for x 
                               in ad_data['geo']['address']
                               ]
                          )

    single_ad_df['parsed_address'] = [parsed_address]

    # json is stored, we will analyze all of them once the data collection is finished
    single_ad_df['author_info'] = str(offer_json['offerData']['agent'])

    # some inner jsons have the same structure, and hence
    # the parsing procedure is always the same
    # 2 following functions are just shortcuts for that procedure
    def search_for_label(input_json, needed_label):
        result = [x['value'] 
                  for x 
                  in input_json
                  if (1==1
                       and 'label' in x 
                       and 'value' in x 
                       and x['label'] == needed_label
                    )
                 ]
        return result

    def none_if_empty(input_list):
        return input_list[0] if len(input_list) > 0 else None
    
    # wc = water closet
    wc_type = search_for_label(offer_json['offerData']['features'][0]['features'], 'Санузел')
    single_ad_df['wc_type'] = none_if_empty(wc_type)

    # the same idea as with the wc, but for the elevator
    elevator_type = search_for_label(offer_json['offerData']['features'][0]['features'] , 'Количество лифтов')
    single_ad_df['elevator_descr'] = none_if_empty(elevator_type)

    # sale terms (свободная, альтернативная продажа)
    sale_terms = search_for_label(offer_json['offerData']['sidebar'], 'Условия сделки')
    single_ad_df['sale_terms'] = none_if_empty(sale_terms)

    # ad views
    if 'stats' in offer_json['offerData'].keys():
        single_ad_df['today_views'] = offer_json['offerData']['stats']['daily']
        single_ad_df['total_views'] = offer_json['offerData']['stats']['total']
    else:
        single_ad_df['today_views'], single_ad_df['total_views'] = None, None

    # price history 
    price_history = [(x['changeTime'], x['priceData']['price']) 
                    for x 
                    in offer_json['offerData']['priceChanges']
                    ]

    single_ad_df['price_history'] = str(price_history)

    # seo stuff generated by cian to promote the ad
    # (text displayed on the cian or vk ads)
    seo_data = offer_json['offerData']['seoData']
    single_ad_df['seo_media_title_full'] = seo_data['socialNetworksTitle']['full']
    single_ad_df['seo_media_title_short'] = seo_data['socialNetworksTitle']['short']
    single_ad_df['seo_main_title'] = seo_data['mainTitle']
    single_ad_df['seo_descr'] = seo_data['description']
    
    is_closed = ad_data['description'] == "Объявление снято с публикации, поищите ещё что-нибудь"
    single_ad_df['ad_is_closed'] = is_closed

    #######################################################################################################
    # loading photos
    forced_mkdir(f"{path}\\photos")
    if not(is_closed) and ad_data['photos'] is not None:
        photos_urls = {x['fullUrl'] 
                      for x 
                      in ad_data['photos']
                     }

        photos_urls = photos_urls | search_photos_url
    else:
        photos_urls = search_photos_url
    
    random_sleep(mean=mean_sleep, var=var_sleep)
    
    def sanitize_filename(url):
        return re.sub(r'[<>:"/\\|?*]', '_', url)

    if len(photos_urls) > 0:
        for photo_url in photos_urls:
            with open(f"{path}\\photos\\{sanitize_filename(photo_url)}", "wb") as file:
                current_image = scraper.get(photo_url)
                file.write(current_image.content)
        
            random_sleep(mean=mean_sleep, var=var_sleep)

    return single_ad_df
