import argparse
import importlib.resources
import os
import importlib.util
import importlib
import requests
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
import threading
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning
import re
import warnings
import socket

disable_warnings(InsecureRequestWarning)
warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

# Locks for file writing
error_lock = threading.Lock()
valid_lock = threading.Lock()
valid_url_lock = threading.Lock()
valid_template_lock = threading.Lock()
known_bads_lock = threading.Lock()
manual_lock = threading.Lock()

urls_to_try = [
    "/auth/admin/master/console",
    "/admin",
    "/trust",
    "/console",
    "/management",
    "/em",
    "/sal",
    "/analyst",
    "/mm",
    "/documents",
    "/tm",
    "/trace",
    "/ping",
    "/metrics",
    "/va",
    "/dms",
    "/workspace",
    "/initial",
    "/features",
    "/version",
    "/v2",
    "/manager",
    "/export",
    "/RM",
    "/health",
    "/authenticate",
    "/auth",
    "/provisioning",
    "/api",
    "/request",
    "/notices",
    "/captcha",
    "/logon",
    "/login",
    "/mail",
    "/sms",
    "/jsp",
    "/home",
    "/download",
    ]

def check_if_loginpage_exists(response):
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        input_fields = soup.find_all('input')
        has_password = any(field.get('type') == 'password' for field in input_fields)
        if has_password: return True
        return False
    except: return False

