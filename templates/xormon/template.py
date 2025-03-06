import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    res = requests.post(url + "/login", verify=False, data={"username":"admin@xormon.com", "password":"xorux4you"})

    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if res.status_code != "401":
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORMON => admin@xormon.com:xorux4you\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => XORMON => admin@xormon.com:xorux4you")
    else:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => XORMON\n")
    
    
def check(source_code):
    return "Xormon is performance monitoring tool for servers, storage, SAN and LAN" in source_code

def get_template():
    return {
        "name": "XORMON",
        "verify_login": verify_login,
        "check": check
    }
    