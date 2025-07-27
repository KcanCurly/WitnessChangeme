import requests
import socket
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "admin"
    password = "admin"

    res = requests.get(url + "/lpar2rrd/", verify=False, auth=(username, password))
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if not "Unauthorized" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORUX LPAR2RRD => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => XORUX LPAR2RRD => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORUX LPAR2RRD\n")

    found = False

    res = requests.get(url + "/stor2rrd/", verify=False, auth=(username, password))

    if not "Unauthorized" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORUX STOR2RRD => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => XORUX STOR2RRD => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORUX STOR2RRD\n")

    found = False

    res = requests.post(url + "/xormon/login", verify=False, data={"username":"admin@xormon.com", "password":"xorux4you"})

    if res.status_code not in (401, 404):
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORUX XORMON => admin@xormon.com:xorux4you\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => XORUX XORMON => admin@xormon.com:xorux4you")
    else:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORUX XORMON\n")
    
    
def check(source_code):
    return "/lpar2rrd/" in source_code

def get_template():
    return {
        "name": "XORUX LPAR2RRD",
        "verify_login": verify_login,
        "check": check
    }
    