import argparse
import importlib.resources
import importlib.resources.simple
import os
import importlib.util
import importlib
import requests
from witnesschangeme.utils import append_random_characters
from pyautogui import locate
import pyautogui
from witnesschangeme.selenium_driver import SeleniumDriver
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import all_of
from selenium.webdriver.common.by import By

if os.name == "posix":
    from pyvirtualdisplay.display import Display
    import Xlib.display

from pkg_resources import resource_string, resource_listdir, resource_isdir
disable_warnings(InsecureRequestWarning)

def authcheck(url, templates, driver: None, output_folder, pyautogui, selenium, verbose):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, allow_redirects=True, headers=headers, verify=False, timeout=15)
        if response.status_code >= 400:
            if verbose:
                print(f"{url} => {response.status_code}")
            with open("witnesschangeme-error.txt", "a") as file:
                file.write(f"{url} => {response.status_code}\n")
            return
    except Exception as e:
        with open("witnesschangeme-error.txt", "a") as file:
            file.write(f"{url} => {e.__class__.__name__}\n")
        return
    
    if not selenium:
        for _, template in templates.items():
            if verbose:
                print(f"Trying {template["name"]}")
            if template["check"](response.text):
                template["verify_login2"](url)
        return

    if "/app/home" in response.url and "Observability" in response.text:
        print(f"{url} => Unauthenticated ELASTIC")
        with open("witnesschangeme-valid.txt", "a") as file:
            file.write(f"{url} => Unauthenticated ELASTIC\n")
        return
    if verbose:
        print(f"{url} => {response.status_code}, proceeding with selenium")
    try:
        driver.driver.get(url)
   
        # IDRAC HACK
        if driver.driver.current_url.endswith("/restgui/start.html"):
            if verbose:
                print("IDRAC HACK activated, waiting 60 seconds")
            WebDriverWait(driver.driver, 60).until(
                EC.visibility_of_element_located((By.XPATH, "//button[@type='submit']"))
            )
            if verbose:
                print("IDRAC HACK ended")

        if pyautogui:
            p = append_random_characters("ss_") + ".png"
            p = os.path.join(os.getcwd(), p)
            driver.driver.save_full_page_screenshot(p)

        for _, template in templates.items():
            if verbose:
                print(f"Trying {template["name"]}")
            try:
                template_path = template["image_path"]
                template_path = os.path.join(template_path, "1.png")
                
                if pyautogui:
                    locate(template_path, p.__str__(), confidence=template["threshold"])
                else:
                    if not template["check"](response.text):
                        continue

                if verbose:
                    print(f"{template["name"]} matched, trying credentials")
            
                found = False
                
                for username, password in template["credentials"]:
                    if template["verify_login"](driver, username, password):
                        with open("witnesschangeme-valid.txt", "a") as file:
                            file.write(f"{url} => {template["name"]} => {username}:{password}\n")
                        print(f"{url} => {template["name"]} => {username}:{password}\n")

                        found = True
                        if pyautogui:
                            os.remove(p)
                        # save_screenshot(self.driver, f"{self.output_dir}/successful_logins/{username}.png")
                        return
                

                if not found:
                    if pyautogui:
                        os.remove(p)
                    if verbose:
                        print(f"Login failed")
                    with open("witnesschangeme-valid-template-no-credential.txt", "a") as file:
                        file.write(f"{url} => {template["name"]}\n")
                    return

            except Exception as e:
                print(e)
        
        if pyautogui:
            os.remove(p)

        with open("witnesschangeme-valid-url-no-template.txt", "a") as file:
            file.write(f"{url}\n")

    except Exception as e:
        with open("witnesschangeme-error.txt", "a") as file:
            file.write(f"{url} => {e.__class__.__name__}\n")
        return     


def main():
    parser = argparse.ArgumentParser(description="Witnesschangeme - Website Authentication Checker")
    parser.add_argument("-t", required=True, help="Target URL to test.")
    parser.add_argument("--pyautogui", default=False, help="Use pyautogui to compare template")
    parser.add_argument("--output-dir", default="output/", help="Directory to save results.")
    parser.add_argument("--use-selenium", default=False, help="Use selenium for authentication checks.")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output.")
    args = parser.parse_args()
    pyautogui.useImageNotFoundException(True)
    if os.name == "posix":
        # Start fake display
        disp = Display(visible=True, size=(1920,1080), backend="xvfb", use_xauth=True)
        disp.start()
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])

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
    driver = None
    if args.use_selenium:
        if args.verbose:
            print("Creating Selenium Driver")
        driver = SeleniumDriver(15)
        if args.verbose:
            print("Created Selenium Driver")
    
    # If given url is a file, read it line by line and run the templates on each line
    if os.path.isfile(args.t):
        with open(args.t, 'r') as file:
            for line in file:
                authcheck(line.strip(), templates, driver, args.output_dir, args.pyautogui, args.use_selenium, args.verbose)
                    

                    
    # If given url is simply a website, run the templates on the website
    else:
        authcheck(args.t, templates, driver, args.output_dir, args.pyautogui, args.use_selenium, args.verbose)
    
    if args.use_selenium:
        if args.verbose:
            print("Quiting Selenium Driver")        
        driver.quit()
        if args.verbose:
            print("Quitted Selenium Driver")
    

if __name__ == "__main__":
    main()