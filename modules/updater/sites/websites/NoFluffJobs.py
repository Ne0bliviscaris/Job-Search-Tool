from modules.updater.data_processing.helper_functions import (
    convert_k_notation,
    ensure_string,
    extract_salary_details,
    get_salary_range,
    process_remote_status,
    salary_cleanup,
    split_salary,
)
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class NoFluffJobs(JobSite):
    """Class to scrape website."""

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        return '[class="list-container"]'

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
        """Returns site name as link."""
        return "NoFluffJobs.com"

    def url(self) -> str:
        """Extracts URL from job record."""
        try:
            url = self.html.get("href")
            if url:
                return url if url.startswith("http") else f"https://nofluffjobs.com{url}"
        except:
            print(f"Error fetching data from record: {self.website} -> URL")

    def job_title(self) -> str:
        """Extracts job title."""
        try:
            container = {"data-cy": "title position on the job offer listing"}
            title = self.html.find(attrs=container)
            return title.text.strip() if title else None
        except:
            print(f"Error fetching data from record: {self.website} -> Job Title")

    def tags(self):
        """Extracts job tags from record."""
        try:
            tags_container = {"data-cy": "category name on the job offer listing"}
            tags = self.html.find_all(attrs=tags_container)
            tags_list = [tag.text for tag in tags]
            if tags_list:
                return TAG_SEPARATOR.join(tags_list)
        except:
            print(f"Error fetching data from record: {self.website} -> Tags")

    def company(self):
        """Extract company name from record."""
        try:
            name = lambda x: x and x.startswith("company-name")
            company_container = {"class": name}
            return self.html.find(attrs=company_container).text
        except:
            print(f"Error fetching data from record: {self.website} -> Company")

    def logo(self):
        """Extract company logo from record."""
        try:
            img = self.html.find("img")
            if img:
                logo_container = {"alt": "Company logo"}
                if logo_container:
                    logo = self.html.find(attrs=logo_container)
                    return logo["src"]
        except:
            print(f"Error fetching data from record: {self.website} -> Logo")

    def location(self):
        location_container = {"data-cy": "location on the job offer listing"}
        location_block = self.html.find(attrs=location_container)
        if location_block:
            location_span = location_block.span
        try:
            return location_span.text.strip()
        except:
            print(f"Error fetching data from record: {self.website} -> Location")

    def remote_status(self):
        try:
            location_container = {"data-cy": "location on the job offer listing"}
            location = self.html.find(attrs=location_container)
            if location:
                return process_remote_status(location.text)
        except:
            print(f"Error fetching data from record: {self.website} -> Remote status")

    def salary_container(self):
        try:
            salary_container = {"data-cy": "salary ranges on the job offer listing"}
            return self.html.find(attrs=salary_container)
        except:
            print(f"Error fetching data from record: {self.website} -> Salary")

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """
        Fetch salary range and additional salary details from the job listing HTML.
        """
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

    @staticmethod
    def perform_additional_action(webdriver):
        """Performs additional actions needed for scraping the website."""
        return None

    @staticmethod
    def stop_scraping(webdriver):
        return nofluffjobs_no_search_results(webdriver)


def nofluffjobs_no_search_results(webdriver):
    """Check if results exist on No Fluff Jobs."""
    from selenium.webdriver.common.by import By

    empty_search = "nfj-no-offers-found-header"
    try:
        no_offers_block = webdriver.find_element(By.CSS_SELECTOR, empty_search)
        if no_offers_block:
            no_offers_text = no_offers_block.text
            if "Brak wyników wyszukiwania" in no_offers_text:
                print(f"No offers found for NoFluffJobs.com: {webdriver.current_url}")
                return True
    except Exception as e:
        pass
