import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "nsroot"
    password = "nsroot"

    extra= '/nitro/v1/config/login'
    pattern = r'^(https?://[^/]+)'
    match = re.match(pattern, url)
    base_url = match.group(1)

    res = requests.post(base_url + extra, verify=False, headers={"NITRO_WEB_APPLICATION": "true", "Content-Type": "application/x-www-form-urlencoded"}, data=f"object=%7B%22login%22%3A%7B%22username%22%3A%22{username}%22%2C%22password%22%3A%22{password}%22%7D%7D")
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if not "Invalid username or password" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => NetScaler Console => {username}:{password}\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => NetScaler Console => {username}:{password}")
        found = True
                
    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => NetScaler Console\n")



def check(source_code):
    return "<title>NetScaler Console</title>" in source_code

def get_template():
    return {
        "name": "NetScaler Console",
        "verify_login": verify_login,
        "check":check
    }
    