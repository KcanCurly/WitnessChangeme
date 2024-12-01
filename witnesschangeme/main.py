import argparse
import importlib.resources
import os
import importlib.util
import importlib
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor   
import requests
from witnesschangeme.utils import append_random_characters
from pyautogui import locate
import pyautogui
from witnesschangeme.selenium_driver import SeleniumDriver

if os.name == "posix":
    from pyvirtualdisplay.display import Display
    import Xlib.display

from pkg_resources import resource_string, resource_listdir, resource_isdir


def authcheck(url, template, driver, output_folder):
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, allow_redirects=True, headers=headers)
    if response.status_code >= 400:
        print(f"{url} returned {response.status_code}", f"{output_folder}/invalid_urls.txt")
        return
    
    driver.driver.get(url)
    
    p = append_random_characters("ss_") + ".png"
    p = Path(__file__).resolve().parent.parent / "temp" / p
    driver.driver.save_screenshot(p)
    
    try:
        template_path = template["image_path"]
        template_path += r"\1.png"
        locate(template_path, p.__str__(), confidence=template["threshold"])
        
        found = False
        
        for username, password in template["credentials"]:
            if template["verify_login"](driver, username, password):
                print(f"Login successful: {username}", f"{output_folder}/successful_logins.txt")
                found = True
                # save_screenshot(self.driver, f"{self.output_dir}/successful_logins/{username}.png")
                break
        
        if not found:
            print(f"Login failed for {url}", f"{output_folder}/failed_logins.txt")
            return
        
    except Exception as e:
        raise e

    finally:
        os.remove(p)

def main():
    parser = argparse.ArgumentParser(description="Witnesschangeme - Website Authentication Checker")
    parser.add_argument("--url", required=True, help="Target URL to test.")
    parser.add_argument("--output-dir", default="output/", help="Directory to save results.")
    args = parser.parse_args()
    
    if os.name == "posix":
        # Start fake display
        disp = Display(visible=True, size=(1920,1080), backend="xvfb", use_xauth=True)
        disp.start()
        pyautogui._pyautogui_x11._display = Xlib.display.Display(os.environ["DISPLAY"])

    with importlib.resources.path("templates", "") as a:
        print(a)


            

    
    return
    # Load all templates
    templates = {}
    current_script = Path(__file__).resolve()
    base_path = os.path.join(current_script.parent.parent, "templates")
    template_folders = []
    for folder in os.listdir(base_path):
        if os.path.isdir(os.path.join(base_path, folder)):
            template_folders.append(folder)
    
    for template in template_folders:        
        template_path = os.path.join(Path(__file__).resolve().parent.parent, "templates", template, "template.py")
        spec = importlib.util.spec_from_file_location("template", template_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        t = module.get_template()
        templates[folder] = t

    print(f"Loaded {len(templates)} templates: {', '.join(templates.keys())}")
    
    print("Creating Selenium Driver")
    driver = SeleniumDriver()
    print("Created Selenium Driver")
    
    # If given url is a file, read it line by line and run the templates on each line
    if os.path.isfile(args.url):
        with open(args.url, 'r') as file:
            for line in file:
                for template_name, template in templates.items():
                    print(f"Running template: {template_name} for {line}")
                    authcheck(line, template, driver, args.output_dir)

                    
    # If given url is simply a website, run the templates on the website
    else:
        for template_name, template in templates.items():
            print(f"Running template: {template_name}")
            authcheck(args.url, template, driver, args.output_dir)
    
    print("Quiting Selenium Driver")        
    driver.quit()
    print("Quitted Selenium Driver")
    

if __name__ == "__main__":
    main()