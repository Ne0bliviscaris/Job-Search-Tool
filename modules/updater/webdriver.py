from selenium import webdriver

from modules.settings import CHROMEDRIVER_CONTAINER


def setup_webdriver():
    """Setup and return a Selenium WebDriver instance"""
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
