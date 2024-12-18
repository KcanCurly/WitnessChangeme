import os
import importlib
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import re
from bs4 import BeautifulSoup

def verify_login2(url, verbose = False):
    found = False

    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "oracle-integrated-lights-out-manager", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]
        extra= '/iPages/loginProcessor.asp'
        pattern = r'^(https?://[^/]+)'
        match = re.match(pattern, url)
        base_url = match.group(1)
        res = requests.get(url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')

        script = soup.findAll('script', text=re.compile('setElementValue.*loginToken.*'))
        script = script[-1]
        match = re.search(r'setElementValue\("loginToken", "(.*?)"\);', script.string)
        login_token = match.group(1)

        res = requests.post(base_url + extra, data={"username" : username, "password": password, "loginToken": login_token}, verify=False)


        if not "/iPages/i_login.asp?msg=2":
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => ORACLE INTEGRATED LIGHTS OUT MANAGER => {username}:{password}\n")
                print(f"{url} => ORACLE INTEGRATED LIGHTS OUT MANAGER => {username}:{password}")

    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => ORACLE INTEGRATED LIGHTS OUT MANAGER\n")

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        WebDriverWait(driver.driver, 60).until(
            EC.visibility_of_element_located((By.ID, "loginButton"))
        )
        username_field = driver.driver.find_element(By.ID, "username")
        password_field = driver.driver.find_element(By.ID, "password")
        login_button = driver.driver.find_element(By.ID, "loginButton")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "/iPages/i_login.asp?msg=2" in driver.driver.page_source
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
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check":check
    }
    