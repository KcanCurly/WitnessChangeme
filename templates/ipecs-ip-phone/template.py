import os
import importlib
from pathlib import Path
from selenium.webdriver.common.by import By

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        currenturl = driver.driver.current_url
        currenturl += "/web/home.asp"
        
        protocol, rest = currenturl.split("://")

        newurl = f"{protocol}://{username}:{password}@{rest}"
        driver.driver.get(currenturl)



        return not "Unauthorized" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "ipecs-ip-phone", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "ipecs-ip-phone", "images")

    return {
        "name": "IPECS IP PHONE",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "threshold": 0.1
    }
    