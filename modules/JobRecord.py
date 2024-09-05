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

    def fetch_job_title(self):
        """
        Fetch job title from the record
        """
        title_container = containers.job_title(self.website)
        job_title = [job.text for job in self.html.find(attrs=title_container)]
        return job_title[0] if job_title else None

    def fetch_job_tags(self):
        """
        Fetch job tags from the record
        """
        tags_container = containers.tags(self.website)
        job_tags = [job.text for job in self.html.find_all(attrs=tags_container)]
        return job_tags

    def fetch_url(self):
        """
        Fetch job record url
        """
        url = self.html["href"]
        if url:
            return self.website + url
        return None

    def fetch_company_name(self):
        """
        Fetch company name from the record
        """
        company_container = containers.company(self.website)
        company_name = self.html.find(attrs=company_container).text.strip()
        return company_name

    def fetch_logo(self):
        logo_container = containers.logo(self.website)
        logo = self.html.find(attrs=logo_container)
        return logo.get("src") if logo else None

        return None

    def fetch_location(self):
        location_container = containers.location(self.website)
        job_location_elements = self.html.find_all(attrs=location_container)
        job_location = [job.text.strip() for job in job_location_elements]
        return job_location

    import re

    def fetch_salary_range(self) -> tuple[int, int, str]:
        """
        Fetch salary range from the job listing HTML.
        """
        salary_container = containers.salary(self.website)
        salary_elements = self.html.find_all(attrs=salary_container)

        if salary_elements:
            raw_salary_text = salary_elements[0].get_text(strip=True)
            # Remove PLN, "zł" and anything inside parentheses like "(B2B)"
            processed_salary_text = (
                raw_salary_text.replace("PLN", "")
                .replace("–", "-")
                .replace("\xa0", "")
                .replace(",", "")
                .replace("zł", "")
                .strip()
            )
            # Remove anything in parentheses (e.g., "(B2B)")
            processed_salary_text = re.sub(r"\(.*?\)", "", processed_salary_text)

            # Regular expression to handle 'k' notation (e.g., 4.5k, 5k)
            def convert_k_notation(salary_text):
                return re.sub(r"(\d+(\.\d+)?)k", lambda x: str(int(float(x.group(1)) * 1000)), salary_text)

            # Apply 'k' notation conversion
            processed_salary_text = convert_k_notation(processed_salary_text)

            # Remove any non-digit or non-range characters
            processed_salary_text = "".join(filter(lambda x: x.isdigit() or x == "-", processed_salary_text))

            # Split salary text into min and max salary if range is provided
            if "-" in processed_salary_text:
                min_salary_text, max_salary_text = processed_salary_text.split("-")
                min_salary = int(min_salary_text.strip())
                max_salary = int(max_salary_text.strip())
            else:
                min_salary = max_salary = int(processed_salary_text.strip())

            return min_salary, max_salary, raw_salary_text

        return None, None, None

    def html(self):
        return self.html

    def record_to_dataframe(self):
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
