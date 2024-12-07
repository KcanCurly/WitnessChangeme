import os
import importlib
from selenium.webdriver.common.by import By

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        username_field = driver.driver.find_element(By.NAME, "username")
        password_field = driver.driver.find_element(By.NAME, "password")
        login_button = driver.driver.find_element(By.XPATH, "//button[@type='submit']")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Login failed" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code : str) -> bool:
    return "Integrated Remote Access Controller" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "idrac", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "idrac", "images")

    return {
        "name": "IDRAC",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "threshold": 0.5,
        "check": check
    }
    