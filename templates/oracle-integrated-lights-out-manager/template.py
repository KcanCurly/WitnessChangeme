import os
import importlib
from selenium.webdriver.common.by import By

def verify_login(driver, username, password):
    # Logic to verify login success
    try:

        username_field = driver.driver.find_element(By.ID, "name")
        password_field = driver.driver.find_element(By.ID, "password")
        login_button = driver.driver.find_element(By.ID, "loginButton")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Authentication Failure" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "Integrated Lights Out Manager" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "oracle-integrated-lights-out-manager", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "oracle-integrated-lights-out-manager", "images")

    return {
        "name": "ORACLE INTEGRATED LIGHTS OUT MANAGER",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "threshold": 0.5,
        "check":check
    }
    