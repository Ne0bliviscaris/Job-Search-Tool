import modules.containers as containers


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
        self.salary_min, self.salary_max = self.fetch_salary_range()

    def __repr__(self):
        return (
            f"JobRecord:\n"
            f"Title: {self.title}\n"
            f"Url: {self.url}\n"
            f"Tags: {self.tags}\n"
            f"Company name: {self.company_name},\n"
            f"Logo: {self.logo}\n"
            f"Location: {self.location}\n"
            f"Min salary: {self.salary_min})\n"
            f"Max salary: {self.salary_max}"
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
        company_name = self.html.find(company_container).text.strip()
        return company_name

    def fetch_logo(self):
        logo_container = containers.logo(self.website)
        logo = self.html.find(logo_container)
        return logo

        return None

    def fetch_location(self):
        location_container = containers.location(self.website)
        job_location_elements = self.html.find_all(attrs=location_container)
        job_location = [job.text.strip() for job in job_location_elements]
        return job_location

    def fetch_salary_range(self):
        salary_container = containers.salary(self.website)
        salary_elements = self.html.find_all(attrs=salary_container)

        # Strip salary text from unwanted characters
        if salary_elements:
            salary_text = salary_elements[0].get_text(strip=True)
            salary_text = salary_text.replace("PLN", "").replace("–", "-").replace("\xa0", "").replace(",", "").strip()
            # Split salary text into min and max salary if range is provided
            if "-" in salary_text:
                min_salary_text, max_salary_text = salary_text.split("-")
                min_salary = int(min_salary_text.strip())
                max_salary = int(max_salary_text.strip())
            else:
                min_salary = max_salary = int(salary_text.strip())

            return min_salary, max_salary
        return None, None

    def html(self):
        return self.html

    def to_dataframe_record(self):
        record = {
            "Title": self.title,
            "Url": self.url,
            "Company name": self.company_name,
            "Logo": self.logo,
            "Location": ", ".join(self.location),
            "Min salary": self.salary_min,
            "Max salary": self.salary_max,
        }

        # Dodajemy tagi jako osobne kolumny
        for i, tag in enumerate(self.tags):
            record[f"Tag {i+1}"] = tag.strip()

        return record
