import pytest
from bs4 import BeautifulSoup

from modules.updater.sites.websites.Bulldogjob import Bulldogjob

empty_listing = (
    "https://bulldogjob.pl/companies/jobs/s/skills,Python/experienceLevel,intern/salaryBrackets,50000,50000"
)
job_listing = "https://bulldogjob.pl/companies/jobs/s/skills,Python"


def test_search_container():
    """Test search results retrieval."""
    site = Bulldogjob(search_link=job_listing)
    search_container = site.scrape()
    assert search_container is not None


def test_scrape_empty_container():
    """Test empty search results handling for RocketJobs."""
    site = Bulldogjob(search_link=empty_listing)
    empty_search_container = site.scrape()
    soup_empty_search = BeautifulSoup(empty_search_container, "html.parser")
    assert len(soup_empty_search) == 0, "Empty search container is not empty"


def test_records_list():
    """Test job records extraction."""
    site = Bulldogjob(search_link=job_listing)
    search_container = site.scrape()
    records = site.records_list(data=search_container)
    assert len(records) > 0


def test_empty_records_list():
    """Test the records list extraction."""
    site = Bulldogjob(search_link=empty_listing)
    search_container = site.scrape()
    soup = BeautifulSoup(search_container, "html.parser")
    records = site.records_list(data=soup)
    assert records is None or len(records) == 0, "Records found in empty search container"
