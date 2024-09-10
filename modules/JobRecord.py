import re

import containers as containers


class JobRecord:
    def __init__(self, html, website):
        self.html = html
        self.website = website
        self.title = self.fetch_job_title()
        self.url = self.fetch_url()
        self.tags = self.fetch_job_tags()
        self.company_name = self.fetch_company_name()
        self.logo = self.fetch_logo()
        self.location = self.fetch_location()
        self.salary_min, self.salary_max, self.salary_text = self.fetch_salary_range()
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
            f"Min salary: {self.salary_min}\n"
            f"Max salary: {self.salary_max}\n"
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
        return tags if tags else []

    def fetch_url(self):
        """
        Fetch job record url
        """
        url = self.html.get("href")
        return self.website + url if url else None

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

    def fetch_salary_range(self) -> tuple[int, int, str]:
        """
        Fetch salary range from the job listing HTML.
        """
        salary = containers.salary(self.html, self.website)

        if salary:
            salary_text = salary.get_text(strip=True)
            # Remove PLN, "zł" and anything inside parentheses like "(B2B)"
            processed_salary = (
                salary_text.replace("PLN", "")
                .replace("–", "-")
                .replace("\xa0", "")
                .replace(",", "")
                .replace("zł", "")
                .strip()
            )
            # Remove anything in parentheses (e.g., "(B2B)")
            processed_salary = re.sub(r"\(.*?\)", "", processed_salary)

            # Regular expression to handle 'k' notation (e.g., 4.5k, 5k)
            def convert_k_notation(salary_text):
                return re.sub(r"(\d+(\.\d+)?)k", lambda x: str(int(float(x.group(1)) * 1000)), salary_text)

            # Apply 'k' notation conversion
            processed_salary = convert_k_notation(processed_salary)

            # Remove any non-digit or non-range characters
            processed_salary = "".join(filter(lambda x: x.isdigit() or x == "-", processed_salary))

            # Split salary text into min and max salary if range is provided
            if "-" in processed_salary:
                min_salary_text, max_salary_text = processed_salary.split("-")
                min_salary = int(min_salary_text.strip())
                max_salary = int(max_salary_text.strip())
            else:
                min_salary = max_salary = int(processed_salary.strip())

            return min_salary, max_salary, salary_text

        return None, None, None

    def html(self):
        return self.html

    def prepare_dataframe(self):
        record = {
            "Title": self.title,
            "Url": self.url,
            "Company name": self.company_name,
            "Logo": self.logo,
            "Location": ", ".join(self.location),
            "Min salary": self.salary_min,
            "Max salary": self.salary_max,
            "Salary text": self.salary_text,
            "Website": self.host_site,
        }

        # Dodajemy tagi jako osobne kolumny
        for i, tag in enumerate(self.tags):
            record[f"Tag {i+1}"] = tag.strip()

        return record

    def host_site(self) -> str:
        """
        Extract the main domain from the website URL.
        """
        return self.website.split("//")[-1].split(".")[0]
