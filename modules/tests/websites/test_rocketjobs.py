from bs4 import BeautifulSoup

from modules.updater.sites.websites.RocketJobs import RocketJobs
from modules.updater.webdriver import setup_webdriver

empty_listing = "https://rocketjobs.pl/oferty-pracy/wszystkie-lokalizacje?doswiadczenie=staz-junior&tryb-pracy=praca-w-pelni-zdalna&zarobki=50000,500000&orderBy=DESC&sortBy=published"
job_listing = "https://rocketjobs.pl/oferty-pracy/wszystkie-lokalizacje/bi-data?orderBy=DESC&sortBy=published"


def test_search_container():
    """Test the search functionality of Pracuj.pl."""
    # Initialize the PracujPL class with an empty search link
    with setup_webdriver() as web_driver:
        site = RocketJobs(search_link=job_listing)
        search_container = site.scrape(web_driver)
        assert search_container is not None, "Search container is None"


def test_scrape_empty_container():
    """Test empty search results handling for RocketJobs."""
    with setup_webdriver() as web_driver:
        site = RocketJobs(search_link=empty_listing)
        empty_search_container = site.scrape(web_driver)
        soup_empty_search = BeautifulSoup(empty_search_container, "html.parser")
        assert len(soup_empty_search) == 0, "Empty search container is not empty"


def test_records_list():
    """Test the records list extraction."""
    with setup_webdriver() as web_driver:
        site = RocketJobs(search_link=job_listing)
        search_container = site.scrape(web_driver)
        soup = BeautifulSoup(search_container, "html.parser")
        records = site.records_list(data=soup)
        assert len(records) > 0


def test_empty_records_list():
    """Test the records list extraction."""
    with setup_webdriver() as web_driver:
        site = RocketJobs(search_link=empty_listing)
        search_container = site.scrape(web_driver)
        soup = BeautifulSoup(search_container, "html.parser")
        records = site.records_list(data=soup)
        assert records is None or len(records) == 0, "Records found in empty search container"
