from bs4 import BeautifulSoup
import requests
import json

source = requests.get("")


with open("product-list.json", "r") as f:
    data = json.load(f)

data = data["searchData"]["results"]["products"]

data = {product["productId"]: product["productName"] for product in data}

with open("product.json", "w") as f:
    json.dump(data, f)
