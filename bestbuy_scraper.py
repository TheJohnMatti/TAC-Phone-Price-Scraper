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
    for index, item in enumerate(products):
        product_list.append(product.product())
        product_list[index].website = "BestBuy.ca"
        product_list[index].link = "https://www.bestbuy.ca/" + item.parent.attrs['href']
        if item.css_matches('[data-automation="productItemName"]'):  # Safety check to prevent errors
            product_list[index].name = item.css_first('[data-automation="productItemName"]').text(deep=False, strip=True)
            if "Open Box" in product_list[index].name:
                product_list[index].cond = "Open Box"
            if "Refurbished" in product_list[index].name:
                product_list[index].used = True
                words = product_list[index].name.split(" ")
                for i, word in enumerate(words):
                    if word == "Refurbished" and i+1<len(words):
                        product_list[index].cond = words[i+1].replace("(", "").replace(")", "")
        if item.css_matches('[data-automation="product-price"]'):
            product_list[index].price = float(item.css_first('[data-automation="product-price"]').child.text(deep=True,separator=" ", strip=True).replace("$", "").split(" ")[0])
        if item.css_matches('[itemprop="ratingValue"]'):
            product_list[index].rating = float(item.css_first('[itemprop="ratingValue"]').attrs['content'])
        if item.css_matches('[class="marketplaceName_3FG8H"]'):
            product_list[index].seller = "Marketplace Seller"
        else:
            product_list[index].seller = "Best Buy"

    return product_list

# Go to page and obtain info

def run(query, page: playwright.sync_api.Page):
    search = "https://www.bestbuy.ca/en-ca/search?search=" + query
    page.goto(search)
    page.get_by_role('button', name = "Show more").click()
    return get_product_list(page)
