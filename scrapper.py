def scrapper():
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import time
    import json
    import pickle
    import pandas as pd
    import json
    import re

    with open("db/cookies/cookies.json", "r") as f:
        data = json.load(f)
    with open("db/cookies/cookies.pkl", "wb") as f:
        pickle.dump(data, f)

    url = "https://www.myntra.com/accessories?f=Categories%3AGold%20Coin"

    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=chrome_options
    )

    driver.get(url)

    cookies = pickle.load(open("db/cookies/cookies.pkl", "rb"))

    for cookie in cookies:
        cookie["domain"] = ".myntra.com"

        try:
            driver.add_cookie(cookie)
        except Exception as e:
            print(e)

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

    with open("db/products.csv", "w", newline="") as file:
        df = pd.DataFrame(productName)
        df.to_csv(file, index=False)
