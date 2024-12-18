import os
import importlib
import requests
from requests.auth import HTTPDigestAuth

def verify_login2(url, verbose = False):
    found = False
    with importlib.resources.path("templates", "") as a:
        b = os.path.join(a, "ipecs-ip-phone", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    for cred in credentials:
        username = cred[0]
        password = cred[1]

        res = requests.get(url + "/web/home.asp", verify=False, auth=HTTPDigestAuth(username, password))

        if not "Unauthorized" in res.text:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => IPECS IP PHONE => {username}:{password}\n")
            print(f"{url} => IPECS IP PHONE => {username}:{password}")
            found = True

    if not found:
        with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
            file.write(f"{url} => IPECS IP PHONE\n")

def verify_login(driver, username, password):
    # Logic to verify login success
    try:
        currenturl = driver.driver.current_url
        currenturl += "/web/home.asp"
        
        protocol, rest = currenturl.split("://")

        newurl = f"{protocol}://{username}:{password}@{rest}"
        driver.driver.get(newurl)



        return not "Unauthorized" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def check(source_code):
    return 'index.asp' in source_code and 'lip-mainframe' in source_code

def get_template():
    # Load credentials and images dynamically
    with importlib.resources.path("templates", "") as a:

        b = os.path.join(a, "ipecs-ip-phone", "creds.txt")
        with open(b, "r") as f:
            credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]
            
        i  = os.path.join(a, "ipecs-ip-phone", "images")

    return {
        "name": "IPECS IP PHONE",
        "image_path": i,
        "credentials": credentials,
        "verify_login": verify_login,
        "verify_login2": verify_login2,
        "threshold": 0.5,
        "check": check
    }
    