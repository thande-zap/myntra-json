def scrapper():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    import json
    import pandas as pd
    import json
    import re

    with open("db/cookies/cookies.json", "r") as f:
        cookies = json.load(f)

    url = "https://www.myntra.com/accessories?f=Categories%3AGold%20Coin"

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    driver.get(url)

    for cookie in cookies:
        driver.add_cookie(cookie)

    time.sleep(5)

    content = (
        driver.find_element(By.CSS_SELECTOR, "body > script:nth-child(5)")
        .get_attribute("innerHTML")
        .replace("window.__myx = ", "")
    )

    content = json.loads(content)

    driver.quit()

    def extract_numbers(text):
        pattern = r"\b(?:[0-1]?[0-9]|20)\b|\b(?:[0-1]?[0-9]|20)(?=\D)"
        matches = re.findall(pattern, text)
        return ".".join(matches)

    def extract_karat(text):
        pattern = r"\b(?:22|24)(?:K|KT)\b"
        matches = re.findall(pattern, text)
        transformed_matches = ["24K" if "24" in match else "22K" for match in matches]
        return "".join(transformed_matches)

    data = content["searchData"]["results"]["products"]

    productName = []
    for index, item in enumerate(data):
        name = item["productName"]
        productName.append(
            {
                "Sr.": index + 1,
                "Name": name,
                "Purity": extract_karat(name),
                "Weight": extract_numbers(name),
                "Price": item["price"],
                "Inventory": item["inventoryInfo"][0]["inventory"],
            }
        )

    df = pd.DataFrame(productName)
    df.to_parquet("db/products.parquet", index=False)