def check_if_known_Bad(response: requests.Response):
    for header, value in response.headers.items():
        if "ClickHouse" in header: return "ClickHouse"

    if "Dynatrace Managed" in response.text:
        return "Dynatrace Managed"
    if "ExchangeService Service" in response.text:
        return "ExchangeService Service"
    if "This is a Windows© Communication Foundation service" in response.text:
        return "Windows© Communication Foundation service"
    if "Node Exporter" in response.text:
        return "Node Exporter"
    if "Humio bulk ingest endpoint" in response.text:
        return "Humio bulk ingest endpoint"
    if "Edison Forever!" in response.text:
        return "Edison Forever"
    if "Outlook" in response.text:
        return "Outlook"
    if "Web Tools" and "Element Manager" in response.text:
        return "Broadcom Web Tools Element Manager"
    if "<title>Nessus</title>" in response.text:
        return "Nessus Scanner"
    if "SOAP Plugin - Source Node Status" in response.text:
        return "SOAP Plugin - Source Node Status"
    if "Welcome to VMware Aria Operations" in response.text:
        return "Welcome to VMware Aria Operations"
    if "PaperCut Software" and "login-illo" in response.text:
        return "PaperCut MobilityPrint"
    if "OpenManage" in response.text:
        return "OpenManage"
    if "XenServer 7" in response.text:
        return "Citrix XenServer 7"
    if "TE-9-Login-Header.png" in response.text:
        return "Tripwire Enterprise 9"
    if "SSL Visibility Appliance" in response.text:
        return "Symantec SSL Visibility"
    if "IIS Windows Server" in response.text:
        return "IIS Windows Server"
    if "Unigy Management System" in response.text or "Unigy(TM) Management System" in response.text:
        return "Unigy Management System"
    if "STREAMS MESSAGING MANAGER" in response.text:
        return "Streams Messaging Manager"
    if "Aangine Automated Portfolio Planning" in response.text:
        return "Aangine Automated Portfolio Planning"
    if "UCMDB Server" in response.text:
        return "UCMDB Server"
    if "WCFDocumentControl Service" in response.text:
        return "WCFDocumentControl Service"
    if "Proofpoint Protection Server" in response.text:
        return "Proofpoint Protection Server"
    if "Isilon InsightIQ" in response.text:
        return "Isilon InsightIQ"
    if "NiFi" in response.text:
        return "NiFi"
    if "HiveServer2" in response.text:
        return "HiveServer2"
    if "Argo CD" in response.text:
        return "Argo CD"
    if "Veritas Data Insight" in response.text:
        return "Veritas Data Insight"
    if "Structured Data Manager" in response.text:
        return "Structured Data Manager"
    if "Micro Focus Robotic Process Automation" in response.text:
        return "Micro Focus Robotic Process Automation"
    if "DEF Web Admin Tool" in response.text:
        return "DEF Web Admin Tool"
    if "<title>DPA</title>" in response.text:
        return "Data Protection Advisor"
    if "Proxmox Datacenter Manager" in response.text:
        return "Proxmox Datacenter Manager"
    if "<title>SAP XSEngine</title>" in response.text:
        return "SAP XSEngine"
    if "<title>ManageEngine ServiceDesk Plus</title>" in response.text:
        return "ManageEngine ServiceDesk Plus"
    if "<title>RecoverPoint for VMs Plugin Server</title>" in response.text:
        return "RecoverPoint for VMs Plugin Server"
    if "<title>Coriolis</title>" in response.text:
        return "Coriolis"
    if "data-netbox-version" in response.text:
        return "Netbox"
    if "<title>WS server test page</title>" in response.text:
        return "WS server test page"
    if "fitalimicon.png" in response.text:
        return "FIT ALIM"
    if "Highest contiguous completed opid" in response.text:
        return "Cerebro Metrics"
    if "LibreNMS" in response.text:
        return "LibreNMS"
    if "VMware vSphere is virtual infrastructure software for partitioning" in response.text:
        return "Vmware vSphere Welcome Page"
    if "<title>Swagger UI</title>" in response.text: # No login
        return "Swagger UI"
    if "<title>Kubernetes Dashboard</title>" in response.text: # No default password
        return "Kubernetes Dashboard"
    if "<title>IBM Tivoli Monitoring Service Index</title>" in response.text: # No login
        return "IBM Tivoli Monitoring Service Index"
    if "<title>Finesse</title>" in response.text: # No default password
        return "Cisco Finesse" 
    if "<title>RMF Data Portal</title>" in response.text: # No login
        return "RMF Data Portal"
    if "<title>Cisco Meeting Server web app</title>" in response.text: # No default password
        return "Cisco Meeting Server web app"
    if "<title>WebSphere Liberty" in response.text: # No default password
        return "WebSphere Liberty"
    if "<title>Headlamp Debug Server</title>" in response.text: # No login
        return "Headlamp Debug Server"
    if "<title>Ivanti System Manager: Sign In</title>" in response.text: # No default password
        return "Ivanti System Manager"
    if "Couchbase Console - FICO Edition</title>" in response.text: # No default password
        return "Couchbase Console - FICO Edition"
    if "<title>Cisco Unified Intelligence Center</title>" in response.text: # No default password
        return "Cisco Unified Intelligence Center"
    if "<title>Log In - Confluence</title>" in response.text: # No default password
        return "Confluence"
    if "<title>Login - AppViewX</title>" in response.text: # No default password
        return "AppViewX"
    if "IA:IM: Login" in response.text: # No default password
        return "IBM Automation Infrastructure Management"
    if "<title>VMware Skyline Health Diagnostics</title>" in response.text:
        return "VMware Skyline Health Diagnostics"
    if "<title>Wowza Streaming Engine Manager</title>" in response.text:
        return "Wowza Streaming Engine Manager"
    if "<title>Qlik NPrinting</title>" in response.text:
        return "Qlik NPrinting"
    if "<title>Identity Service Management</title>" in response.text:
        return "Identity Service Management"
    if "cuicui" in response.text: # No default password
        return "Cisco Unified Intelligence Center"
    if "Identity Services Engine" in response.text:
        return "Cisco Identity Services Engine" # No default password
    if "Cisco Virtualized Voice Browser" in response.text:
        return "Cisco Virtualized Voice Browser Portal" # No default password no login page
    if "Cisco Unified Communications Manager" in response.text:
        return "Cisco Unified Communications Manager" # No default password no login page
    if "URL=/verba/" in response.text:
        return "VERINT Verba" # No default password
    if "Cisco Unified Communications Manager" in response.text or "Cisco Unified Communications Self Care Portal" in response.text:
        return "Cisco Unified Communications Manager/Self Care Portal Portal" # No default password no login page
    if "<title>RSA Security Analytics Login</title>" in response.text:
        return "RSA Security Analytics" # No default password
    if "FortiWeb" in response.text:
        return "FortiWeb" # No default password
    if "You Know, for Search" in response.text:
        return "Elastic cluster version endpoint" # No login
    if "Installed Applications" in response.text and "Cisco Systems logo" in response.text:
        return "Cisco generic portal" # No login
    if "ephemeral_id" in response.text and "username" in response.text and "pipeline" in response.text:
        return "Generic logstash version portal" # No login
    if "/core/console/console.html" in response.url:
        return "Dell OpenManage Enterprise" # No login
    if "Serv-U FTP Server" in response.text:
        return "Serv-U FTP Server" # No default password
    if "Please return to Webex Control Hub" in response.text:
        return "Cisco Webex" # No default password
    if "window['nprintingVersion']" in response.text and "window['npProject'] = \"newsstand\"":
        return "NPRinting NewsStand" # No default password
    if "NodeManager information" in response.text and "hadoop" in response.text:
        return "hadoop" # No login page
    if "it works!" in response.text.lower():
        return "it works!" # No login page
    if "truenas_core_logomark" in response.text.lower():
        return "TrueNAS" # No default password
    if "strapi" in response.text.lower():
        return "Strapi" # No default password
    if " <title>Communication Manager</title>" in response.text:
        return "Crane Communication Manager" # No default password
    if "crane-cdp.svg" in response.text and "<title>Loyalty - Login</title>":
        return "Crane CDP" # No default password
    if '<title ng-bind="mnTitle">Couchbase Server</title>' in response.text:
        return "Couchbase Server" # No default password
    if "<title>Business Performance Index - BPI</title>" in response.text:
        return "Crane BPI" # No default password
    if "<title>Oracle HTTP Server" in response.text:
        return "Oracle HTTP Server Homepage" # No login
    if "Prometheus Time Series Collection and Processing Server" in response.text:
        return "Prometheus Time Series Collection and Processing Server" # No login
    if "If you're seeing this, you've successfully installed Tomcat. Congratulations!" in response.text:
        return "Apache Tomcat Default homepage" # No login
    if "<title>Eureka</title>" in response.text and "<h1>System Status</h1>" in response.text:
        return "Eureka" # No login
    if "<title>Test Page for the Nginx HTTP Server on" in response.text:
        return "Test Page for the Nginx HTTP Server" # No login 
    if "<title>Wazuh</title>" in response.text:
        return "Wazuh" # No default password
    if "<title>Login | crane CGO</title>" in response.text:
        return "Crane CGO" # No default password
    if "<title>Portainer</title>" in response.text:
        return "Portainer" # No default password
    if "HELP jvm_info VM version info" in response.text:
        return "jvm debug" # No login
    if "<title>Log in | Django site admin</title>" in response.text:
        return "Django administration" # No default password
    if '<font color="blue">new </font><font color="black">SALicInterfaceClient</font>' in response.text:
        return "SALicInterfaceClient" # No login
    if "<title> Dynamic Workload Console </title>" in response.text:
        return "IBM Workload Scheduler" # No default password
    if "<title>DMS Spy</title>" in response.text:
        return "DMS Spy" # No default password
    if "<title>Oracle Enterprise Performance Management System Workspace, Fusion Edition</title>" in response.text:
        return "Oracle Enterprise Performance Management System Workspace, Fusion Edition" # No default password
    if '<font color="teal">WCFCommunicationInitialMetadataServiceClient</font>' in response.text:
        return "WCFCommunicationInitialMetadataServiceClient" # No login page
    if "<title>cAdvisor" in response.text:
        return "cAdvisor" # No login page
    if "<title>Graylog Web Interface</title>" in response.text:
        return "Graylog Web Interface" # No default password
    if '"NAME":"CentOS Linux","ID":"centos"' in response.text:
        return "CentOS Web Interface" # No default password

