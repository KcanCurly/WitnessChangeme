import requests

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "admin"
    password = "admin"

    res = requests.post(url, verify=False, data={"username":username, "password": password})

    if not "Authentication failed" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => WATSON => {username}:{password}\n")
        print(f"{url} => WATSON => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => WATSON\n")

def check(source_code):
    return "/Watson/" in source_code

def get_template():
    return {
        "name": "WATSON",
        "verify_login": verify_login,
        "check":check
    }
    