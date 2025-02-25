import requests
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "iCAM7000"
    password = "iris7000"

    extra= '/cgi-bin/read'
    pattern = r'^(https?://[^/]+)'
    match = re.match(pattern, url)
    base_url = match.group(1)

    res = requests.post(base_url + extra, allow_redirects=False, verify=False, data={"username":username, "password": password, "logoutBtn": "1"})

    if "Invalid username or password" not in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => IRIS ID iCAM => {username}:{password}\n")
        print(f"{url} => IRIS ID iCAM => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => IRIS ID iCAM\n")

def check(source_code):
    return "<title>Iris ID - iCAM Configuration</title>" in source_code

def get_template():
    return {
        "name": "IRIS ID iCAM",
        "verify_login": verify_login,
        "check":check
    }
    