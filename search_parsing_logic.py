import cloudscraper
from math import ceil
from utils import (
    load_offer_json
)

scraper = cloudscraper.create_scraper()
#url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&district%5B0%5D=10&electronic_trading=2&engine_version=2&maxprice=14000000&object_type%5B0%5D=1&offer_type=flat&only_flat=1"
url = "https://www.cian.ru/cat.php?currency=2&deal_type=sale&district%5B0%5D=10&electronic_trading=2&engine_version=2&minprice=40000000&object_type%5B0%5D=1&offer_type=flat&only_flat=1"


offers_json = load_offer_json(scraper, url, 'search_page')['results']
max_page = ceil(offers_json['aggregatedOffers']/28)

offers_list = offers_json['offers']

offer = offers_list[3]


offer['fullUrl']
offer['agent']
offer['isAuction']
offer['creationDate']
offer['hasFurniture']
offer['cadastralNumber']
offer['rentByPartsDescription']
offer['totalArea']
offer['balconiesCount']
offer['isApartments']
offer['floorNumber']
offer['title']
offer['roomsCount']
offer['kp']
offer['decoration']
offer['isByHomeowner']
offer['rosreestrCheck']
offer['livingArea']
offer['kitchenArea']
offer['loggiasCount']
offer['bedroomsCount']
offer['description']
offer['isDuplicatedDescription']


# geo
offer['geo']['userInput']
offer['geo']['coordinates']
offer['geo']['railways']
offer['geo']['undergrounds']

# building
offer['building']['parking']
offer['building']['type']
offer['building']['passengerLiftsCount']
offer['building']['cargoLiftsCount']
offer['building']['materialType']
offer['building']['floorsCount']
offer['building']['classType']
offer['building']['buildYear']
offer['building']['deadline']

# deal terms
offer['bargainTerms']['mortgageAllowed']
offer['bargainTerms']['saleType']
offer['bargainTerms']['priceType']
offer['bargainTerms']['vatType']
offer['bargainTerms']['price']
offer['bargainTerms']['utilitiesTerms']
offer['bargainTerms']['agentBonus']
offer['bargainTerms']['deposit']
offer['bargainTerms']['agentFee']
offer['bargainTerms']['bargainAllowed']

# ad publisher
offer['user'] 
offer['user']['accountType']
offer['user']['isSubAgent']

# cian estimate range (not always present)
offer['goodPrice']['estimationRange']

photos_urls_list = [x['fullUrl'] for x in offer['photos']]

