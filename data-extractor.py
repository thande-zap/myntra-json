import pandas as pd
import json
import re


def extract_numbers(text):
    pattern = r"\b(?:[0-1]?[0-9]|20)\b|\b(?:[0-1]?[0-9]|20)(?=\D)"
    matches = re.findall(pattern, text)
    return ".".join(matches)


def extract_karat(text):
    pattern = r"\b(?:22|24)(?:K|KT)\b"
    matches = re.findall(pattern, text)
    transformed_matches = ["24K" if "24" in match else "22K" for match in matches]
    return "".join(transformed_matches)


with open("db/raw-data.json", "r") as f:
    data = json.load(f)

data = data["searchData"]["results"]["products"]

productName = []

for index, item in enumerate(data):
    name = item["productName"]
    productName.append(
        {
            "Sr.": index + 1,
            "name": name,
            "purity": extract_karat(name),
            "weight": extract_numbers(name),
            "price": item["price"],
            "inventory": item["inventoryInfo"][0]["inventory"],
        }
    )


with open("db/products.json", "w") as f:
    json.dump(productName, f, indent=2)
