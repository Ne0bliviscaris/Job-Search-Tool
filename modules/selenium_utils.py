from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

import modules.containers as containers
from modules.websites import PRACUJPL


def get_container(driver: webdriver.Chrome, search_link: str) -> str:
    """
    Get the HTML content of the search container using Selenium
    """
    search_container = containers.search(search_link)
    if not search_container:
        print(f"No results for: {search_link}")
        return ""
    try:
        search_block = driver.find_element(By.CSS_SELECTOR, search_container)
        return search_block.get_attribute("outerHTML")
    except Exception as e:
        print(f"No results for: {search_link}")
        return ""


def setup_webdriver() -> webdriver.Chrome:
    """
    Setup and return a Selenium WebDriver instance
    """
    # Local path to chromedriver - static - change if needed
    chromedriver_path = "C:\\Users\\Dragon\\Downloads\\chromedriver-win64\\chromedriver.exe"
    # Create and start ChromeDriver service
    webdriver_service = Service(chromedriver_path)
    webdriver_service.start()

    # Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=old")  # Run Chrome in headless mode - no window is displayed
    options.add_argument("--disable-gpu")  # Disable GPU (optional but recommended in headless mode)
    options.add_argument("--no-sandbox")  # Disable sandbox (optional but may help in some cases)
    options.add_argument("--disable-dev-shm-usage")  # Disable shared memory (optional but may help in some cases)
    options.add_argument("window-size=1920,1080")  # Always force PC version of the website
    options.add_argument("--window-position=-2400,-2400")  # In case blank window is displayed, move it off-screen
    options.add_argument("--log-level=2")  # Hide unnecessary logs
    options.add_argument("--disable-webgl")  # Disable WebGL
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})

    # Return WebDriver instance
    return webdriver.Chrome(service=webdriver_service, options=options)


def scrape(web_driver, search_link: str) -> str:
    """Scrape given link using Selenium."""
    web_driver.get(search_link)
    perform_additional_action(web_driver, search_link)
    html_content = get_container(web_driver, search_link)
    return html_content


def perform_additional_action(driver: webdriver.Chrome, search_link: str) -> None:
    """Perform additional actions depending on the page."""
    if PRACUJPL in search_link:
        pracujpl_confirm_cookies(driver)
        click_pracujpl_multiloc(driver)


def click_pracujpl_multiloc(driver: webdriver.Chrome):
    """Open all multilocation records to get offer link."""
    css_selector = '[data-test-location="multiple"]'
    try:
        elements = driver.find_elements(By.CSS_SELECTOR, css_selector)
        for element in elements:
            element.click()
    except Exception as e:
        pass


def pracujpl_confirm_cookies(driver):
    """Confirm cookies on Pracuj.pl."""
    css_selector = '[data-test="button-submitCookie"]'
    try:
        element = driver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()
    except Exception as e:
        pass
