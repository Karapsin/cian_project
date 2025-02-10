from offer_parsing_logic import parse_offer_page
import time



urls_list = ['https://www.cian.ru/sale/flat/308690852/',
             'https://www.cian.ru/sale/flat/311102797/'
            ]

total_df = pd.read_csv("data_load\\old_flats_sale.csv")
already_done = set(total_df['url'])
scraper = cloudscraper.create_scraper()

for url in urls_list:

    if url in already_done:
        print(f"skipping {url}")
        continue

    print(f"starting {url}")
    new_df = parse_offer_page(scraper, url)
    new_df['url'] = url
    new_df['offer_page_load_dttm'] = get_current_datetime()

    total_df = pd.concat([total_df, new_df], ignore_index = True)
    print(total_df)

    total_df.to_csv("data_load\\old_flats_sale.csv", index = False)