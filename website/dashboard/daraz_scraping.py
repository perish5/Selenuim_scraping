from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from .models import Product
import os
import requests
from PIL import Image
from io import BytesIO
import base64

def scrape_daraz(search_query):
    service = Service(executable_path="C:/Users/Acer/Desktop/New folder (3)/Data Analysis/chromedriver.exe")
    driver = webdriver.Chrome(service=service)

    driver.get("https://www.daraz.com.np/")
    WebDriverWait(driver, 5).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "search-box__input--O34g")))
    input_element = driver.find_element(By.CLASS_NAME, "search-box__input--O34g")
    input_element.send_keys(search_query + Keys.ENTER)

    products = driver.find_elements(By.XPATH, '//div[contains(@class,"gridItem--Yd0sa")]')

    product_name = []
    delivery = []
    actual_price = []
    discounted_price = []
    # image_urls = []
    # images = []

    for product in products:
        try:
            product_name.append(product.find_element(By.XPATH, './/div[contains(@class,"title-wrapper--IaQ0m")]').text)
        except:
            product_name.append('N/A')

        try:
            delivery.append(product.find_element(By.XPATH, './/div[contains(@class,"voucher-wrapper--vCNzH")]').text)
        except:
            delivery.append('N/A')

        try:
            actual_price.append(product.find_element(By.XPATH, './/div[contains(@class,"original-price--lHYOH")]').text)
        except:
            actual_price.append('N/A')

        try:
            price_element = WebDriverWait(product, 10).until(
                EC.visibility_of_element_located((By.XPATH, './/div[contains(@class,"current-price--Jklkc")]'))
            )
            discounted_price.append(price_element.text)
        except:
            discounted_price.append('N/A')


    driver.quit()

    df_product = pd.DataFrame({'Product_Name': product_name, 'Delivery': delivery,
                                'Actual_Price': actual_price, 'Discounted_Price': discounted_price
                               })
    

    return df_product




