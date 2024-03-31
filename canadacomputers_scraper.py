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
    for item in products:
        new_product = product.product()
        new_product.website = "CanadaComputers.com"
        new_product.used = False
        new_product.cond = "New"
        new_product.seller = "Canada Computers"
        get_title(new_product, item)
        get_cond(new_product, item)
        get_link(new_product, item)
        get_price(new_product, item)
        get_seller(new_product, item)
        get_ratings(new_product, item)
        product_list.append(new_product)

    return product_list


# Obtain product title
def get_title(new_product, item):
    if item.css_matches('[class="text-dark d-block productTemplate_title"]'):
        new_product.name = item.css_first('[class="text-dark d-block productTemplate_title"]').text(deep=True,
                                                                                                            strip=True)

# Obtain product condition
def get_cond(new_product, item):
    pass


# Obtain product link
def get_link(new_product, item):
    if item.css_matches('a'):  # Safety check to prevent errors
        new_product.link = item.css_first('a').attrs['href']

# Obtain product price
def get_price(new_product, item):
    if item.css_matches('[class~="pq-hdr-product_price"]'):
        try:
            new_product.price = float(
                item.css_first('[class~="pq-hdr-product_price"]').child.text(deep=True, strip=True).replace("$",
                                                                                                            "").replace(
                    ",", ""))
        except ValueError:
            print(f"Failed at converting price to float for {new_product.link}")

# Obtain product seller
def get_seller(new_product, item):
    pass

# Obtain product ratings
def get_ratings(new_product, item):
    pass  # No ratings available on Canada Computers


# Go to page and obtain info
def run(query, page: playwright.sync_api.Page):
    search = "https://www.canadacomputers.com/search/results_details.php?language=en&keywords=" + query
    page.goto(search)
    page.mouse.wheel(0, -10000)
    time.sleep(1)
    return get_product_list(page)
