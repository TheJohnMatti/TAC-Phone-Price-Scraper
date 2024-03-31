import playwright.sync_api
from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for Best Buy

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[itemtype="http://schema.org/Product"]')  # Get product parent node
    product_list = []
    for item in products:
        new_product = product.product()
        new_product.website = "BestBuy.ca"
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
    if item.css_matches('[data-automation="productItemName"]'):  # Safety check to prevent errors
        new_product.name = item.css_first('[data-automation="productItemName"]').text(deep=False, strip=True)
        if "Open Box" in new_product.name:
            new_product.cond = "Open Box"
        if "Refurbished" in new_product.name:
            new_product.used = True
            words = new_product.name.split(" ")
            for i, word in enumerate(words):
                if word == "Refurbished" and i + 1 < len(words):
                    new_product.cond = words[i + 1].replace("(", "").replace(")", "")


# Obtain product condition
def get_cond(new_product, item):
    pass


# Obtain product link
def get_link(new_product, item):
    new_product.link = "https://www.bestbuy.ca/" + item.parent.attrs['href']

# Obtain product price
def get_price(new_product, item):
    if item.css_matches('[data-automation="product-price"]'):
        try:
            new_product.price = float(
                item.css_first('[data-automation="product-price"]').child.text(deep=True, separator=" ",
                                                                               strip=True).replace("$", "").split(" ")[0])
        except ValueError:
            print(f"Failed at converting price to float for {new_product.link}")

# Obtain product seller
def get_seller(new_product, item):
    if item.css_matches('[class="marketplaceName_3FG8H"]'):
        new_product.seller = "Marketplace Seller"
    else:
        new_product.seller = "Best Buy"

# Obtain product ratings
def get_ratings(new_product, item):
    if item.css_matches('[itemprop="ratingValue"]'):
        try:
            new_product.rating = float(item.css_first('[itemprop="ratingValue"]').attrs['content'])
        except ValueError:
            print(f"Failed at converting rating to float for {new_product.link}")


# Go to page and obtain info
def run(query, page: playwright.sync_api.Page):
    search = "https://www.bestbuy.ca/en-ca/search?search=" + query
    page.goto(search)
    page.get_by_role('button', name = "Show more").click()
    return get_product_list(page)
