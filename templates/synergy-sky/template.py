import requests
import socket
import re

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "admin@localhost"
    password = "Newpassword6"

    res = requests.get(url + "/config", verify=False, auth=(username, password))

    if res.status_code in [200]:
        hostname = None
        try:
            pattern = r'https?://(.*):'
            match_hostname = re.match(pattern, url)
            if match_hostname:
                ip = match_hostname.group(1)

                hostname, _, _ = socket.gethostbyaddr(ip)
        except:pass
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => Synergy SKY Appliance => {username}:{password}\n")
        print(f"{url} => Synergy SKY Appliance => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => Synergy SKY Appliance\n")

def check(source_code):
    return "<title>Synergy SKY Appliance</title>" in source_code

def get_template():
    return {
        "name": "Synergy SKY Appliance",
        "verify_login": verify_login,
        "check":check
    }
    