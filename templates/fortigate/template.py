import requests
import socket
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin"
    password = "admin"
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    res = requests.post(url + "/logincheck", data={"username" : username, "password": password})
    if not "Authentication failure" in res.text and not "Unable to contact server" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => FORTIGATE => {username}:{password}\n")
        print(f"{url} => FORTIGATE{f" | {hostname}" if hostname else ""} => {username}:{password}")
        found = True
                
    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => FORTIGATE\n")



def check(source_code):
    return "logon_merge.gif" in source_code or \
            "ftnt-fortinet-grid" in source_code or \
            "<title>FortiGate</title>" in source_code

def get_template():
    return {
        "name": "FORTIGATE",
        "verify_login": verify_login,
        "check":check
    }
    