import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "smc"
    password = "smc"

    res = requests.post(url + "/univmax/restapi/common/login", auth=(username, password), timeout= 15, verify=False, headers={
        "U4V-REST-APP-NAME" : "univmax" # needed
    })
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if "Unauthorized" not in res.text and res.status_code == 200:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => UNISPHERE FOR POWERMAX => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => UNISPHERE FOR POWERMAX => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => UNISPHERE FOR POWERMAX\n")


def check(source_code):
    return "Welcome to EMC Unisphere for VMAX" in source_code

def get_template():
    return {
        "name": "UNISPHERE FOR POWERMAX",
        "verify_login": verify_login,
        "check":check
    }
    