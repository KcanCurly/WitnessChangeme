import requests

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "hacluster"
    password = "hacluster"

    res = requests.post(url + "/login", allow_redirects=False, verify=False, data={"username":username, "password": password, "Login": "Login"})

    if res.headers["Location"] == "/manage":
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => HIGH AVAILABILITY MANAGEMENT => {username}:{password}\n")
        print(f"{url} => HIGH AVAILABILITY MANAGEMENT => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => HIGH AVAILABILITY MANAGEMENT\n")

def check(source_code):
    return "Pacemaker/Corosync Configuration" in source_code

def get_template():
    return {
        "name": "HIGH AVAILABILITY MANAGEMENT",
        "verify_login": verify_login,
        "check":check
    }
    