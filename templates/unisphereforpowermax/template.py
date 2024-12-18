import os
import importlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def verify_login2(url):
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "unisphereforpowermax", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]
        res = requests.post(url + "/restapi/common/login", auth=(username, password), timeout= 15)
        if not "Unauthorized" in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => UNISPHERE FOR POWERMAX => {username}:{password}\n")

    with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
        file.write(f"{url} => UNISPHERE FOR POWERMAX\n")

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        finalurl = driver.driver.current_url + "univmax/"
        driver.driver.get(finalurl)
        print("Unisphere HACK activated, waiting 60 seconds")
        WebDriverWait(driver.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))
        )
        print("Unisphere HACK ended")
        username_field = driver.driver.find_element(By.NAME, "uName")
        password_field = driver.driver.find_element(By.NAME, "passwordEye")
        login_button = driver.driver.find_element(By.XPATH, '//button[@type="submit"]')

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Incorrect user name or password or account is temporarily blocked" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "Welcome to EMC Unisphere for VMAX" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "unisphereforpowermax", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "unisphereforpowermax", "images")

    return {
        "name": "UNISPHERE FOR POWERMAX",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check":check
    }
    