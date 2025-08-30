import httpx
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
from modules.updater.data_processing.site_files import load_html_as_soup, save_html
from modules.updater.error_handler import missing_container_handler, no_offers_found
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class PracujPL(JobSite):
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
        ...

    @staticmethod
    def records_list(data) -> list:
        """Extracts job records from HTML."""
        try:
            record_container = {"data-test": "default-offer"}
            records = data.find_all(attrs=record_container)
            return [record for record in records]
        except Exception:
            print("Error detecting records: Pracuj.pl")
            return []

    def website(self) -> str:
        """Returns site name as link."""
        return "Pracuj.pl"

    @missing_container_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        container = {"data-test": "link-offer"}
        url_a = self.html.find("a", container)
        if url_a:
            return url_a.get("href")

    @missing_container_handler
    def job_title(self) -> str:
        """Extracts job title."""
        container = {"data-test": "offer-title"}
        return self.html.find("h2", container).text.strip()

    @missing_container_handler
    def tags(self):
        """Extracts job tags from record."""
        container = {"data-test": "technologies-item"}
        tags_block = self.html.find_all("span", container)
        tags_list = [tag.text.strip() for tag in tags_block]
        if tags_list:
            return TAG_SEPARATOR.join(tags_list)

    @missing_container_handler
    def company(self):
        """Extract company name from record."""
        return self.html.find("h3", {"data-test": "text-company-name"}).text.strip()

    @missing_container_handler
    def logo(self):
        """Extract company logo from record."""
        logo = self.html.find("img", {"data-test": "image-responsive"})
        return logo["src"] if logo else None

    @missing_container_handler
    def location(self):
        """Extract location from record."""
        loc = self.html.find("h4", {"data-test": "text-region"})

        if not loc:
            return None

        location = loc.text
        return remove_remote_status(location)

    @missing_container_handler
    def remote_status(self):
        """Extract remote status from record."""
        tag_name = "offer-additional-info"

        def additional_info_container(tag):
            return tag.has_attr("data-test") and tag["data-test"].startswith(tag_name)

        additional_info = self.html.find_all(additional_info_container)
        status = additional_info[-1].text
        return process_remote_status(status)

    @missing_container_handler
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

    def scrape(self):
        """Scrape given link using Selenium."""
        request = httpx.get(self.search_link)

        soup = BeautifulSoup(request.text, "html.parser")
        search_block = soup.find("div", {"data-test": "section-offers"})
        return str(search_block) if search_block else no_offers_found(self.website, self.search_link)
