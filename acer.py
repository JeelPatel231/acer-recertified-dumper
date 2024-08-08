import requests
import logging
from bs4 import BeautifulSoup, Tag
from database import init_db, session
from database.models import Product, ProductImages

logging.basicConfig(level=logging.DEBUG)
init_db()


base_url = 'https://store.acer.com/en-in/laptops'
params = { 'p' : 1, 'product_list_limit': 'all' }

resp = requests.get(base_url, params=params, headers={
  'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64; rv:128.0) Gecko/20100101 Firefox/128.0',
  'X-Requested-With' : 'XMLHttpRequest'
})

html_content = resp.text

soup = BeautifulSoup(html_content, features='html.parser')

list_holder = soup.find('ol', class_="product-items")
all_products = list_holder.find_all('div', { 'data-container': 'product-list' })


def extract_all_prices(price_wrapper: Tag):
  m = {}
  for price in price_wrapper.find_all('span', class_='price-wrapper'):
    amount = price['data-price-amount']
    price_type = price['data-price-type']

    m[price_type] = int(amount)

  return m

def extract_product_info(product: Tag) -> Product:
  name = product.strong.a.text.strip()
  link = product.strong.a['href']
  eec_prod_id = product['data-eec-product-id']
  actions = product.find('div', class_='product actions product-item-actions')

  image_list = list(map(lambda x: next(iter(x['src'].split('?', 1))) ,product.find_all('img')))

  price = product.find('div', class_='price-box price-final_price')
  product_id = int(price['data-product-id'])
  all_prices = extract_all_prices(price)

  stock = actions.find('div', class_='stock').text.strip()
  description = product.find('div', class_='product description product-item-description').ul.get_text().strip()

  image_entities = [ProductImages(product_id=product_id, image_url=x) for x  in image_list]

  return Product(
    id=product_id,
    name=name,
    link=link, 
    eec_product_id=eec_prod_id, 
    stock=stock,
    description=description, 
    images=image_entities,
    old_price=all_prices.get('oldPrice'),
    special_price=all_prices['finalPrice']
  )

prods = map(extract_product_info, all_products)

session.add_all(list(prods))
session.commit()