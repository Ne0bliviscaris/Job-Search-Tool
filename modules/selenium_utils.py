from selenium import webdriver
from selenium.webdriver.common.by import By

import modules.containers as containers
import modules.site_specific_actions as site_specific_actions
from modules.websites import PRACUJPL


def scrape(web_driver, search_link: str) -> str:
    """Scrape given link using Selenium."""
    web_driver.get(search_link)
    perform_additional_action(web_driver, search_link)
    html_content = get_search_container(web_driver, search_link)
    return html_content


def get_search_container(driver: webdriver.Chrome, search_link: str) -> str:
    """
    Get the HTML content of the search container using Selenium
    """
    search_container = containers.search(search_link)
    if not search_container:
        print(f"Website not supported yet: {search_link}")
        return ""
    try:
        search_block = driver.find_element(By.CSS_SELECTOR, search_container)
        return search_block.get_attribute("outerHTML")
    except Exception as e:
        print(f"Search container empty or not recognized for: {search_link}")
        return ""


def perform_additional_action(driver: webdriver.Chrome, search_link: str):
    """Perform additional actions depending on the page."""
    if PRACUJPL in search_link:
        site_specific_actions.pracujpl_confirm_cookies(driver)
        site_specific_actions.pracujpl_click_multi_location_offer(driver)


def setup_webdriver():
    """
    Setup and return a Selenium WebDriver instance
    """
    # Path to container with Chrome
    docker_chrome_url = "http://localhost:4444/wd/hub"

    options = set_chromedriver_options()

    # Return WebDriver instance
    return webdriver.Remote(command_executor=docker_chrome_url, options=options)


def set_chromedriver_options():
    """Set options for Chrome WebDriver."""
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=old")  # Run Chrome in headless mode - no window is displayed
    options.add_argument("--disable-gpu")  # Disable GPU (optional but recommended in headless mode)
    options.add_argument("--no-sandbox")  # Disable sandbox (optional but may help in some cases)
    options.add_argument("--disable-dev-shm-usage")  # Disable shared memory (optional but may help in some cases)
    options.add_argument("window-size=1920,1080")  # Always force PC version of the website
    options.add_argument("--window-position=-2400,-2400")  # In case blank window is displayed, move it off-screen
    options.add_argument("--log-level=2")  # Hide unnecessary logs
    options.add_argument("--disable-webgl")  # Disable WebGL
    options.add_experimental_option("prefs", {"profile.managed_default_content_settings.images": 2})  # Disable images
    return options
