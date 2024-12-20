from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import quote

def verify_login(url, valid_lock, valid_template_lock, verbose = False):
    found = False

    username = "*admin"
    password = "1234"

    res = requests.get(url, verify=False, timeout= 15)
    soup = BeautifulSoup(res.text, "html.parser")

    wsf_request_id = soup.find("input", {"id": "wsfHashId"})["value"]

    script_content = soup.findAll('script', type="text/javascript")
    script_content = script_content[-1].string

    match = re.search(r'"instanceID":"(.*?)"', script_content)
    if match:
        instance_id = match.group(1)


    wsfState='{"async":true,"hash":{},"object":"C4","method":"onLogin","params":[],"ctrlsState":{"C1":{"focusedCtrl":"C10"},"C9":{"modified":true,"value":"*' + username +'"},"C10":{"modified":true,"value":"*' + password + '"}},"deletedServerCtrls":[],"requestID":0,"instanceID":"' + instance_id + "}"
    wsfRequestId = wsf_request_id
    C7="tr"
    pwd=password

    res = requests.post(url, verify=False, timeout= 15, data={"wsfState" : quote(wsfState), "wsfRequestId": wsfRequestId, "C7": C7, "pwd": pwd})

    if not "errorMsg" in res.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => MYQ => {username}:{password}\n")
        print(f"{url} => MYQ => {username}:{password}")
        found = True

    if not found:
        with valid_template_lock:
            with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                file.write(f"{url} => MYQ\n")


def check(source_code):
    return "/myq/" in source_code

def get_template():
    return {
        "name": "MYQ",
        "verify_login": verify_login,
        "check":check
    }
    