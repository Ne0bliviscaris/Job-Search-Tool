from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import modules.updater.scraper.site_specific_actions as site_specific_actions
from modules.settings import CHROMEDRIVER_CONTAINER
from modules.updater.sites.JobSite import JobSite
from modules.websites import NOFLUFFJOBS, PRACUJPL


def scrape(web_driver, job_site: JobSite) -> str:
    """Scrape given link using Selenium."""
    web_driver.get(job_site.search_link)
    job_site.perform_additional_action(web_driver)
    stop_scraping = job_site.stop_scraping(web_driver)

    if stop_scraping is True:
        return ""

    search_block = web_driver.find_element(By.CSS_SELECTOR, job_site.search_container())
    return search_block.get_attribute("outerHTML") or ""


def wait_for_content(driver, search_container, timeout=10):
    """Wait for element to be present and contain content."""
    wait = WebDriverWait(driver, timeout)
    page_content = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, search_container)))

    page_content_loaded = len(page_content.text.strip()) > 0
    wait.until(lambda d: page_content_loaded)
    return page_content


def perform_additional_action(driver: webdriver.Chrome, search_link: str):
    """Perform additional actions depending on the page."""
    if PRACUJPL in search_link:
        site_specific_actions.pracujpl_confirm_cookies(driver)
        site_specific_actions.pracujpl_click_multi_location_offer(driver)


def evaluate_stop_conditions(web_driver, search_link: str) -> bool:
    """Check if the stop conditions are met."""
    if NOFLUFFJOBS in search_link:
        return site_specific_actions.nofluffjobs_check_if_results_exist(web_driver)
    return False


def setup_webdriver():
    """
    Setup and return a Selenium WebDriver instance
    """
    # Path to container with Chrome
    options = set_chromedriver_options()
    driver = webdriver.Remote(command_executor=CHROMEDRIVER_CONTAINER, options=options)
    driver.set_page_load_timeout(15)
    return driver


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
    # options.add_argument("--disable-blink-features=AutomationControlled")  # Try to avoid detection
    # options.add_argument("--disable-extensions")
    return options
