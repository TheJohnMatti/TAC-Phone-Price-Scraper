from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
import product

## Scraper specialized for eBay

# Obtain array of products and find properties within

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[class="s-item__wrapper clearfix"]')  # Get product parent node
    product_list = []
    for index, item in enumerate(products):
        product_list.append(product.product())
        product_list[index].website = "Ebay.ca"
        if item.css_matches('[class="s-item__title"]'):  # Safety check to prevent errors
            product_list[index].name = item.css_first('[class="s-item__title"]').text(deep=True, separator=" ", strip=True)
        if (item.css_matches('[class="s-item__subtitle"]')):
            product_list[index].cond = item.css('[class="s-item__subtitle"]')[-1].text(deep=True, separator="", strip=True)
            if product_list[index].cond != "New (Other)":
                product_list[index].used = True
        if (item.css_matches('[class="s-item__price"]')):
            price = item.css_first('[class="s-item__price"]').text(separator=" ", strip=True).replace(" to ", "-")
            newPrice = ""
            for i in price:
                if i.isnumeric() or i == "-" or i == ".":
                    newPrice += i
            if '-' in newPrice:
                prices = newPrice.split("-")
                product_list[index].set_price_range([float(prices[0]), float(prices[1])])
            else:
                product_list[index].price = float(newPrice)
        if (item.css_matches('[class="s-item__seller-info-text"]')):
            product_list[index].seller = item.css_first('[class="s-item__seller-info-text"]').text(strip=True).split(" ")[0]
        if (item.css_matches('[class="x-star-rating"]')):
            product_list[index].rating = float(item.css_first('[class="x-star-rating"]').text(strip=True)[:3])
        if(item.css_matches('[class="s-item__link"]')):
            product_list[index].link = item.css_first('[class="s-item__link"]').attrs['href']

    return product_list


# Go to page and obtain info

def run(query, page):
    search = "https://www.ebay.ca/sch/i.html?_nkw=" + query
    page.goto(search)
    return get_product_list(page)


