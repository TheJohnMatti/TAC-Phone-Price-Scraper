import numpy as np
import product

## Data processing methods

def process_data(products, words):
    if products == []:
        return products
    products = list(filter(lambda x: isinstance(x.price, float), products)) # remove non-float prices (faulty data)
    average_price = np.average([x.price for x in products])
    products = list(filter(lambda x: (x.price >= average_price/4), products)) # remove suspiciously cheap products (likely phone cases or other accessories)
    return products



# def main():
#     product1 = product.product()
#     product1.price = 100.0
#     product1.name = "product1"
#     product2 = product.product()
#     product2.price = 1000.0
#     product2.name = "product2"

# if __name__ == "__main__":
#     main()
