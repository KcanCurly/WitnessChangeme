import os
import importlib
from selenium.webdriver.common.by import By
import requests
import re

def verify_login2(url, verbose = False):
    found = False
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "idrac", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]
        extra= '/sysmgmt/2015/bmc/session'
        pattern = r'^(https?://[^/]+)'
        match = re.match(pattern, url)
        base_url = match.group(1)

        res = requests.post(base_url + extra, verify=False, headers={"user":username, "password": password})

        if '"authResult": 7' in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => IDRAC => {username}:{password}\n")
            print(f"{url} => IDRAC => {username}:{password}")
            found = True

    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => IDRAC\n")

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
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check": check
    }
    