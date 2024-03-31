from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for Walmart


# Obtain array of products and find properties within
def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[data-item-id]')  # Get product parent node
    product_list = []
    for item in products:
        new_product = product.product()
        new_product.website = "Walmart.ca"
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
    if item.css_matches('[class="w_q67L"]'):  # Safety check to prevent errors
        new_product.name = item.css_first('[class="w_q67L"]').text(deep=False, strip=True)
        if "Condition" in new_product.name or "Grade" in new_product.name:
            words = new_product.name.split(" ")
            for i, word in enumerate(words):
                if word == "Condition":
                    if i - 1 >= 0:
                        new_product.cond = words[i - 1]
        new_product.used = "Refurbished" in new_product.name


# Obtain product condition
def get_cond(new_product, item):
    pass


# Obtain product link
def get_link(new_product, item):
    new_product.link = "https://www.walmart.ca" + item.child.attrs['href']

# Obtain product price
def get_price(new_product, item):
    if item.css_matches('[data-automation-id="product-price"]'):
        price = item.css_first('[data-automation-id="product-price"]').child.text(deep=False, strip=True)
        accPrice = ""
        for char in price:
            if char.isnumeric() or char == ".":
                accPrice += char
        try:
            new_product.price = float(accPrice)
        except ValueError:
            print(f"Failed at converting price to float for {new_product.link}")

# Obtain product seller
def get_seller(new_product, item):
    new_product.seller = "Walmart"

# Obtain product ratings
def get_ratings(new_product, item):
    if item.css_matches('[data-testid="product-ratings"]'):
        try:
            new_product.rating = float(item.css_first('[data-testid="product-ratings"]').attrs['data-value'])
        except ValueError:
            print(f"Failed at converting rating to float for {new_product.link}")


# Go to page and obtain info
def run(query, page):
    search = "https://www.walmart.ca/en/search?q=" + query
    page.goto(search)
    return get_product_list(page)

