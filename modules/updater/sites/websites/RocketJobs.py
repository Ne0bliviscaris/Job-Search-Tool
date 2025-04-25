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


class RocketJobs(JobSite):
    """Class to scrape website."""

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        return '[data-test-id="virtuoso-item-list"]'

    @staticmethod
    def records_list(html) -> list:
        """Extracts job records from HTML."""
        try:
            record_container = {"data-index": True}
            records = html.find_all(attrs=record_container)
            return [record for record in records]
        except:
            print("Error detecting records: RocketJobs.pl")

    def website(self) -> str:
        """Returns site name as link."""
        return "Rocketjobs.pl"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        relative_link = self.html.a.get("href")
        return f"https://{self.website}/{relative_link}"

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        title = self.html.h3
        return title.text.strip() if title else None

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        name = lambda class_name: class_name and class_name.startswith("skill-tag")
        tags = self.html.find_all(class_=name)
        tags_list = [tag.text for tag in tags]
        if tags_list:
            return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        company_icon = {"data-testid": "ApartmentRoundedIcon"}
        svg_icon = self.html.find("svg", company_icon)
        if svg_icon:
            parent_name = lambda class_name: class_name and class_name.startswith("MuiBox-root")
            parent_div = svg_icon.find_parent("div", class_=parent_name)
            company = parent_div.span
            return company.text if company else None

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        logo = self.html.img
        return logo.get("src") if logo else None

    @scraping_error_handler
    def location(self):
        """Extract location from job record."""
        company_icon = {"data-testid": "PlaceOutlinedIcon"}
        svg_icon = self.html.find("svg", company_icon)
        if svg_icon:
            parent_block_class = lambda class_name: class_name and class_name.startswith("MuiBox-root")
            parent_div = svg_icon.find_parent("div", class_=parent_block_class)
            if parent_div and parent_div.span:
                location = parent_div.span.text
                return remove_remote_status(location)

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from job record."""
        location_icon = {"style": "display:block"}
        location = self.html.find("div", location_icon)
        if location:
            parent_div = location.find_parent("div")
            if parent_div:
                status = parent_div.text.lower()
                return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        # All containers on site are MuiBox-root. Need to find the right one
        MuiBox_block = lambda class_name: class_name and class_name.startswith("MuiBox-root")
        # Salary is in sibling div to the one containing title (h3)
        h3_container = self.html.h3
        if h3_container:
            parent_div = h3_container.find_parent("div", class_=MuiBox_block)
            salary_block = parent_div.find_next_sibling("div", class_=MuiBox_block)
            # Salary is in <span> inside the parent div of <h3>
            if salary_block:
                salary = salary_block.text.replace("New", "")
                return salary

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """Fetch salary range and details from job listing HTML."""
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
            print(f"Error processing data from record: {self.website} -> Salary range")
            return None, None, salary_details, salary_text

    def scrape(self, webdriver):
        """Scrape given link using Selenium."""
        webdriver.get(self.search_link)
        try:
            search_block = webdriver.find_element(By.CSS_SELECTOR, self.search_container())
            return search_block.get_attribute("outerHTML")
        except:
            return no_offers_found(self.website, self.search_link)


def stop_scraping(webdriver):
    """Check if search returned no results."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(webdriver.page_source, "html.parser")
    try:
        empty_search = "Nie znaleźliśmy ofert pracy dla podanych kryteriów"
        empty_search_container = soup.find(text=lambda text: empty_search in text)
        if empty_search_container:
            return True
    except:
        return False
