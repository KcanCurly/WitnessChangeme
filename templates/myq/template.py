import os
import importlib
import requests
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re
from urllib.parse import quote

def verify_login2(url):
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "myq", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]
        res = requests.get(url, verify=False, timeout= 15)
        soup = BeautifulSoup(res.text, "html.parser")

        wsf_request_id = soup.find("input", {"id": "wsfHashId"})["value"]

        script_content = soup.findAll('script', type="text/javascript")
        script_content = script_content[-1].string

        match = re.search(r'"instanceID":"(.*?)"', script_content)
        if match:
            instance_id = match.group(1)


        wsfState='{"async":true,"hash":{},"object":"C4","method":"onLogin","params":[],"ctrlsState":{"C1":{"focusedCtrl":"C10"},"C9":{"modified":true,"value":"*' + username +'"},"C10":{"modified":true,"value":"*' + password + '"}},"deletedServerCtrls":[],"requestID":0,"instanceID":"' + instance_id + "}"
        wsfRequestId = wsf_request_id
        C7="tr"
        pwd=password

        req = requests.Request("POST", url, data={"wsfState" : quote(wsfState), "wsfRequestId": wsfRequestId, "C7": C7, "pwd": pwd})
        prepared = req.prepare()
        print(f"{prepared.method} {prepared.url} HTTP/1.1")
        for k, v in prepared.headers.items():
            print(f"{k}: {v}")
        if prepared.body:
            print("\n", prepared.body.decode() if isinstance(prepared.body, bytes) else prepared.body)
        res = requests.post(url, verify=False, timeout= 15, data={"wsfState" : quote(wsfState), "wsfRequestId": wsfRequestId, "C7": C7, "pwd": pwd})
        print(res.headers)
        print(res.text)
        for cookie in res.cookies:
            print(cookie.name)
            if "PHP" in cookie.name:
                with open("witnesschangeme-valid.txt", "a") as file:
                    file.write(f"{url} => MYQ => {username}:{password}\n")

    with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
        file.write(f"{url} => MYQ\n")


def verify_login(driver, username, password):
    # Logic to verify login success
    try:

        username_field = driver.driver.find_element(By.ID, "C9input")
        password_field = driver.driver.find_element(By.ID, "C10input")
        login_button = driver.driver.find_element(By.ID, "C12")

        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()



        return not "formMsg errorMsg" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "/myq/" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "myq", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "myq", "images")

    return {
        "name": "MYQ",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check":check
    }
    