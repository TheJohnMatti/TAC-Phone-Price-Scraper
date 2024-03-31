from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for eBay

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[class="s-item__wrapper clearfix"]')  # Get product parent node
    product_list = []
    for item in products:
        new_product = product.product()
        new_product.website = "Ebay.ca"
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
    if item.css_matches('[class="s-item__title"]'):  # Safety check to prevent errors
        new_product.name = item.css_first('[class="s-item__title"]').text(deep=True, separator=" ", strip=True)


# Obtain product condition
def get_cond(new_product, item):
    if item.css_matches('[class="s-item__subtitle"]'):
        new_product.cond = item.css('[class="s-item__subtitle"]')[-1].text(deep=True, separator="", strip=True)
        if new_product.cond != "New (Other)":
            new_product.used = True


# Obtain product link
def get_link(new_product, item):
    if item.css_matches('[class="s-item__link"]'):
        new_product.link = item.css_first('[class="s-item__link"]').attrs['href']

# Obtain product price
def get_price(new_product, item):
    if item.css_matches('[class="s-item__price"]'):
        price = item.css_first('[class="s-item__price"]').text(separator=" ", strip=True).replace(" to ", "-")
        newPrice = ""
        for i in price:
            if i.isnumeric() or i == "-" or i == ".":
                newPrice += i
        if '-' in newPrice:
            prices = newPrice.split("-")
            try:
                new_product.set_price_range([float(prices[0]), float(prices[1])])
            except ValueError:
                print(f"Failed at converting price to float for {new_product.link}")

        else:
            try:
                new_product.price = float(newPrice)
            except ValueError:
                print(f"Failed at converting price to float for {new_product.link}")

# Obtain product seller
def get_seller(new_product, item):
    if item.css_matches('[class="s-item__seller-info-text"]'):
        new_product.seller = item.css_first('[class="s-item__seller-info-text"]').text(strip=True).split(" ")[0]

# Obtain product ratings
def get_ratings(new_product, item):
    if item.css_matches('[class="x-star-rating"]'):
        try:
            new_product.rating = float(item.css_first('[class="x-star-rating"]').text(strip=True)[:3])
        except ValueError:
            print(f"Failed at converting rating to float for {new_product.link}")

# Go to page and obtain info
def run(query, page):
    search = "https://www.ebay.ca/sch/i.html?_nkw=" + query
    page.goto(search)
    return get_product_list(page)


