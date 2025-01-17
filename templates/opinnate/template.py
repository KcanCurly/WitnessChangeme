import requests
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "admin"
    password = "opinnate"

    extra= '/api/login'
    pattern = r'^(https?://[^/]+)'
    match = re.match(pattern, url)
    base_url = match.group(1)

    res = requests.post(base_url + extra, verify=False, data={"username":username, "password": password})

    if 'Login Succesfull' in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => Opinnate => {username}:{password}\n")
        print(f"{url} => Opinnate => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => Opinnate\n")


def check(source_code : str) -> bool:
    return "<title>Opinnate</title>" in source_code

def get_template():

    return {
        "name": "Opinnate",
        "verify_login": verify_login,
        "check": check
    }
    