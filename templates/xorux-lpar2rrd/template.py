import os
import importlib
import requests
from bs4 import BeautifulSoup

def verify_login2(url, verbose = False):
    found = False
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "xorux-lpar2rrd", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]

        res = requests.get(url + "/lpar2rrd/", verify=False, auth=(username, password))

        if not "Unauthorized" in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => XORUX LPAR2RRD => {username}:{password}\n")
            print(f"{url} => XORUX LPAR2RRD => {username}:{password}")
            found = True

    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => XORUX LPAR2RRD\n")

    found = False
    for cred in credentials:
        username = cred[0]
        password = cred[1]

        res = requests.get(url + "/stor2rrd/", verify=False, auth=(username, password))

        if not "Unauthorized" in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => XORUX STOR2RRD => {username}:{password}\n")
            print(f"{url} => XORUX STOR2RRD => {username}:{password}")
            found = True

    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => XORUX STOR2RRD\n")
    

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        currenturl = driver.driver.current_url
        currenturl += "/lpar2rrd/"
        
        protocol, rest = currenturl.split("://")

        newurl = f"{protocol}://{username}:{password}@{rest}"
        driver.driver.get(newurl)



        return not "Unauthorized" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return "/lpar2rrd/" in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "xorux-lpar2rrd", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "xorux-lpar2rrd", "images")

    return {
        "name": "XORUX LPAR2RRD",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "threshold": 0.5,
        "check": check
    }
    