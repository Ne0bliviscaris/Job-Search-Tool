import modules.updater.scraper.containers as containers
from modules.updater.data_processing.helper_functions import (
    convert_k_notation,
    ensure_string,
    extract_salary_details,
    get_salary_range,
    salary_cleanup,
    split_salary,
)


class JobRecord:
    def __init__(self, html, website):
        self.html = html
        self.website = website
        self.url = self.fetch_url()
        self.title = self.fetch_job_title()
        self.tags = self.fetch_job_tags()
        self.company_name = self.fetch_company_name()
        self.logo = self.fetch_logo()
        self.location = self.fetch_location()
        self.remote_status = self.fetch_remote_status()
        self.salary_min, self.salary_max, self.salary_details, self.salary_text = self.fetch_salary_range()
        self.host_site = self.host_site()
        # self.added_date = self.current_date()

    def __repr__(self):
        return (
            f"JobRecord:\n"
            f"Title: {self.title}\n"
            f"Url: {self.url}\n"
            f"Tags: {self.tags}\n"
            f"Company name: {self.company_name}\n"
            f"Logo: {self.logo}\n"
            f"Location: {self.location}\n"
            f"Remote status: {self.remote_status}\n"
            f"Min salary: {self.salary_min}\n"
            f"Max salary: {self.salary_max}\n"
            f"Salary details: {self.salary_details}\n"
            f"Salary text: {self.salary_text}\n"
            f"Website: {self.host_site}\n"
        )

    def fetch_job_title(self) -> str:
        """
        Fetch job title from the record
        """
        job_title = containers.job_title(self.html, self.website)
        return job_title if job_title else None

    def fetch_job_tags(self) -> list[str]:
        """
        Fetch job tags from the record
        """
        tags = containers.tags(self.html, self.website)
        return tags if tags else None

    def fetch_url(self):
        """
        Fetch job record url
        """
        url = containers.url(self.html, self.website)
        return url if url else None

    def fetch_company_name(self):
        """
        Fetch company name from the record
        """
        company = containers.company(self.html, self.website)
        return company if company else None

    def fetch_logo(self):
        logo = containers.logo(self.html, self.website)
        return logo if logo else None

    def fetch_location(self):
        location = containers.location(self.html, self.website)
        return location if location else None

    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """
        Fetch salary range and additional salary details from the job listing HTML.
        """
        salary = containers.salary(self.html, self.website)

        if salary:
            salary_text = ensure_string(salary)
            cleaned_salary = salary_cleanup(salary_text)
            salary_details = extract_salary_details(cleaned_salary, salary_text)
            converted_salary = convert_k_notation(cleaned_salary)
            processed_salary = get_salary_range(converted_salary)

            try:
                min_salary, max_salary = split_salary(processed_salary)
                return min_salary, max_salary, salary_details, salary_text

            except ValueError:
                return None, None, salary_details, salary_text

        return None, None, None, None

    def html(self):
        return self.html

    def prepare_dataframe(self):
        record = {
            "title": self.title,
            "logo": self.logo,
            "company_name": self.company_name,
            "location": self.location,
            "remote_status": self.remote_status,
            "min_salary": self.salary_min,
            "max_salary": self.salary_max,
            "salary_details": self.salary_details,
            "salary_text": self.salary_text,
            "tags": self.tags,
            "url": self.url,
            "website": self.host_site,
        }

        return record

    def host_site(self) -> str:
        """
        Extract the main domain from the website URL.
        """
        return self.website.split("//")[-1]

    def fetch_remote_status(self) -> str:
        """
        Check if the job listing is remote.
        """
        status = containers.remote_status(self.html, self.website)
        return status if status else None
