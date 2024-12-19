import os
import importlib
from selenium.webdriver.common.by import By
import requests

def verify_login2(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "zabbix", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]

        res = requests.post(url + "/index.php", verify=False, data={"name":username, "password": password, "enter": "Sign+in"})

        if not "Incorrect user name or password or account is temporarily blocked" in res.text:
            with valid_lock:
                with open("witnesschangeme-valid.txt", "a") as file:
                    file.write(f"{url} => ZABBIX => {username}:{password}\n")
            print(f"{url} => ZABBIX => {username}:{password}")
            found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => ZABBIX\n")


def verify_login(driver, username, password):
    # Logic to verify login success
    try:

        username_field = driver.driver.find_element(By.NAME, "name")
        password_field = driver.driver.find_element(By.NAME, "password")
        login_button = driver.driver.find_element(By.NAME, "enter")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "Incorrect user name or password or account is temporarily blocked" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "zabbix-logo" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "zabbix", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "zabbix", "images")

    return {
        "name": "ZABBIX",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check":check
    }
    