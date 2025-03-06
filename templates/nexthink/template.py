import requests
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin"
    password = "admin"

    token_re = r"name=\"csrf_nexthink_token\" value=\"(.*)\" " 

    res1 = requests.get(url, verify=False)

    match = re.search(token_re, res1.text)
    if match:
        token = match.group(1)

        res = requests.post(url + "/", verify=False, data={"csrf_nexthink_token":token, "username": username, "password": password, "login": "Sign+In"})


        if not "Authentication failed! Your username and/or password is invalid" in res.text:
            
            with valid_lock:
                with open("witnesschangeme-valid.txt", "a") as file:
                    file.write(f"{url} => Nexthink => {username}:{password}\n")
            print(f"{url} => Nexthink => {username}:{password}")
            found = True
                
    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => Nexthink\n")



def check(source_code):
    return "<title>Nexthink console: Login</title>" in source_code

def get_template():
    return {
        "name": "Nexthink",
        "verify_login": verify_login,
        "check":check
    }
    