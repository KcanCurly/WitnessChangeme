import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    res = requests.post(url + "/authenticate", verify=False, data={"username":"admin", "password":"admin"})

    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if res.status_code not in [401]:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => JHipster Registry => admin:admin\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => JHipster Registry => admin:admin")
    else:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => JHipster Registry\n")
    
    
def check(source_code):
    return '<title>JHipster Registry</title>' in source_code

def get_template():
    return {
        "name": "JHipster Registry",
        "verify_login": verify_login,
        "check": check
    }
    