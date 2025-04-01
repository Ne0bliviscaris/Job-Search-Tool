import pytest
from bs4 import BeautifulSoup

from modules.updater.scraper.selenium_utils import setup_webdriver
from modules.updater.sites.websites.JustJoinIT import JustJoinIT

empty_listing = "https://rocketjobs.pl/oferty-pracy/wszystkie-lokalizacje?doswiadczenie=staz-junior&tryb-pracy=praca-w-pelni-zdalna&zarobki=50000,500000&orderBy=DESC&sortBy=published"
job_listing = "https://rocketjobs.pl/oferty-pracy/wszystkie-lokalizacje/bi-data?orderBy=DESC&sortBy=published"


@pytest.fixture(scope="module")
def shared_driver():
    """Create a single webdriver instance for all tests."""
    with setup_webdriver() as driver:
        yield driver


def test_search_container(shared_driver):
    """Test search results retrieval."""
    site = JustJoinIT(search_link=job_listing)
    search_container = site.scrape(shared_driver)
    assert search_container is not None


def test_scrape_empty_container(shared_driver):
    """Test empty search results handling for RocketJobs."""
    site = JustJoinIT(search_link=empty_listing)
    empty_search_container = site.scrape(shared_driver)
    soup = BeautifulSoup(empty_search_container, "html.parser")
    assert len(empty_search_container) == 0, "Empty search container is not empty"


def test_records_list(shared_driver):
    """Test the records list extraction."""
    site = JustJoinIT(search_link=job_listing)
    search_container = site.scrape(shared_driver)
    soup = BeautifulSoup(search_container, "html.parser")
    records = site.records_list(html=soup)
    assert len(records) > 0


def test_empty_records_list(shared_driver):
    """Test the records list extraction."""
    site = JustJoinIT(search_link=empty_listing)
    search_container = site.scrape(shared_driver)
    soup = BeautifulSoup(search_container, "html.parser")
    records = site.records_list(html=soup)
    assert records is None or len(records) == 0, "Records found in empty search container"
