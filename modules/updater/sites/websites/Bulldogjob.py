import requests
from bs4 import BeautifulSoup

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


class Bulldogjob(JobSite):
    """Class to scrape website."""

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        return "div#__next"

    @staticmethod
    def records_list(html) -> list:
        """Extracts job records from HTML."""
        try:
            block_name = lambda class_name: class_name and class_name.startswith("JobListItem_item")
            record_container = {"class": block_name}
            records = html.find_all("a", attrs=record_container)
            return [record for record in records]
        except:
            print("Error detecting records: BULLDOGJOB")
            return []

    def website(self) -> str:
        """Returns site name as link."""
        return "Bulldogjob.pl"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        return self.html.get("href")

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        block_name = lambda class_name: class_name and class_name.startswith("JobListItem_item__title")
        container = {"class": block_name}
        title_block = self.html.find(attrs=container).h3
        return title_block.text.strip()

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        name = lambda class_name: class_name and class_name.startswith("JobListItem_item__tags")
        tags_container = {"class": name}
        tags_block = self.html.find(attrs=tags_container)
        if tags_block:
            tags_list = [span.text.strip() for span in tags_block.find_all("span")]
            return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        name = lambda class_name: class_name and class_name.startswith("JobListItem_item__title")
        title_company_container = {"class": name}
        title_company_block = self.html.find(attrs=title_company_container)
        # Find the <h3> tag with offer title and get the <div> sibling
        title_container = title_company_block.h3
        return title_container.find_next_sibling("div").text.strip()

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        logo_container = {"class": lambda class_name: class_name and class_name.startswith("JobListItem_item__logo")}
        if logo_container:
            return self.html.find(attrs=logo_container).img["src"]

    @scraping_error_handler
    def location(self):
        """Extract location from record."""
        name = lambda class_name: class_name and class_name.startswith("JobListItem_item__details")
        details_block = self.html.find(attrs={"class": name})

        location_block = details_block.div.div
        if location_block:
            spans = location_block.find_all("span")
            location_texts = [span.text.strip() for span in spans]
            location = " | ".join(location_texts)
            return remove_remote_status(location)
        return None

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from record."""
        container_name = "JobListItem_item__details"
        remote_container = lambda class_name: class_name and class_name.startswith(container_name)
        details_block = self.html.find(attrs={"class": remote_container})
        if details_block:
            first_block = details_block.div
            if first_block:
                status = first_block.text
        return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        container_name = "JobListItem_item__salary"
        salary_container = lambda class_name: class_name and class_name.startswith(container_name)
        container = self.html.find(attrs={"class": salary_container})
        if container:
            return container.text

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

    def scrape(self, webdriver=None) -> str:
        """Scrape given link using Selenium."""
        response = requests.get(self.search_link)
        soup = BeautifulSoup(response.text, "html.parser")
        if stop_scrape(soup):
            return no_offers_found(self.website, self.search_link)
        search_block = soup.select_one(self.search_container())
        return search_block if search_block else ""


def stop_scrape(soup):
    empty_search = "Brak wyników pasujących do wyszukiwania"
    if soup and empty_search in soup.text:
        return True
    return False
