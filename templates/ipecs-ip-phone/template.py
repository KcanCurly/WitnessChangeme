import requests
from requests.auth import HTTPDigestAuth
import socket
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    username = "admin"
    password = "ipkts"

    res = requests.get(url + "/web/home.asp", verify=False, auth=HTTPDigestAuth(username, password))
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
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => IPECS IP PHONE => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => IPECS IP PHONE => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => IPECS IP PHONE\n")


def check(source_code):
    return 'index.asp' in source_code and 'lip-mainframe' in source_code

def get_template():
    return {
        "name": "IPECS IP PHONE",
        "verify_login": verify_login,
        "check": check
    }
    