import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "admin"
    password = "admin"

    res = requests.post(url, verify=False, data={"username":username, "password": password})
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if not "Authentication failed" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => WATSON => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => WATSON => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => WATSON\n")

def check(source_code):
    return "/Watson/" in source_code

def get_template():
    return {
        "name": "WATSON",
        "verify_login": verify_login,
        "check":check
    }
    