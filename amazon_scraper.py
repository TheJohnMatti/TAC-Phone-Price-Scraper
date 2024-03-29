from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for Amazon

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[data-component-type="s-search-result"]')  # Get product parent node
    product_list = []
    for index, item in enumerate(products):
        product_list.append(product.product())
        product_list[index].website = "Amazon.ca"
        product_list[index].link = "https://www.amazon.ca/dp/" + item.attrs['data-asin']
        if item.css_matches('[data-cy="title-recipe"]'):  # Safety check to prevent errors
            product_list[index].name = item.css_first('[class="a-size-base-plus a-color-base a-text-normal"]').text(deep=False, strip=True)
            product_list[index].used = "(Renewed)" in product_list[index].name
        if item.css_matches('[class="a-price"]'):
            product_list[index].price = float(item.css_first('[class="a-price"]').child.text(deep=False, strip=True).replace(",", "")[1:])
        if item.css_matches('[class|="a-icon a-icon-star-small a-star-small"]'):
            product_list[index].rating = float(item.css_first('[class|="a-icon a-icon-star-small a-star-small"]').text(deep=True, strip=True)[:3])

    for item in product_list:
        print("Name: ", item.name)
        print("Price: ", item.price)
        print("Rating: ", item.rating)
        print("Used: ", item.used)

    return product_list

# Go to page and obtain info

def run(query, page):
    search = "https://www.amazon.ca/s?k=" + query
    page.goto(search)
    return get_product_list(page)

