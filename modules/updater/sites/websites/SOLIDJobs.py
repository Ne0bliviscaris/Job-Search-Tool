import urllib.parse

import httpx

from modules.updater.data_processing.helper_functions import (
    convert_k_notation,
    ensure_string,
    extract_salary_details,
    get_salary_range,
    process_remote_status,
    salary_cleanup,
    split_salary,
)
from modules.updater.data_processing.site_files import load_json, save_json
from modules.updater.error_handler import no_offers_found, scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class Solidjobs(JobSite):
    """Class to scrape Solidjobs website."""

    @staticmethod
    def file_extension():
        return "json"

    def save_file(self, filename, html):
        """Save HTML content to a file."""
        save_json(filename, html)

    def load_file(self, filename):
        """Load HTML content from a file."""
        return load_json(filename)

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        ...

    @staticmethod
    def records_list(data) -> list:
        """Extracts job records from HTML."""
        if not data:
            return []
        return data

    def website(self) -> str:
        """Returns site name as link."""
        return "solid.jobs"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        return f"https://{self.website}/offer/{self.html['id']}/{self.html['jobOfferUrl']}"

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        return self.html["jobTitle"]

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        skills = self.html.get("requiredSkills", [])
        tags_list = [skill.get("name") for skill in skills if skill.get("name")]
        return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        return self.html["companyName"]

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        return self.html.get("companyLogoUrl")

    @scraping_error_handler
    def location(self):
        """Extract location from job record."""
        return self.html.get("companyCity")

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from job record."""
        status = self.html.get("remotePossible")
        return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        salary = self.html.get("salaryRange", {})
        if not salary:
            return None
        lower = int(salary.get("lowerBound"))
        upper = int(salary.get("upperBound"))
        currency = salary.get("currency", "PLN")
        return f"{lower} - {upper} {currency}"

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

    def scrape(self, webdriver=None):
        """Scrape given link using Selenium."""
        all_offers = self._fetch_offers_json()
        if not all_offers or len(all_offers) == 0:
            return no_offers_found(self.website, self.search_link)

        params = self._parse_url_params(self.search_link)
        filtered_offers = self._filter_offers(all_offers, params)

        return filtered_offers

    def _parse_url_params(self, url):
        """Parse filter parameters from URL."""
        params = {}
        parts = url.split(";")
        for part in parts:
            if "=" in part:
                key, value = part.split("=", 1)
                decoded_value = urllib.parse.unquote(value)
                if key == "cities" and "Trójmiasto" in decoded_value:
                    decoded_value = decoded_value.replace("Trójmiasto", "Gdańsk,Gdynia,Sopot")
                params[key] = decoded_value
        return params

    def _filter_offers(self, offers, params):
        """Filter job offers by URL parameters."""
        filtered = []
        for offer in offers:
            if "cities" in params:
                city_list = params["cities"].split(",")
                remote_values = ["W całości", "Możliwa w całości"]
                is_remote = offer.get("remotePossible") in remote_values
                city = offer.get("companyCity") in city_list
                is_fully_remote = "Praca zdalna" in city_list and is_remote
                if not (is_fully_remote or city):
                    continue
            if "categories" in params and offer.get("mainCategory") != params["categories"]:
                continue
            if "subcategories" in params and offer.get("subCategory") != params["subcategories"]:
                continue
            if "experiences" in params:
                exp_list = params["experiences"].split(",")
                if offer.get("experienceLevel") not in exp_list:
                    continue
            if "minimumSalary" in params:
                salary = offer.get("salaryRange", {})
                if salary and salary.get("upperBound", 0) < float(params["minimumSalary"]):
                    continue
            filtered.append(offer)
        return filtered

    def _fetch_offers_json(self):
        """Fetch job offers from Solidjobs API as JSON."""
        url = "https://solid.jobs/api/offers?division=it&sortOrder=default"
        headers = {
            "Accept": "application/vnd.solidjobs.jobofferlist+json, application/json, text/plain, */*",
        }
        response = httpx.get(url, headers=headers)
        return response.json()
