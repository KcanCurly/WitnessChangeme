import argparse
import importlib.resources
import importlib.resources.simple
import os
import importlib.util
import importlib
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup

disable_warnings(InsecureRequestWarning)

# Locks for file writing
error_lock = threading.Lock()
valid_lock = threading.Lock()
valid_url_lock = threading.Lock()
valid_template_lock = threading.Lock()
known_bads_lock = threading.Lock()
manual_lock = threading.Lock()



def check_if_known_Bad(response):
    if "Dynatrace Managed" in response:
        return "Dynatrace Managed"
    if "ExchangeService Service" in response:
        return "ExchangeService Service"
    if "This is a Windows© Communication Foundation service" in response:
        return "Windows© Communication Foundation service"
    if "Node Exporter" in response:
        return "Node Exporter"
    if "Humio bulk ingest endpoint" in response:
        return "Humio bulk ingest endpoint"
    if "Edison Forever!" in response:
        return "Edison Forever"
    if "Outlook" in response:
        return "Outlook"
    if "Web Tools" and "Element Manager" in response:
        return "Broadcom Web Tools Element Manager"
    if "Nessus Scanner" in response:
        return "Nessus Scanner"
    if "SOAP Plugin - Source Node Status" in response:
        return "SOAP Plugin - Source Node Status"
    if "Welcome to VMware Aria Operations" in response:
        return "Welcome to VMware Aria Operations"
    if "PaperCut Software" and "login-illo" in response:
        return "PaperCut MobilityPrint"
    if "OpenManage" in response:
        return "OpenManage"
    if "XenServer 7" in response:
        return "Citrix XenServer 7"
    if "TE-9-Login-Header.png" in response:
        return "Tripwire Enterprise 9"
    if "SSL Visibility Appliance" in response:
        return "Symantec SSL Visibility"
    if "IIS Windows Server" in response:
        return "IIS Windows Server"
    if "Unigy Management System" in response:
        return "Unigy Management System"
    if "STREAMS MESSAGING MANAGER" in response:
        return "Streams Messaging Manager"
    if "Aangine Automated Portfolio Planning" in response:
        return "Aangine Automated Portfolio Planning"
    if "UCMDB Server" in response:
        return "UCMDB Server"
    if "WCFDocumentControl Service" in response:
        return "WCFDocumentControl Service"
    if "Proofpoint Protection Server" in response:
        return "Proofpoint Protection Server"
    if "Isilon InsightIQ" in response:
        return "Isilon InsightIQ"
    if "NiFi" in response:
        return "NiFi"
    if "HiveServer2" in response:
        return "HiveServer2"
    if "Argo CD" in response:
        return "Argo CD"
    if "Veritas Data Insight" in response:
        return "Veritas Data Insight"
    if "Structured Data Manager" in response:
        return "Structured Data Manager"
    if "Micro Focus Robotic Process Automation" in response:
        return "Micro Focus Robotic Process Automation"
    if "DEF Web Admin Tool" in response:
        return "DEF Web Admin Tool"
    if "<title>DPA</title>" in response:
        return "Data Protection Advisor"
    if "Proxmox Datacenter Manager" in response:
        return "Proxmox Datacenter Manager"
    if "<title>SAP XSEngine</title>" in response:
        return "SAP XSEngine"
    if "<title>ManageEngine ServiceDesk Plus</title>" in response:
        return "ManageEngine ServiceDesk Plus"
    if "<title>RecoverPoint for VMs Plugin Server</title>" in response:
        return "RecoverPoint for VMs Plugin Server"
    return None

def check_if_manual(response):
    if "Sign in to RStudio" in response:
        return "RSTUDIO => rstudio:rstudio"
    if "Sign in to Posit Workbench" in response:
        return "POSIT WORKBENCH => rstudio:rstudio"
    if "GetDocLink.ashx?link=logon_troubleshooting" in response:
        return "Xperience => administrator:(blank)"
    return None

def find_login(response):
    if "SAS Web Application Server" in response:
        return "/SASLogon/login"
    if "URL='/ui'" in response:
        return "/ui/#/login"
    return None

def find_title(url, response):
    if "/cgi/login.cgi" in response and "Insyde Software" in response:
        return "Veritas Remote Management"

    soup = BeautifulSoup(response, 'html.parser')
    title_tag = soup.title
    if title_tag and title_tag.string != "":
        return title_tag.string.strip()

    return ""

def authcheck(url, templates, verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, bads_lock):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, allow_redirects=True, headers=headers, verify=False, timeout=15)
        if response.status_code >= 400:
            if verbose:
                print(f"{url} => {response.status_code}")
            with error_lock:
                with open("witnesschangeme-error.txt", "a") as file:
                    file.write(f"{url} => {response.status_code}\n")
            return
    except Exception as e:
        with error_lock:
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url} => {e.__class__.__name__}\n")
        return
    
    bad = check_if_known_Bad(response.text)
    if bad:
        with bads_lock:
            with open("witnesschangeme-known-bad.txt", "a") as file:
                file.write(f"{url} => {bad}\n")
        return

    manual = check_if_manual(response.text)
    if manual:
        with manual_lock:
            with open("witnesschangeme-manual.txt", "a") as file:
                file.write(f"{url} => {manual}\n")
        return

    # NO AUTH
    if "Grafana" in response.text and "login" not in response.url:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => GRAFANA NO AUTH\n")
        print(f"{url} => GRAFANA NO AUTH")
    if "Loading Elastic" in response.text and "spaces/space_selector" in response.url:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => ELASTIC NO AUTH\n")
        print(f"{url} => ELASTIC NO AUTH")


    try:
        for _, template in templates.items():
            if verbose:
                print(f"Trying {template["name"]}")
            if template["check"](response.text):
                template["verify_login"](url, valid_lock, valid_template_lock, verbose)
                return

        title = find_title(url, response.text)
        with valid_url_lock:
            with open("witnesschangeme-valid-url-no-template.txt", "a") as file:
                if title != "":
                    file.write(f"{url} => {title}\n")
                else: file.write(f"{url}\n")

    except TimeoutError as timeout:
        with error_lock:
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url} => Timeout\n")
    except Exception as e:
        with error_lock:
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url} => {e.__class__.__name__}\n")
                file.write(str(e))

    return


def main():
    parser = argparse.ArgumentParser(description="Witnesschangeme - Website Default Credentials Authentication Checker")
    parser.add_argument("-t", required=True, help="Target URL/file to test.")
    parser.add_argument("--threads", type=int, required=False, default=10, help="Number of threads to use. (Default = 10)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()

    templates = {}

    with importlib.resources.path("templates", "") as a:
            
        for item in a.iterdir():
            if not item.name.startswith("__"):
                spec = importlib.util.spec_from_file_location(item.name, os.path.join(a, item.name, "template.py"))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                t = module.get_template()
                templates[item.name] = t

    if args.verbose:
        print(f"Loaded {len(templates)} templates: {', '.join(templates.keys())}")

    max_threads = args.threads
    # If given url is a file, read it line by line and run the templates on each line
    if os.path.isfile(args.t):
        with open(args.t, "r") as file:
            lines = [line.strip() for line in file]  # Strip newline characters

            with ThreadPoolExecutor(max_threads) as executor:
                executor.map(lambda url: authcheck(url, templates, args.verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, known_bads_lock), lines)
                    

                    
    # If given url is simply a website, run the templates on the website
    else:
        authcheck(args.t, templates, args.verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, known_bads_lock)
    

if __name__ == "__main__":
    main()