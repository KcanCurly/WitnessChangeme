import requests
import re
from bs4 import BeautifulSoup

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    credentials = ["root:changeme", "admin:welcome1", "admin:changeme"]

    for cred in credentials:
        cred = cred.split(":")
        username = cred[0]
        password = cred[1]
        extra = "/iPages/i_login.asp"
        extra1 = '/iPages/loginProcessor.asp'
        pattern = r'^(https?://[^/]+)'
        match = re.match(pattern, url)
        base_url = match.group(1)
        res = requests.get(url + extra, verify=False, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')

        scripts = soup.findAll('script')
        for script in scripts:
            if "loginToken" in script:
                print(script.string)
                match = re.search(r'"loginToken", "(.*?)"\);', script.string)
                login_token = match.group(1)

                res = requests.post(base_url + extra1, data={"username" : username, "password": password, "loginToken": login_token}, verify=False, timeout=15)

                if "/iPages/suntab.asp" in res.text and res.status_code == 200:
                    with valid_lock:
                        with open("witnesschangeme-valid.txt", "a") as file:
                            file.write(f"{url} => ORACLE INTEGRATED LIGHTS OUT MANAGER => {username}:{password}\n")
                    print(f"{url} => ORACLE INTEGRATED LIGHTS OUT MANAGER => {username}:{password}")

                break

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => ORACLE INTEGRATED LIGHTS OUT MANAGER\n")

def check(source_code):
    return "Integrated Lights Out Manager" in source_code

def get_template():
    return {
        "name": "ORACLE INTEGRATED LIGHTS OUT MANAGER",
        "verify_login": verify_login,
        "check":check
    }
    