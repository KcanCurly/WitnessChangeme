import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    creds = ["root:calvin", "root:ARCADMIN"]
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    for cred in creds:
        found = False
        username = cred.split(":")[0]
        password = cred.split(":")[1]

        extra= '/sysmgmt/2015/bmc/session'
        pattern = r'^(https?://[^/]+)'
        match = re.match(pattern, url)
        base_url = match.group(1)

        res = requests.post(base_url + extra, verify=False, headers={"user":username, "password": password})

        if '"authResult" : 7' in res.text:
            with valid_lock:
                with open("witnesschangeme-valid.txt", "a") as file:
                    file.write(f"{url}{f" | {hostname}" if hostname else ""} => IDRAC => {username}:{password}\n")
            print(f"{url}{f" | {hostname}" if hostname else ""} => IDRAC => {username}:{password}")
            found = True

        if not found:
            with valid_template_lock:
                with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                    file.write(f"{url}{f" | {hostname}" if hostname else ""} => IDRAC\n")


def check(source_code : str) -> bool:
    return "idrac-start-screen" in source_code

def get_template():

    return {
        "name": "IDRAC",
        "verify_login": verify_login,
        "check": check
    }
    