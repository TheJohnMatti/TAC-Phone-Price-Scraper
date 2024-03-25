## Product class containing information categories we are interested in scraping

class product:
    def __init__(self):
        self.website = ""
        self.name = ""
        self.price = 0.0
        self.rating = 0.0  # Out of 5
        self.used = False  # False = new, True = used
        self.cond = ""
        self.seller = "Unknown"
        self.link = ""
        self.prices = []  # Used for products with a price range (E.g selections for GB)

    def set_price_range(self, priceRange):
        self.prices.append(priceRange[0])
        self.prices.append(priceRange[1])
