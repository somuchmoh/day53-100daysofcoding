from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

ZILLOW_URL = "https://appbrewery.github.io/Zillow-Clone/"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScxGgJBLj9jjaGvPOpp4UJNHdM_mTGah9ym5P-_t0SMTRAyGw/viewform?usp=sf_link"

response = requests.get(ZILLOW_URL)
zillow = response.text
soup = BeautifulSoup(zillow, "html.parser")

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_URL)

price_list = []
for price in soup.find_all(name="span", class_="PropertyCardWrapper__StyledPriceLine"):
    if "+" in price.text:
        prop_price_old = price.text.split("+")
        prop_price = prop_price_old[0] + "/mo"
        price_list.append(prop_price)
    else:
        prop_price = price.text
        price_list.append(prop_price)

add_list = []
for address in soup.find_all(name="address"):
    new_add = address.text.split("\n")
    add_list.append(new_add[1].replace(" ", ""))

link_list = []
for links in soup.find_all(name="a", class_="StyledPropertyCardDataArea-anchor"):
    link_list.append(links['href'])
print(link_list)

for i in range(0, len(add_list)):
    add_field = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(3)
    add_field.click()
    add_field.send_keys(add_list[i])

    price_field = driver.find_element(By.XPATH,
                                    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(3)
    price_field.click()
    price_field.send_keys(price_list[i])

    link_field = driver.find_element(By.XPATH,
                                      '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    time.sleep(3)
    link_field.click()
    link_field.send_keys(link_list[i])

    submit = driver.find_element(By.CLASS_NAME, "NPEfkd")
    submit.click()

    submit_another_response = driver.find_element(By.CSS_SELECTOR, "a")
    submit_another_response.click()