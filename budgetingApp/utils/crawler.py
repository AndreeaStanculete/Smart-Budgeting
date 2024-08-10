from bs4 import BeautifulSoup
from requests import get

def searchForPrices(product: str) -> str:
    priceListWithURL = []
    searchURL = f"https://www.emag.ro/search/{product}?ref=effective_search"
    searchClass = 'product-new-price'

    page = get(searchURL)
    soup = BeautifulSoup(page.content, 'html.parser')

    for item in soup.find_all(class_=searchClass):
        priceListWithURL.append({
            'Price': float(item.getText()[:-4].replace('.', '').replace(',', '.')),
            'Name': "",
            'URL': ""
        })
    for index, item in enumerate(soup.find_all('a', class_="card-v2-title")):
        priceListWithURL[index]['URL'] = item['href']
        priceListWithURL[index]['Name'] = item.text
    priceListWithURL.sort(key = lambda x: x['Price'])

    return priceListWithURL[:2]