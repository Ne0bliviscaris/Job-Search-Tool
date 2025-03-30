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
from modules.updater.error_handler import scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class Solidjobs(JobSite):
    """Class to scrape Solidjobs website."""

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        return '[class="scrollable-content"]'

    @staticmethod
    def records_list(html) -> list:
        """Extracts job records from HTML."""
        block_name = "sj-offer-list-item"  # <sj-offer-list-item> block
        records = html.find_all(block_name)
        return [record for record in records]

    def website(self) -> str:
        """Returns site name as link."""
        return "solid.jobs"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        relative_link = self.html.a.get("href")
        return f"https://{self.website}{relative_link}" if relative_link else None

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        title = self.html.h2
        return title.text.strip()

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        tags_block = self.html.find_all("solidjobs-skill-display")
        if tags_block:
            tags_list = [tag.text.replace("#", "") for tag in tags_block]
            if tags_list:
                return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        company = self.html.find("a", {"mattooltip": "Kliknij, aby zobaczy pozostałe oferty firmy."})
        return company.text if company else None

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        logo = self.html.img
        return logo.get("src") if logo else None

    @scraping_error_handler
    def location(self):
        """Extract location from job record."""
        location_container = self.html.find("div", class_="flex-row")
        if location_container:
            location_span = location_container.find_all("span")[1]
            if location_span:
                location = location_span.text.replace("100% zdalnie ", "").replace("(", "").replace(")", "").strip()
                return remove_remote_status(location)

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from job record."""
        location = self.html.find_all("span", {"mattooltip": True})
        if location:
            remote_status = location[-1]
            status = remote_status.text.strip()
            return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        salary_container = self.html.find("sj-salary-display")
        return salary_container.text.strip() if salary_container else None

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """Fetch salary range and details from job listing."""
        salary_text = ensure_string(self.salary_container())
        if not salary_text:
            return None, None, None, None

        cleaned_salary = salary_cleanup(salary_text)
        salary_details = extract_salary_details(cleaned_salary, salary_text)
        converted_salary = convert_k_notation(cleaned_salary)
        processed_salary = get_salary_range(converted_salary)
        try:
            min_salary, max_salary = split_salary(processed_salary)
            return min_salary, max_salary, salary_details, salary_text
        except ValueError:
            print(f"Error processing data from record: {self.website()} -> Salary range")
            return None, None, salary_details, salary_text

    @staticmethod
    def perform_additional_action(webdriver):
        """Performs additional actions needed for scraping the website."""
        return None

    @staticmethod
    def stop_scraping(webdriver):
        """Returns stop condition for scraping."""
        return no_search_block(webdriver)


def no_search_block(webdriver):
    """Check if search block exists on page."""
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.by import By

    search_block = '[class="scrollable-content"]'

    try:
        webdriver.find_element(By.CSS_SELECTOR, search_block)
        # Element found, search block exists
        return False
    except NoSuchElementException:
        # Element not found, no search block
        return True