def check_if_manual(response):
    if "Sign in to RStudio" in response:
        return "RSTUDIO => rstudio:rstudio"
    if "Sign in to Posit Workbench" in response:
        return "POSIT WORKBENCH => rstudio:rstudio"
    if "GetDocLink.ashx?link=logon_troubleshooting" in response:
        return "Xperience => administrator:(blank)"
    if "Enable it to login into Central server" in response:
        return "Endpoint Central => admin:admin"
    if "ecs-loader" in response:
        return "DELL EMC ECS => root:ChangeMe emcsecurity:ChangeMe"
    if "<title>Allegro Packets Network Multimeter - Login</title>" in response:
        return "Allegro Packets Network Multimeter => admin:allegro"
    if "<title>Virtual Appliance Management Infrastructure</title>" in response:
        return "Avamar => root:avam@r"
    return None

def find_login(response):
    if "SAS Web Application Server" in response:
        return "/SASLogon/login"
    if "URL='/ui'" in response:
        return "/ui/#/login"
    return None

def solve_http_status(url):
    for u in urls_to_try:
        response = requests.get(url + u, allow_redirects=True, verify=False, timeout=15)
        if response.status_code in [200]:
            return response.url


# TO DO:
def find_title(url, response):
    soup = BeautifulSoup(response, 'html.parser')
    title_tag = soup.title
    if title_tag and title_tag.string:
        return title_tag.string.strip()

    if "/cgi/login.cgi" in response and "Insyde Software" in response:
        return "Veritas Remote Management"
    if "https://tomcat.apache.org" in response:
        return "Tomcat (No Version)"
    
    return ""

