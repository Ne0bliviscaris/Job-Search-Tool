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

    def website(self) -> str:
        """Returns site name as link."""
        return "Pracuj.pl"

    def url(self) -> str:
        """Extracts URL from job record."""
        try:
            container = {"data-test": "link-offer"}
            url_a = self.html.find("a", container)
            if url_a:
                return url_a.get("href")
        except:
            print(f"Error fetching data from record: {self.website} -> URL")

    def job_title(self) -> str:
        """Extracts job title."""
        try:
            container = {"data-test": "offer-title"}
            return self.html.find("h2", container).text.strip()
        except:
            print(f"Error fetching data from record: {self.website} -> Job Title")

    def tags(self):
        """Extracts job tags from record."""
        try:
            container = {"data-test": "technologies-item"}
            tags_block = self.html.find_all("span", container)
            tags_list = [tag.text.strip() for tag in tags_block]
            if tags_list:
                return TAG_SEPARATOR.join(tags_list)

        except:
            print(f"Error fetching data from record: {self.website} -> Tags")

    def company(self):
        """Extract company name from record."""
        try:
            return self.html.find("h3", {"data-test": "text-company-name"}).text.strip()
        except:
            print(f"Error fetching data from record: {self.website} -> Company")

    def logo(self):
        """Extract company logo from record."""
        try:
            return self.html.find("img", {"data-test": "image-responsive"})["src"]
        except:
            print(f"Error fetching data from record: {self.website} -> Logo")

    def location(self):
        try:
            loc = self.html.find("h4", {"data-test": "text-region"})
            if loc and loc.strong:
                location = loc.strong.text
                return remove_remote_status(location)
        except:
            print(f"Error fetching data from record: {self.website} -> Location")

    def remote_status(self):
        try:
            tag_name = "offer-additional-info"
            additional_info_containers = lambda tag: tag.has_attr("data-test") and tag["data-test"].startswith(
                tag_name
            )
            additional_info = self.html.find_all(additional_info_containers)
            status = additional_info[-1].text
            return process_remote_status(status)
        except:
            print(f"Error fetching data from record: {self.website} -> Remote status")

    def salary_container(self):
        try:
            salary_container = self.html.find("span", {"data-test": "offer-salary"})
            if salary_container:
                return salary_container.text.strip()
        except:
            print(f"Error fetching data from record: {self.website} -> Salary")

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

    @staticmethod
    def stop_scraping(webdriver):
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
