from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for Walmart

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[data-item-id]')  # Get product parent node
    product_list = []
    for index, item in enumerate(products):
        product_list.append(product.product())
        product_list[index].website = "Walmart.ca"
        product_list[index].seller = "Walmart"
        product_list[index].link = "https://www.walmart.ca" + item.child.attrs['href']
        if item.css_matches('[class="w_q67L"]'):  # Safety check to prevent errors
            product_list[index].name = item.css_first('[class="w_q67L"]').text(deep=False, strip=True)
            if "Condition" in product_list[index].name or "Grade" in product_list[index].name:
                words = product_list[index].name.split(" ")
                for i, word in enumerate(words):
                    if word == "Condition":
                        if i-1 >= 0:
                            product_list[index].cond = words[i-1]

            product_list[index].used = "Refurbished" in product_list[index].name
        if item.css_matches('[data-automation-id="product-price"]'):
            price = item.css_first('[data-automation-id="product-price"]').child.text(deep=False, strip=True)
            accPrice = ""
            for char in price:
                if char.isnumeric() or char == ".":
                    accPrice+=char
            product_list[index].price = float(accPrice)
        if item.css_matches('[data-testid="product-ratings"]'):
            product_list[index].rating = float(item.css_first('[data-testid="product-ratings"]').attrs['data-value'])

    return product_list

# Go to page and obtain info

def run(query, page):
    search = "https://www.walmart.ca/en/search?q=" + query
    page.goto(search)
    return get_product_list(page)

