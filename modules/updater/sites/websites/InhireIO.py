from urllib.parse import parse_qs, urlparse

import requests

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
from modules.updater.data_processing.site_files import (
    load_json,
    save_json,
    set_filename_from_link,
)
from modules.updater.error_handler import no_offers_found, scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR, JobSite


class InhireIO(JobSite):
    """Class to scrape website."""

    @staticmethod
    def file_extension():
        return "json"

    @staticmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        ...

    @staticmethod
    def records_list(data, link, test_mode=False) -> list:
        """Load records from JSON file."""
        if test_mode:
            return data
        return data

    def save_file(self, filename, records):
        """Export records to a file."""
        save_json(filename, records)

    def load_file(self, filename):
        """Load records from a file."""
        data = load_json(filename)
        return data

    def website(self) -> str:
        """Returns site name."""
        return "Inhire.io"

    @scraping_error_handler
    def url(self) -> str:
        """Extracts URL from job record."""
        main_url = self.html["offerAdditionalFields"].get("rp_url")
        if main_url:
            return f"https://inhire.io/praca/{main_url}"
        else:
            url = self.html["offerAdditionalFields"]["external_offer_url"]
            return f"{url}"

    @scraping_error_handler
    def job_title(self) -> str:
        """Extracts job title."""
        title = self.html["process_title"]
        return title or None

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        tags = self.html["skills"]
        tags_list = [tag.capitalize() for tag in tags.split(",") if tags]
        if tags_list:
            return TAG_SEPARATOR.join(tags_list)

    @scraping_error_handler
    def company(self):
        """Extract company name from record."""
        return self.html["company_name"] or None

    @scraping_error_handler
    def logo(self):
        """Extract company logo from record."""
        company_id = self.html["company_id"]
        img_src = f"https://inhire.io/img/companies/logos/{company_id}_logo.png"
        return img_src or None

    @scraping_error_handler
    def location(self):
        """Extract location from job record."""
        cities = self.html["cities"]
        location = cities.replace(",", TAG_SEPARATOR)
        return remove_remote_status(location)

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from job record."""
        status = None
        cities = self.html["cities"]
        hybrid_work = self.html["offerAdditionalFields"]["hybrid_work"]["hybrid_work"]
        if hybrid_work:
            status = "Hybrid"
            return process_remote_status(status)

        if "remote" in cities.lower():
            status = "Remote"
        elif self.html["offerAdditionalFields"]["is_remote_recruitment"]:
            status = "Remote"
        else:
            status = "On-site"

        return process_remote_status(status)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        if self.html["undisclosed_salary"]:
            return None
        default_salary = self.html["salary"]["permanent"]
        salary = self.html["salary"]
        if salary:
            if default_salary and default_salary != "hidden":
                return default_salary
            else:
                b2b_salary = salary["contract"]
                if b2b_salary and b2b_salary != "hidden":
                    return b2b_salary

        return None

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
        except ValueError as e:
            print(f"Error processing data from record: {self.website} -> Salary range - data: {salary_text}")
            return None, None, salary_details, salary_text

    def scrape(self, webdriver=None):
        """Scrape using API request."""
        all_offers = []
        page = 1
        while True:
            data = self._send_api_request(page)
            if not data or len(data) == 0:
                break

            all_offers.extend(data)
            page += 1

        return all_offers if all_offers else no_offers_found(self.website, self.search_link)

    def _send_api_request(self, page=1):
        """Scrape single page of results."""
        base_url = "https://inhire.io/getAllOffersNonAuth"
        payload = self._construct_API_request(link=self.search_link, page_number=page)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        response = requests.post(base_url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["response"]
        return []

    def _construct_API_request(self, link=None, page_number=1):
        if not link:
            return None

        parsed = urlparse(link)
        params = parse_qs(parsed.query)
        payload = {}

        if "company_sectors" in params:
            sector_values = params["company_sectors"][0].split(",")
            sector_ids = []
            for val in sector_values:
                if val.isdigit():
                    sector_ids.append(int(val))
            if sector_ids:
                payload["company_sector_ids"] = sector_ids

        if "company_sizes" in params:
            size_values = params["company_sizes"][0].split(",")
            size_ids = []
            for val in size_values:
                if val.isdigit():
                    size_ids.append(int(val))
            if size_ids:
                payload["company_size_ids"] = size_ids

        if "employment_types" in params:
            val = params["employment_types"][0].strip()
            if val:
                payload["contract_type"] = val

        if "experiences" in params:
            exp_values = params["experiences"][0].split(",")
            exp_list = []
            for val in exp_values:
                if val:
                    exp_list.append(val)
            if exp_list:
                payload["experience"] = exp_list

        if "locations" in params:
            loc_values = params["locations"][0].split(",")
            loc_ids = []
            for val in loc_values:
                if val.isdigit():
                    loc_ids.append(int(val))
            if loc_ids:
                payload["city_ids"] = loc_ids

        if "roles" in params:
            if params["roles"] == ["it"]:
                it_roles_full = [
                    "backend_developer",
                    "frontend_developer",
                    "full_stack_developer",
                    "mobile_developer",
                    "embedded_developer",
                    "machine_learning_engineer",
                    "big_data",
                    "data_science",
                    "ux_designer",
                    "security_engineer",
                    "telco",
                    "network_engineer",
                    "network_administrator",
                    "it_administration",
                    "database_administrator",
                    "database_developer",
                    "devops_engineer",
                    "architect",
                    "team_leader",
                    "project_manager",
                    "product_owner",
                    "sap",
                    "scrum_master",
                    "blockchain_engineer",
                    "etl_developer",
                    "bi",
                    "business_analyst",
                    "testing",
                    "helpdesk",
                    "game_developer",
                    "other",
                ]
                payload["it_roles"] = it_roles_full
            else:
                role_values = params["roles"][0].split(",")

                role_list = [val for val in role_values if val]
                if role_list:
                    payload["it_roles"] = role_list

        if "salary" in params:
            try:
                salary = int(params["salary"][0])
                payload["salary"] = salary
            except ValueError:
                pass

        if "technologies" in params:
            tech_values = params["technologies"][0].split(",")
            tech_ids = []
            for val in tech_values:
                if val.isdigit():
                    tech_ids.append(int(val))
            if tech_ids:
                payload["it_technology_ids"] = tech_ids

        payload["include_undisclosed"] = True
        payload["page"] = page_number
        return payload
