from selenium.webdriver.common.by import By


def pracujpl_click_multi_location_offer(webdriver):
    """Open all multilocation records to get offer link."""
    css_selector = '[data-test-location="multiple"]'
    try:
        elements = webdriver.find_elements(By.CSS_SELECTOR, css_selector)
        for element in elements:
            element.click()
    except Exception as e:
        pass


def pracujpl_confirm_cookies(webdriver):
    """Confirm cookies on Pracuj.pl."""
    css_selector = '[data-test="button-submitCookie"]'
    try:
        element = webdriver.find_element(By.CSS_SELECTOR, css_selector)
        element.click()
    except Exception as e:
        pass
