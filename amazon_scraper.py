from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for Amazon

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[data-component-type="s-search-result"]')  # Get product parent node
    product_list = []

    for item in products:
        new_product = product.product()
        new_product.website = "Amazon.ca"
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
    if item.css_matches('[data-cy="title-recipe"]'):  # Safety check to prevent errors
        new_product.name = item.css_first('[class="a-size-base-plus a-color-base a-text-normal"]').text(
            deep=False, strip=True)
        new_product.used = "(Renewed)" in new_product.name

# Obtain product condition
def get_cond(new_product, item):
    pass


# Obtain product link
def get_link(new_product, item):
    new_product.link = "https://www.amazon.ca/dp/" + item.attrs['data-asin']

# Obtain product price
def get_price(new_product, item):
    if item.css_matches('[class="a-price"]'):
        try:
            new_product.price = float(
                item.css_first('[class="a-price"]').child.text(deep=False, strip=True).replace(",", "")[1:])
        except ValueError:
            print(f"Failed at converting price to float for {new_product.link}")

# Obtain product seller
def get_seller(new_product, item):
    pass

# Obtain product ratings
def get_ratings(new_product, item):
    if item.css_matches('[class|="a-icon a-icon-star-small a-star-small"]'):
        try:
            new_product.rating = float(
                item.css_first('[class|="a-icon a-icon-star-small a-star-small"]').text(deep=True, strip=True)[:3])
        except ValueError:
            print(f"Failed at converting rating to float for {new_product.link}")


# Go to page and obtain info
def run(query, page):
    search = "https://www.amazon.ca/s?k=" + query
    page.goto(search)
    return get_product_list(page)

