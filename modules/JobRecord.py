import hashlib
import re

import modules.containers as containers


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
            f"Website: {self.host_site}"
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
            # Get the salary text from the salary tag
            salary_text = salary if isinstance(salary, str) else salary.get_text(strip=True)

            # Convert to lower case and remove PLN, "zł", and anything inside parentheses like "(B2B)"
            processed_salary = re.sub(r"\(.*?\)", "", salary_text.lower())
            processed_salary = re.sub(r"(usd.*|pln.*|eur.*|zł.*)", "", processed_salary)
            processed_salary = (
                processed_salary.replace("–", "-")
                .replace("\xa0", "")
                .replace(",", "")
                .replace("Znamy widełki", "")
                .strip()
            )

            # Cut off the salary range from the string
            last_two_chars = processed_salary[-2:]
            index = salary_text.lower().rfind(last_two_chars)
            salary_details = salary_text[index + 2 :].strip() if index != -1 else None
            # Handle Bulldogjobs case
            if salary_text == "Znamy widełki":
                salary_details = salary_text

            # Convert 'k' notation (e.g., 4.5k, 5k) to full numbers
            processed_salary = re.sub(
                r"(\d+(\.\d+)?)k", lambda x: str(int(float(x.group(1)) * 1000)), processed_salary
            )

            # Remove any non-digit or non-range characters
            processed_salary = "".join(filter(lambda x: x.isdigit() or x == "-", processed_salary))

            try:
                # Split salary text into min and max salary if range is provided
                salary_parts = processed_salary.split("-")
                if len(salary_parts) >= 2:
                    # Use first 2 parts as min and max salary
                    min_salary = int(salary_parts[0].strip())
                    max_salary = int(salary_parts[1].strip())
                else:
                    min_salary = max_salary = int(processed_salary.strip())

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
            "website": self.host_site,
            "tags": self.tags,
            "url": self.url,
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
        if not self.location:
            return "Remote"

        status = containers.remote_status(self.html, self.website)
        return status if status else None
