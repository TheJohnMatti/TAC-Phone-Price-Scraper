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
    names = html.css('[class="a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"]')
    product_list = []
    for index, name in enumerate(names):
        product_list.append(product.product())
        product_list[index].name = name.text(deep=True, separator="", strip=True)
        product_list[index].used = "(Renewed)" in product_list[index].name
    prices = html.css('[class="a-price"]')
    for index, price in enumerate(prices):
        product_list[index].price = float(price.child.text(deep=False, separator="", strip=True).replace(",", "")[1:])
    stars = html.css('[class|="a-icon a-icon-star-small a-star-small"]')
    for index, star in enumerate(stars):
        product_list[index].rating = float(star.text(deep=True, separator="", strip=True)[:3])

    for item in product_list:
        print("Name: ", item.name)
        print("Price: ", item.price)
        print("Rating: ", item.rating)
        print("Used: ", item.used)

    return product_list

def run(query, page):
    search = "https://www.amazon.ca/s?k=" + query
    page.goto(search)
    return get_product_list(page)


def main():
    run("0")


if __name__ == "__main__":
    main()
