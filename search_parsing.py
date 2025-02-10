import cloudscraper
from search_parsing_logic import(
    parse_all_search_results
)


urls_list = ["https://www.cian.ru/cat.php?currency=2&deal_type=sale&district%5B0%5D=10&electronic_trading=2&engine_version=2&minprice=40000000&object_type%5B0%5D=1&offer_type=flat&only_flat=1"]
scraper = cloudscraper.create_scraper()

for url in urls_list:
    df = parse_all_search_results(scraper, url)
    df.to_excel("test_search_page_parsing.xlsx")
