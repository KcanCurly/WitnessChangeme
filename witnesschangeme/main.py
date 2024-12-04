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

if os.name == "posix":
    from pyvirtualdisplay.display import Display
    import Xlib.display

from pkg_resources import resource_string, resource_listdir, resource_isdir
disable_warnings(InsecureRequestWarning)

def authcheck(url, templates, driver, output_folder):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, allow_redirects=True, headers=headers, verify=False)
    if response.status_code >= 400:
        print(f"{url} returned {response.status_code}")
        return
    
    driver.driver.get(url)

    WebDriverWait(driver, 10).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    
    p = append_random_characters("ss_") + ".png"
    with importlib.resources.path("temp", "") as b:
        p = os.path.join(os.getcwd(), p)
        driver.driver.save_full_page_screenshot(p)

        for template_name, template in templates.items():
            print(f"Triyng {template["name"]}")
            try:
                template_path = template["image_path"]
                template_path = os.path.join(template_path, "1.png")
                
                # try:
                locate(template_path, p.__str__(), confidence=template["threshold"])
                print(f"{template["name"]} matched, trying credentials")
            
                found = False
                
                for username, password in template["credentials"]:
                    if template["verify_login"](driver, username, password):
                        print(f"Login successful: {username}")
                        found = True
                        # save_screenshot(self.driver, f"{self.output_dir}/successful_logins/{username}.png")
                        break
                
                if not found:
                    print(f"Login failed")
                    return

            except Exception as e:
                print(e)

        # os.remove(p)

def main():
    parser = argparse.ArgumentParser(description="Witnesschangeme - Website Authentication Checker")
    parser.add_argument("--url", required=True, help="Target URL to test.")
    parser.add_argument("--output-dir", default="output/", help="Directory to save results.")
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
                

    print(f"Loaded {len(templates)} templates: {', '.join(templates.keys())}")
    
    print("Creating Selenium Driver")
    driver = SeleniumDriver()
    print("Created Selenium Driver")
    
    # If given url is a file, read it line by line and run the templates on each line
    if os.path.isfile(args.url):
        with open(args.url, 'r') as file:
            for line in file:
                authcheck(line, templates, driver, args.output_dir)
                    

                    
    # If given url is simply a website, run the templates on the website
    else:
        authcheck(args.url, templates, driver, args.output_dir)
    
    print("Quiting Selenium Driver")        
    driver.quit()
    print("Quitted Selenium Driver")
    

if __name__ == "__main__":
    main()