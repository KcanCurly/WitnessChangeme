#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import FirefoxOptions
import requests


TEMPLATE_FILE = "../templates/test"

def get_website_content(url):
    try:
        # Fetch the website content
        response = requests.get(url)
        response.raise_for_status()

        
        
        with open(TEMPLATE_FILE, "r", encoding="utf-8") as file:
            template = file.read().strip()
            print(response.text)
            if template in response.text:
                print("Template found")
            else:
                print("Template not found")

        
        pass
    except Exception as e:
        raise e

def main():
    options = FirefoxOptions()
    options.add_argument("--headless")
    with webdriver.Firefox(options=options) as driver:
        driver.get("https://web-scraping.dev/login")
        driver.set_window_size(1920, 1080)
        
        driver.save_full_page_screenshot("screenshot.png")


        driver.quit()

    
if __name__ == "__main__":
    get_website_content("https://web-scraping.dev/login")
    # main()
