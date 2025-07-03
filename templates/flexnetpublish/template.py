import requests
import re
import socket

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False
    res = requests.post(url + "/handlesignin", verify=False, data={"username":"admin", "password":"admin"}, allow_redirects=False)

    hostname = None
    try:
        pattern = r'https?://(.*):'
        match_hostname = re.match(pattern, url)
        if match_hostname:
            ip = match_hostname.group(1)

            hostname, _, _ = socket.gethostbyaddr(ip)
    except:pass
    if "You successfully signed in" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => FlexNet Publisher License => admin:admin\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => FlexNet Publisher License => admin:admin")
    else:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => FlexNet Publisher License\n")
    
    
def check(source_code):
    return '<meta http-equiv="refresh" content="0; url=login">' in source_code

def get_template():
    return {
        "name": "FlexNet Publisher License",
        "verify_login": verify_login,
        "check": check
    }
    