from playwright.sync_api import sync_playwright
from selectolax.parser import HTMLParser
from bs4 import BeautifulSoup as bs
import requests
import product

def parse_html(html, asin):
    print(html.css_first("title").text())
    print(asin)

def get_product_list(page):
    html = HTMLParser(page.content())
    products = html.css('[class="s-item__wrapper clearfix"]')
    product_list = []
    for index, item in enumerate(products):
        product_list.append(product.product())
        if item.css_matches('[class="s-item__title"]'):
            product_list[index].name = item.css_first('[class="s-item__title"]').text(deep=True, separator="", strip=True)
        if (item.css_matches('[class="s-item__subtitle"]')):
            product_list[index].cond = item.css('[class="s-item__subtitle"]')[-1].text(deep=True, separator="", strip=True)
            if product_list[index].cond != "New (Other)":
                product_list[index].used = True
        if (item.css_matches('[class="s-item__price"]')):
            product_list[index].price = item.css_first('[class="s-item__price"]').text(separator=" ", strip=True).replace(" to ", "-")
        if (item.css_matches('[class="s-item__seller-info-text"]')):
            product_list[index].seller = item.css_first('[class="s-item__seller-info-text"]').text(strip=True).split(" ")[0]
        if (item.css_matches('[class="x-star-rating"]')):
            product_list[index].rating = item.css_first('[class="x-star-rating"]').text(strip=True)




    for item in product_list:
        print("Name: ", item.name)
        print("Price: ", item.price)
        print("Rating: ", item.rating)
        print("Used: ", item.used)
        print("Condition: ", item.cond)
        print("Seller: ", item.seller)

    return product_list

def run(query, page):
    search = "https://www.ebay.ca/sch/i.html?_nkw=" + query
    page.goto(search)
    return get_product_list(page)


def main():
    pw = sync_playwright().start()
    browser = pw.chromium.launch()
    page = browser.new_page()
    run("0", page)


if __name__ == "__main__":
    main()
