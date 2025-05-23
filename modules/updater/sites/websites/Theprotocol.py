from bs4 import BeautifulSoup
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
from modules.updater.data_processing.site_files import load_html_as_soup, save_html
from modules.updater.error_handler import no_offers_found, scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class Theprotocol(JobSite):
    """Class to scrape website."""

    @staticmethod
    def file_extension():
        return "html"

    def save_file(self, filename, html):
        """Save HTML content to a file."""
        save_html(filename, html)

    def load_file(self, filename):
        """Load HTML content from a file."""
        return load_html_as_soup(filename)

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        return '[data-test="offersList"]'

    @staticmethod
    def records_list(data) -> list:
        """Extracts job records from HTML."""
        try:
            record_container = {"data-test": "list-item-offer"}
            records = data.find_all(attrs=record_container)
            return [record for record in records]
        except:
            print("Error detecting records: Theprotocol")

    def website(self) -> str:
        """Returns site name as link."""
        return "Theprotocol.it"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        relative_url = self.html.get("href")
        return f"https://theprotocol.it{relative_url}"

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        container = {"data-test": "text-jobTitle"}
        return self.html.find(attrs=container).text.strip()

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        tags_container = {"data-test": "chip-expectedTechnology"}
        tags = self.html.find_all(attrs=tags_container)
        tags_list = [tag.text for tag in tags]
        return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        company_container = {"data-test": "text-employerName"}
        return self.html.find(attrs=company_container).text.strip()

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        logo_container = {"data-test": "icon-companyLogo"}
        logo = self.html.find(attrs=logo_container)
        if logo:
            return logo.get("src")

    @scraping_error_handler
    def location(self):
        """Extract location from record."""
        single_loc = {"data-test": "text-workplaces"}
        multi_loc = {"data-test": "chip-location"}

        locations_list = self.html.find_all(attrs=multi_loc)
        if locations_list:
            locations = [location.text for location in locations_list]
            return TAG_SEPARATOR.join(locations)
        single_location = self.html.find(attrs=single_loc)
        if single_location:
            location = single_location.text
            return remove_remote_status(location)

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from record."""
        if not self.location:
            return process_remote_status(self.location)

        remote_container = {"data-test": "text-workModes"}
        remote_status = self.html.find(attrs=remote_container)
        if remote_status:
            status = remote_status.text.lower()
        return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        salary_container = {"data-test": "text-salary"}
        salary = self.html.find(attrs=salary_container)
        if salary:
            return salary.text

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """
        Fetch salary range and additional salary details from the job listing HTML.
        """
        salary_text = ensure_string(self.salary_container())
        if not salary_text:
            return None, None, None, None
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

        if stop_scraping(webdriver):
            return no_offers_found(self.website, self.search_link)

        search_block = webdriver.find_element(By.CSS_SELECTOR, self.search_container())
        return search_block.get_attribute("outerHTML")


def stop_scraping(webdriver):
    """Returns stop condition for scraping."""
    try:

        soup = BeautifulSoup(webdriver.page_source, "html.parser")
        no_offers_element = soup.find(attrs={"data-test": "text-emptyList"})
        if no_offers_element:
            return True
    except:
        return False
