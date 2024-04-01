from selenium import webdriver
from ignored import url
import time


driver = webdriver.Chrome()
driver.set_window_size(width=1920, height=1080)

driver.get(url.url)
time.sleep(10)
var = "String" "String1"

driver.save_screenshot("db/screenshot.png")


driver.quit()
