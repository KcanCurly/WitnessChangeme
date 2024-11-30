from pathlib import Path
import requests
import pyautogui
import os
from selenium_driver import SeleniumDriver
import random
import string


class AuthChecker:
    def __init__(self, url, template, output_dir):
        self.url = url
        self.template = template
        self.output_dir = output_dir
        self.driver = SeleniumDriver()

    def run(self):
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.get(self.url, allow_redirects=True, headers=headers)
        if response.status_code >= 400:
            print(f"{self.url} returned {response.status_code}", f"{self.output_dir}/invalid_urls.txt")
            return
        

        self.driver.driver.get(self.url)
        

        p = self.append_random_characters("ss_") + ".png"
        p = Path(__file__).resolve().parent.parent / "temp" / p
        self.driver.driver.save_screenshot(p)
        
        try:
            template_path = self.template["image_path"]
            template_path += r"\1.png"
            pyautogui.locate(template_path, p.__str__(), confidence=self.template["threshold"])
            
            found = False
            
            for username, password in self.template["credentials"]:
                if self.template["verify_login"](self.driver, username, password):
                    print(f"Login successful: {username}", f"{self.output_dir}/successful_logins.txt")
                    found = True
                    # save_screenshot(self.driver, f"{self.output_dir}/successful_logins/{username}.png")
                    break
            
            if not found:
                print(f"Login failed for {self.url}", f"{self.output_dir}/failed_logins.txt")
                return
            
        except Exception as e:
            raise e

        finally:
            os.remove(p)
            self.driver.quit()

        
    def append_random_characters(self, base_str, length=6):
        # Define the characters to choose from (letters and digits)
        characters = string.ascii_letters + string.digits
    
        # Generate random characters
        random_suffix = ''.join(random.choices(characters, k=length))
    
        # Append the random characters to the base string
        return base_str + random_suffix