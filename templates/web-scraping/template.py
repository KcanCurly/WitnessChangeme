import os
from selenium.webdriver.common.by import By

def verify_login(driver, username, password):
    # Logic to verify login success
    try:

        username_field = driver.driver.find_element(By.NAME, "username")
        password_field = driver.driver.find_element(By.NAME, "password")
        login_button = driver.driver.find_element(By.CSS_SELECTOR, "button.btn.btn-primary[type='submit']")

        
        username_field.send_keys(username)
        password_field.send_keys(password)
        login_button.click()

        return "The secret message is" in driver.driver.page_source
    except Exception as e:
        print(e)
        return False

def get_template():
    # Load credentials and images dynamically
    current_dir = os.path.dirname(os.path.abspath(__file__))
    creds_file = os.path.join(current_dir, "creds.txt")
    images_folder = os.path.join(current_dir, "images")

    with open(creds_file, "r") as f:
        credentials = [tuple(line.strip().split(":")) for line in f if ":" in line]

    return {
        "image_path": images_folder,
        "credentials": credentials,
        "verify_login": verify_login,
        "threshold": 0.5
    }
    
