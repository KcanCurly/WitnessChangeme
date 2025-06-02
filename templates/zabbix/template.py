import requests
import socket
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "Admin"
    password = "zabbix"

    res = requests.post(url + "/index.php", verify=False, data={"name":username, "password": password, "enter": "Sign+in"})
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    print(repr(res.text))
    if "incorrect user name or password or account is temporarily blocked" not in res.text.lower():
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => ZABBIX => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => ZABBIX => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => ZABBIX\n")

def check(source_code):
    return "zabbix-logo" in source_code

def get_template():
    return {
        "name": "ZABBIX",
        "verify_login": verify_login,
        "check":check
    }
    