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


def nofluffjobs_check_if_results_exist(webdriver):
    """Check if results exist on No Fluff Jobs."""
    empty_search = "nfj-no-offers-found-header"
    try:
        no_offers_block = webdriver.find_element(By.CSS_SELECTOR, empty_search)
        if no_offers_block:
            no_offers_text = no_offers_block.text
            if "Brak wyników wyszukiwania" in no_offers_text:
                print(f"No offers found for NoFluffJobs: {webdriver.current_url}")
                return True
    except Exception as e:
        pass
