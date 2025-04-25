import requests
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
from modules.updater.error_handler import no_offers_found, scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class InhireIO(JobSite):
    """Class to scrape website."""

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        ...

    @staticmethod
    def records_list(html) -> list:
        """Extracts job records from HTML."""
        try:
            block_name = lambda id_name: id_name and id_name.startswith("nfjPostingListItem")
            record_container = {"id": block_name}
            records = html.find_all(attrs=record_container)
            return [record for record in records]

        except:
            print("Error detecting records: NoFluffJobs.com")

    def website(self) -> str:
        """Returns site name."""
        return "Inhire.io"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        url = self.html.get("href")
        if url:
            return url if url.startswith("http") else f"https://nofluffjobs.com{url}"

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        container = {"data-cy": "title position on the job offer listing"}
        title = self.html.find(attrs=container)
        if title:
            return title.text.strip()

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        tags_container = {"data-cy": "category name on the job offer listing"}
        tags = self.html.find_all(attrs=tags_container)
        tags_list = [tag.text for tag in tags]
        if tags_list:
            return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        name = lambda x: x and x.startswith("company-name")
        company_container = {"class": name}
        return self.html.find(attrs=company_container).text.strip()

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        img = self.html.find("img")
        if img:
            logo_container = {"alt": "Company logo"}
            logo = self.html.find(attrs=logo_container)
            if logo:
                return logo["src"]

    @scraping_error_handler
    def location(self):
        """Extract location from job record."""
        location_container = {"data-cy": "location on the job offer listing"}
        location_block = self.html.find(attrs=location_container)
        if location_block and location_block.span:
            location = location_block.span.text.strip()
            return remove_remote_status(location)

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from job record."""
        location_container = {"data-cy": "location on the job offer listing"}
        location = self.html.find(attrs=location_container)
        if location:
            return process_remote_status(location.text)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        salary_container = {"data-cy": "salary ranges on the job offer listing"}
        return self.html.find(attrs=salary_container)

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """Fetch salary range and details from job listing HTML."""
        salary_text = ensure_string(self.salary_container())
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

    def scrape(self, webdriver=None):
        """Scrape using API request."""
        all_offers = []
        page = 1

        while True:
            data = self._send_api_request(page)
            # if stop_scraping(data):
            #     return no_offers_found(self.website, self.search_link)

            if not data or len(data) == 0:
                break

            all_offers.extend(data)
            page += 1

        return all_offers

    def _send_api_request(self, page=1):
        """Scrape single page of results."""
        base_url = "https://inhire.io/getAllOffersNonAuth"

        payload = {
            "it_technology_ids": [7],  # Python
            "include_undisclosed": True,
            "it_roles": ["big_data", "data_science", "machine_learning_engineer"],
            "page": page,
        }

        response = requests.post(base_url, json=payload)

        if response.status_code == 200:
            return response.json()["response"]
        return []


def stop_scraping(html):
    """Check if scraping should stop."""
    soup = BeautifulSoup(html, "html.parser")
    try:
        no_results = soup.find("div", {"class": "robot-info-box"})
        if no_results:
            return True
    except:
        return False
