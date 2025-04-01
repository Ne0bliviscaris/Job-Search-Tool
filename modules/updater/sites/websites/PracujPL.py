import re

from selenium.webdriver.common.by import By

from modules.updater.data_processing.helper_functions import (
    convert_k_notation,
    ensure_string,
    extract_salary_details,
    get_salary_range,
    process_remote_status,
    remove_remote_status,
    salary_cleanup,
    split_salary,
)
from modules.updater.error_handler import no_offers_found, scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class PracujPL(JobSite):
    """Class to scrape website."""

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        return '[data-test="section-offers"]'

    @staticmethod
    def records_list(html) -> list:
        """Extracts job records from HTML."""
        try:
            record_container = {"data-test": "default-offer"}
            records = html.find_all(attrs=record_container)
            return [record for record in records]
        except:
            print("Error detecting records: Pracuj.pl")
            return []

    def website(self) -> str:
        """Returns site name as link."""
        return "Pracuj.pl"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        container = {"data-test": "link-offer"}
        url_a = self.html.find("a", container)
        if url_a:
            return url_a.get("href")

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        container = {"data-test": "offer-title"}
        return self.html.find("h2", container).text.strip()

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        container = {"data-test": "technologies-item"}
        tags_block = self.html.find_all("span", container)
        tags_list = [tag.text.strip() for tag in tags_block]
        if tags_list:
            return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        return self.html.find("h3", {"data-test": "text-company-name"}).text.strip()

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        logo = self.html.find("img", {"data-test": "image-responsive"})
        return logo["src"] if logo else None

    @scraping_error_handler
    def location(self):
        """Extract location from record."""
        loc = self.html.find("h4", {"data-test": "text-region"})

        if not loc:
            return None

        if not multiloc_offer(loc):
            location = loc.text
            return remove_remote_status(location)
        else:
            return handle_multiloc(self.html)

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from record."""
        tag_name = "offer-additional-info"
        additional_info_containers = lambda tag: tag.has_attr("data-test") and tag["data-test"].startswith(tag_name)
        additional_info = self.html.find_all(additional_info_containers)
        status = additional_info[-1].text
        return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary information."""
        salary_container = self.html.find("span", {"data-test": "offer-salary"})
        if salary_container:
            return salary_container.text.strip()

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """
        Fetch salary range and additional salary details from the job listing HTML.
        """
        salary = self.salary_container()
        if not salary:
            return None, None, None, None

        salary_text = ensure_string(salary)
        if salary_text:
            cleaned_salary = salary_cleanup(salary_text)
            salary_details = extract_salary_details(cleaned_salary, salary_text)
            converted_salary = convert_k_notation(cleaned_salary)
            processed_salary = get_salary_range(converted_salary)

            try:
                min_salary, max_salary = split_salary(processed_salary)
                return min_salary, max_salary, salary_details, salary_text

            except ValueError:
                print(f"Error processing data from record: {self.website} -> Salary range")
                return None, None, salary_details, salary_text

        return None, None, None, None

    def scrape(self, webdriver):
        """Scrape given link using Selenium."""
        webdriver.get(self.search_link)
        try:
            search_block = webdriver.find_element(By.CSS_SELECTOR, self.search_container())
            return search_block.get_attribute("outerHTML")
        except:
            return no_offers_found(self.website, self.search_link)


def perform_additional_action(webdriver):
    """Performs additional actions needed for scraping the website."""
    pracujpl_confirm_cookies(webdriver)
    pracujpl_click_multi_location_offer(webdriver)


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


def multiloc_offer(loc):
    """Check if the job listing is a multilocation offer."""
    multiloc_pattern = r"[0-9]+ lokalizacj"
    multiloc_match = re.findall(multiloc_pattern, loc.text)
    if multiloc_match:
        return True
    return False


def handle_multiloc(html):
    """Handle multilocation records."""
    wybierz_lokalizacje = html.find("p", text="Wybierz lokalizację")
    loc_selector = wybierz_lokalizacje.parent
    multi_loc = loc_selector.find_all("a", {"data-test": "link-offer"})
    locations = [location.text for location in multi_loc]
    return TAG_SEPARATOR.join(locations)
