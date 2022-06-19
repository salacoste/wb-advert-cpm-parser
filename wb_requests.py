import requests
import urllib


def __wb_headers():
    headers = {
        "Accept": "*/*",
        "Origin": "https://www.wildberries.ru",
        "Accept-Encoding": "gzip, deflate, br",
        "Host": "catalog-ads.wildberries.ru",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
        "Accept-Language": "en-us",
        "Referer": "https://www.wildberries.ru/catalog/0/search.aspx?search={url_encoded_query_text}",
        "Connection": "keep-alive"
    }
    return headers


def search_catalog_ads(query_text):
    url_encoded_query_text = urllib.parse.quote_plus(query_text)
    url = f'https://catalog-ads.wildberries.ru/api/v5/search?keyword={url_encoded_query_text}'
    headers = __wb_headers()
    headers["Referer"] = headers["Referer"].replace('{url_encoded_query_text}', url_encoded_query_text)
    print('send request: {}'.format(url))
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()