import requests
import re
from bs4 import BeautifulSoup
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    credentials = ["root:changeme", "admin:welcome1", "admin:changeme"]
    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    for cred in credentials:
        cred = cred.split(":")
        username = cred[0]
        password = cred[1]
        extra = "/iPages/i_login.asp"
        extra1 = '/iPages/loginProcessor.asp'
        pattern = r'^(https?://[^/]+)'
        match = re.match(pattern, url)
        base_url = match.group(1)
        res = requests.get(url + extra, verify=False, timeout=15)
        cookies = res.cookies
        soup = BeautifulSoup(res.text, 'html.parser')

        scripts = soup.find_all('script')

        for script in scripts:
            if script.string and "loginToken" in script.string:

                match = re.search(r'"loginToken", "(.*?)"\);', script.string)
                login_token = match.group(1)

                res = requests.post(base_url + extra1, data={"username" : username, "password": password, "loginToken": login_token}, verify=False, timeout=15, cookies=cookies)

                if "/iPages/suntab.asp" in res.text and res.status_code == 200:
                    with valid_lock:
                        with open("witnesschangeme-valid.txt", "a") as file:
                            file.write(f"{url}{f" | {hostname}" if hostname else ""} => ORACLE INTEGRATED LIGHTS OUT MANAGER => {username}:{password}\n")
                    print(f"{url}{f" | {hostname}" if hostname else ""} => ORACLE INTEGRATED LIGHTS OUT MANAGER => {username}:{password}")

                break

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => ORACLE INTEGRATED LIGHTS OUT MANAGER\n")

def check(source_code):
    return "Integrated Lights Out Manager" in source_code

def get_template():
    return {
        "name": "ORACLE INTEGRATED LIGHTS OUT MANAGER",
        "verify_login": verify_login,
        "check":check
    }
    