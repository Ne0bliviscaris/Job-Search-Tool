import pytest
from bs4 import BeautifulSoup

from modules.updater.sites.websites.PracujPL import PracujPL
from modules.updater.webdriver import setup_webdriver

empty_listing = "https://it.pracuj.pl/praca?et=1&sal=50000"
job_listing = "https://it.pracuj.pl/praca"


def test_search_container():
    """Test the search functionality of Pracuj.pl."""
    # Initialize the PracujPL class with an empty search link
    with setup_webdriver() as web_driver:
        site = PracujPL(search_link=job_listing)
        search_container = site.scrape(web_driver)
        assert search_container is not None, "Search container is None"


def test_scrape_empty_container():
    """Test the search functionality of Pracuj.pl."""
    # Initialize the PracujPL class with an empty search link
    with setup_webdriver() as web_driver:
        site = PracujPL(search_link=empty_listing)
        empty_search_container = site.scrape(web_driver)
        soup_empty_search = BeautifulSoup(empty_search_container, "html.parser")
        assert len(soup_empty_search) == 0, "Empty search container is not empty"


def test_records_list():
    """Test job records extraction from HTML."""
    with setup_webdriver() as web_driver:

        site = PracujPL(search_link=job_listing)
        search_container = site.scrape(web_driver)
        soup = BeautifulSoup(search_container, "html.parser")
        records = site.records_list(data=soup)
        assert len(records) > 0, "No records found in the search container"


def test_empty_records_list():
    """Test the records list extraction."""
    with setup_webdriver() as web_driver:
        site = PracujPL(search_link=empty_listing)
        search_container = site.scrape(web_driver)
        records = site.records_list(data=search_container)
        assert records is None or len(records) == 0, "Records found in empty search container"
