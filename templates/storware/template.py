import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin"
    password = "vPr0tect"
    extra = "/api/session/login"
    res = requests.post(url + extra, json={"login" : username, "password": password})
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if res.status_code not in ["401"]:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => STORWARE => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => STORWARE => {username}:{password}")
        found = True
                
    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => STORWARE\n")



def check(source_code):
    return "../assets/img/apple-icon.png" in source_code

def get_template():
    return {
        "name": "STORWARE",
        "verify_login": verify_login,
        "check":check
    }
    