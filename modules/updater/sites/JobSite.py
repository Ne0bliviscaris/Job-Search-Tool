from abc import ABC, abstractmethod

TAG_SEPARATOR = " | "


class JobSite(ABC):
    """Base abstract class for job board sites."""

    def __init__(self, search_link=None, html=None):
        self.html = html
        self.search_link = search_link
        self.website = self.website()
        if html:
            self.url = self.url()
            self.title = self.job_title()
            self.tags = self.tags()
            self.company_name = self.company()
            self.logo = self.logo()
            self.location = self.location()
            self.remote_status = self.remote_status()
            self.salary_min, self.salary_max, self.salary_details, self.salary_text = self.fetch_salary_range()

    @staticmethod
    @abstractmethod
    def search_container() -> str:
        """Returns CSS selector for the container with job listings."""
        pass

    @staticmethod
    @abstractmethod
    def records_list(html) -> list:
        """Extracts job records from HTML."""
        pass

    @abstractmethod
    def website(self) -> str:
        """Returns site name as link."""
        pass

    @abstractmethod
    def url(self) -> str:
        """Extracts URL from job record."""
        pass

    @abstractmethod
    def job_title(self) -> str:
        """Extracts job title."""
        pass

    @abstractmethod
    def tags():
        """Extracts job tags from record."""
        pass

    @abstractmethod
    def company(self):
        """Extract company name from record."""
        pass

    @abstractmethod
    def logo(self):
        """Extract company logo from record."""
        pass

    @abstractmethod
    def location(self):
        """Extract job location from record."""
        pass

    @abstractmethod
    def remote_status(self):
        """Extract remote work status from record."""
        pass

    @abstractmethod
    def salary_container(self):
        """Extract salary container from record."""
        pass

    @abstractmethod
    def fetch_salary_range(self) -> tuple[int, int, str, str]:
        """Fetch salary range and details from job listing."""
        pass

    @staticmethod
    def stop_scraping(webdriver) -> str:
        """Returns stop condition for scraping."""
        pass

    @staticmethod
    def perform_additional_action(webdriver) -> str:
        """Returns additional actions for scraping."""
        pass

    def to_dict(self):
        return {
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
            "website": self.website,
        }
