import os
import importlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests

def verify_login2(url, verbose = False):
    found = False
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "watson", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]

        res = requests.post(url, verify=False, data={"username":username, "password": password})

        if not "Authentication failed" in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => WATSON => {username}:{password}\n")
            print(f"{url} => WATSON => {username}:{password}")
            found = True

    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => WATSON\n")

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        WebDriverWait(driver.driver, 60).until(
            EC.visibility_of_element_located((By.XPATH, "//input[@type='submit']"))
        )

        username_field = driver.driver.find_element(By.ID, "username")
        password_field = driver.driver.find_element(By.ID, "password")
        login_button = driver.driver.find_element(By.XPATH, "//input[@type='submit']")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Authentication failed" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "/Watson/" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "watson", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "watson", "images")

    return {
        "name": "WATSON",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check":check
    }
    