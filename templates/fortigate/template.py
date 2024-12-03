import os
import importlib
from pathlib import Path
from selenium.webdriver.common.by import By

def verify_login(driver, username, password):
    # Logic to verify login success
    try:

        username_field = driver.find_element(By.ID, "username")
        password_field = driver.find_element(By.ID, "secretkey")
        login_button = driver.find_element(By.ID, "login_button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Authentication failure" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "fortigate", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "fortigate", "images")

    return {
        "name": "FORTIGATE",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "threshold": 0.5
    }
    