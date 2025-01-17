import requests

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin"
    password = "vPr0tect"
    extra = "/api/session/login"
    res = requests.post(url + extra, json={"login" : username, "password": password})

    if res.status_code not in ["401"]:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => STORWARE => {username}:{password}\n")
        print(f"{url} => STORWARE => {username}:{password}")
        found = True
                
    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => STORWARE\n")



def check(source_code):
    return "../assets/img/apple-icon.png" in source_code

def get_template():
    return {
        "name": "STORWARE",
        "verify_login": verify_login,
        "check":check
    }
    