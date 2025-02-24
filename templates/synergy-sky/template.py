import requests

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin@localhost"
    password = "Newpassword6"

    res = requests.post(url + "/config", verify=False, auth=(username, password))

    if res.status_code in [200]:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => Synergy SKY Appliance => {username}:{password}\n")
        print(f"{url} => Synergy SKY Appliance => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => Synergy SKY Appliance\n")

def check(source_code):
    return "<title>Synergy SKY Appliance</title>" in source_code

def get_template():
    return {
        "name": "Synergy SKY Appliance",
        "verify_login": verify_login,
        "check":check
    }
    