import requests

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin"
    password = "admin"
    extra = "/login"
    res = requests.post(url + extra, json={"user" : username, "password": password})

    if "Logged in" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => GRAFANA => {username}:{password}\n")
        print(f"{url} => GRAFANA => {username}:{password}")
        found = True
                
    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => GRAFANA\n")



def check(source_code):
    return "<title>Grafana</title>" in source_code

def get_template():
    return {
        "name": "GRAFANA",
        "verify_login": verify_login,
        "check":check
    }
    