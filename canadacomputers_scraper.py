import playwright.sync_api
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import time
import product

## Scraper specialized for Canada Computers

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[data-item-id]')  # Get product parent nodes
    product_list = []
    for index, item in enumerate(products):
        product_list.append(product.product())
        product_list[index].used = False
        product_list[index].cond = "New"
        product_list[index].website = "CanadaComputers.com"
        if item.css_matches('a'):  # Safety check to prevent errors
            product_list[index].link = item.css_first('a').attrs['href']
        if item.css_matches('[class="text-dark d-block productTemplate_title"]'):
            product_list[index].name = item.css_first('[class="text-dark d-block productTemplate_title"]').text(deep=True, strip=True)
        if item.css_matches('[class~="pq-hdr-product_price"]'):
            product_list[index].price = float(item.css_first('[class~="pq-hdr-product_price"]').child.text(deep=True, strip=True).replace("$", "").replace(",", ""))
        # No ratings available on Canada Computers
        product_list[index].seller = "Canada Computers"

    return product_list

# Go to page and obtain info

def run(query, page: playwright.sync_api.Page):
    search = "https://www.canadacomputers.com/search/results_details.php?language=en&keywords=" + query
    page.goto(search)
    page.mouse.wheel(0, -10000)
    time.sleep(1)
    return get_product_list(page)