def authcheck(url, templates, verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, bads_lock, wasprocessed = False, is_solved = False):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    hostname = None
    try:
        response = requests.get(url, allow_redirects=True, headers=headers, verify=False, timeout=15)

        # Find if there was a redirect thru meta tag
        match = re.search(r'<meta .*;URL=(.*)"\s*', response.text, re.IGNORECASE)
        if match:
            redirect_url = match.group(1)
            redirect_url = redirect_url.strip("'")
            redirect_url = redirect_url.strip("\"")
            redirect_url = redirect_url.strip(".")
            authcheck(url + redirect_url, templates, verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, bads_lock, wasprocessed)
            return
        try:
            pattern = r'https?://(.*):'
            match_hostname = re.match(pattern, url)
            if match_hostname:
                ip = match_hostname.group(1)

                hostname, _, _ = socket.gethostbyaddr(ip)
        except:pass

        if response.status_code >= 400:
            if not is_solved: 
                zz = solve_http_status(url)
                if zz: 
                    authcheck(zz, templates, verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, bads_lock, wasprocessed, True)
                    return

            if verbose:
                print(f"{url} => {response.status_code}")
            with error_lock:
                with open("witnesschangeme-error.txt", "a") as file:
                    file.write(f"{url}{f" | {hostname}" if hostname else ""} => {response.status_code}\n")
            return
        if response.headers.get("Content-Length") == "0" or response.text.lower() == "ok" or response.text.lower() == "hello world!":
            with bads_lock:
                with open("witnesschangeme-known-bad.txt", "a") as file:
                    file.write(f"{url}{f" | {hostname}" if hostname else ""} => Empty or 'OK'\n")
            return
    except Exception as e:
        with error_lock:
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => {e.__class__.__name__} {e}\n")
        return
    
    bad = check_if_known_Bad(response)
    if bad:
        with bads_lock:
            with open("witnesschangeme-known-bad.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => {bad}\n")
        return

    manual = check_if_manual(response.text)
    if manual:
        with manual_lock:
            with open("witnesschangeme-manual.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => {manual}\n")
        return

    # NO AUTH
    if "Grafana" in response.text and "login" not in response.url:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => GRAFANA NO AUTH\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => Grafana NO AUTH")
    if "Loading Elastic" in response.text and "spaces/space_selector" in response.url:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => ELASTIC NO AUTH\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => Elastic NO AUTH")
    if "WebSphere Integrated Solutions Console" in response.text and "Password" not in response.text:
        with valid_lock:
            with open("witnesschangeme-valid.txt", "a") as file:
                file.write(f"{url} => WebSphere Integrated Solutions Console NO AUTH\n")
        print(f"{url}{f" | {hostname}" if hostname else ""} => WebSphere Integrated Solutions Console NO AUTH")


    try:
        for _, template in templates.items():
            if verbose:
                print(f"Trying {template["name"]}")
            if template["check"](response.text):
                template["verify_login"](url, valid_lock, valid_template_lock, verbose)
                return

        title = find_title(url, response.text)
        # vmware esxi    # In website was not identified, so we tried to identify it:
        if not wasprocessed:
            if """<meta http-equiv="refresh" content="0;URL='/ui'"/>""" in response.text:
                authcheck(url + "/ui", templates, verbose, error_lock, valid_lock, valid_url_lock, valid_template_lock, bads_lock, True)
                return

        with valid_url_lock:
            with open("witnesschangeme-valid-url-no-template.txt", "a") as file:
                lin = check_if_loginpage_exists(response.text)
                file.write(f"{url}{f" => {title}" if title else ""}{f" (Login)" if lin else ""}\n")
                return

    except TimeoutError as timeout:
        with error_lock:
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => Timeout\n")
                return
    except Exception as e:
        with error_lock:
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url}{f" | {hostname}" if hostname else ""} => {e.__class__.__name__} {e}\n")
                return



def main():
    parser = argparse.ArgumentParser(description="Witnesschangeme - Website Default Credentials Authentication Checker")
    parser.add_argument("-t", required=True, help="Target URL/file to test.")
    parser.add_argument("--threads", type=int, default=10, help="Number of threads to use. (Default = 10)")
    parser.add_argument("--dns-ip", type=str, help="DNS ip to do reverse DNS lookup")
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