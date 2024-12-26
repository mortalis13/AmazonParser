import re
import requests
import pyquery
import random
import time
from dataclasses import dataclass


useragents = [
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4894.117 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4855.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4892.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4854.191 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4859.153 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.79 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36/null',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36,gzip(gfe)',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4895.86 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4860.89 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4885.173 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4864.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4877.207 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_2_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4872.118 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 12_3_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4876.128 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML%2C like Gecko) Chrome/100.0.4896.127 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'
]

headers = {"User-Agent": useragents[random.randint(0,len(useragents))],"accept-language": "en-US,en;q=0.9","accept-encoding": "gzip, deflate, br","accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7"}


@dataclass
class Item:
    title: str
    price: float


def get_page(url):
  resp = requests.get(url, headers=headers)
  html = resp.text
  return html

def get_total_pages(html):
  doc = pyquery.PyQuery(html)
  pagination = list(doc('.s-pagination-strip ul .s-pagination-item').items())
  
  for item in reversed(pagination):
    if item.text().isnumeric():
      return int(item.text())
    
  return 0

def proc_page(url = None, html = None):
  if url:
    html = get_page(url)

  doc = pyquery.PyQuery(html)
  
  items = []

  results = doc('[data-component-type="s-search-result"]').items()
  for result in results:
    title = next(result('[data-cy="title-recipe"] > .a-link-normal.a-text-normal').items())
    price = next(result('[data-cy="price-recipe"] .a-price-whole').items(), None)
    try:
      price = float(price.text().replace(',', '').replace('\xa0', '').strip()) if price else None
    except:
      print(f'Cannot parse price {price.text()}')
      price = None
      
    title = title.text().strip() if title else None
    if price:
      items.append(Item(title, price))
    
  return items


base = 'https://www.amazon.com/s?k=keychron+keyboard&crid=32JE53FOHD7HX&sprefix=keychron+keyboa%2Caps%2C232&ref=nb_sb_noss_2'
# base = 'https://www.amazon.de/-/en/s?k=keychron+keyboard&rh=p_n_free_shipping_eligible%3A20943778031&ref=sr_nr_p_n_free_shipping_eligible_1&dc&crid=359SCOYDOENHA&qid=1735170466&rnid=20943777031&sprefix=keychron+keyboard%2Caps%2C125&ds=v1%3AlrToZ6w1OGxch6VQ1XsLFMZrluPZJ0H59DbCcSPoX%2BE'
# base = 'https://www.amazon.es/s?k=keychron+keyboard&rh=p_n_free_shipping_eligible%3A20930980031&dc&__mk_es_ES=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=1GU72G4WW85GD&qid=1735166580&rnid=20930979031&ref=sr_nr_p_n_free_shipping_eligible_1&sprefix=keychron+keyboard%2Caps%2C203&ds=v1%3AjDCqSMAOuYSp0YihfdJy5W7kuIoHzrwf9OAev79fqkE'
# base = 'https://www.amazon.fr/s?k=keychron+keyboard&rh=p_n_free_shipping_eligible%3A20934939031&dc&__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2J0WDEL0NU1MV&qid=1735171065&rnid=20934938031&sprefix=keychron+keyboard%2Caps%2C104&ref=sr_nr_p_n_free_shipping_eligible_1&ds=v1%3AUfcVmIKsbrvUuzB4Vn16kgSF6HvMkK2GfGISYYUmHT0'
# base = 'https://www.amazon.pl/s?k=keychron+keyboard&rh=p_n_free_shipping_eligible%3A20876078031&dc&qid=1735171070&rnid=20876077031&ref=sr_nr_p_n_free_shipping_eligible_1&ds=v1%3AqS21UO3xSU7yJ5d8uiXlhXLoXPhuwIA6UtzpqQB3BxA'


result = []

url = base + ''
html = get_page(url)
items = proc_page(html=html)
total = get_total_pages(html=html)
result.extend(items)

print(f'Total pages: {total}\n')

if total > 1:
  urls = [
    base + f'&ref=sr_pg_{page}&page={page}' for page in range(2, total+1)
  ]

  for url in urls:
    print(url)
    items = proc_page(url)
    result.extend(items)
    time.sleep(1 + random.random())
    print()

result.sort(key=lambda x: x.price)

with open('data.txt', 'w', encoding='utf8') as f:
  for item in result:
    title = item.title
    price = str(item.price)
    if len(price) == 2:
      price = price + ' '
    
    if not title.lower().startswith('keychron'): continue
    if re.search(r'\bDE\b', title): continue
    if re.search(r'\bES\b', title): continue
    if re.search(r'\bFR\b', title): continue
    
    f.write(price + ' :: ' + title + '\n')
