import requests

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "Admin"
    password = "zabbix"

    res = requests.post(url + "/index.php", verify=False, data={"name":username, "password": password, "enter": "Sign+in"})

    if not "Incorrect user name or password or account is temporarily blocked" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => ZABBIX => {username}:{password}\n")
        print(f"{url} => ZABBIX => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => ZABBIX\n")

def check(source_code):
    return "zabbix-logo" in source_code

def get_template():
    return {
        "name": "ZABBIX",
        "verify_login": verify_login,
        "check":check
    }
    