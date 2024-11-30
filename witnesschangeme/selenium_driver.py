from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class SeleniumDriver:
    def __init__(self, timeout=10):
        """
        Initialize the SeleniumDriver with options for headless browsing and timeout.
        
        :param headless: Whether to run the browser in headless mode.
        :param timeout: The default timeout for page load and element interactions.
        """
        self.timeout = timeout
        self.driver = self._initialize_driver()

    def _initialize_driver(self):
        """Set up and return a Selenium WebDriver instance."""
        firefox_options = Options()
        firefox_options.binary_location = r'C:\Users\Admin\Downloads\geckodriver-v0.35.0-win32\geckodriver.exe'
        firefox_options.add_argument("--disable-gpu")
        firefox_options.add_argument("--no-sandbox")
        firefox_options.add_argument("--disable-dev-shm-usage")
        firefox_options.add_argument("--headless")

        # Enable request interception to handle redirects
        caps = DesiredCapabilities.FIREFOX
        caps["goog:loggingPrefs"] = {"performance": "ALL"}

        driver = webdriver.Firefox(options=firefox_options)

        driver.set_page_load_timeout(self.timeout)
        return driver


    def quit(self):
        """Close the browser and clean up resources."""
        self.driver.quit()
