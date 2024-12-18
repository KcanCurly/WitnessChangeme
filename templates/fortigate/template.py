import os
import importlib
import requests
from selenium.webdriver.common.by import By

def verify_login2(url, verbose = False):
    found = False
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "fortigate", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]
        res = requests.post(url + "/logincheck", data={"username" : username, "password": password})
        if not "Authentication failure" in res.text and not "Unable to contact server" in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => FORTIGATE => {username}:{password}\n")
            print(f"{url} => FORTIGATE => {username}:{password}")
            found = True
                
    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => FORTIGATE\n")


def verify_login(driver, username, password):
    # Logic to verify login success
    try:

        username_field = driver.driver.find_element(By.ID, "username")
        password_field = driver.driver.find_element(By.ID, "secretkey")
        login_button = driver.driver.find_element(By.ID, "login_button")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Authentication failure" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "logon_merge.gif" in source_code or \
            "ftnt-fortinet-grid" in source_code

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
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check":check
    }
    