import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "system"
    password = "manager"

    res = requests.post(url + "/login", verify=False, data={"schema": "0", "alias":username, "password": password})
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if "SUCCESSFUL" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => ARIS Connect => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => ARIS Connect => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => ARIS Connect\n")

def check(source_code):
    return "ARISWebUiKit" in source_code

def get_template():
    return {
        "name": "ARIS Connect",
        "verify_login": verify_login,
        "check":check
    }
    