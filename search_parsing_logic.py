import cloudscraper
from constants import SEARCH_PAGE_JSON_TEMPLATE
from math import ceil
from utils import (
    load_offer_json
)

scraper = cloudscraper.create_scraper()
url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&district%5B0%5D=10&electronic_trading=2&engine_version=2&flat_share=2&maxprice=14000000&offer_type=flat&only_flat=1"

offers_json = load_offer_json(scraper, url, SEARCH_PAGE_JSON_TEMPLATE)['results']
max_page = ceil(offers_json['aggregatedOffers']/28)

offers_json = offers_json['offers']
single_offer_url = offers_json['fullUrl']
offers_json[0]['fullUrl']
