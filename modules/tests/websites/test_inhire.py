from bs4 import BeautifulSoup

from modules.updater.sites.websites.InhireIO import InhireIO
from modules.updater.updater import update_site
from modules.updater.webdriver import setup_webdriver

empty_listing = "https://inhire.io/oferty-pracy?experiences=0_1&locations=1&roles=it,blockchain_engineer&salary=75000&technologies=413"
job_listing = "https://inhire.io/?roles=it"


def test_search_container():
    """Test the search functionality of Pracuj.pl."""
    # Initialize the PracujPL class with an empty search link

    site = InhireIO(search_link=job_listing)
    search_container = site.scrape()
    assert search_container is not None, "Search container is None"
    assert len(search_container) > 0, "Search container is empty"


def test_scrape_empty_container():
    """Test empty search results handling for RocketJobs."""
    site = InhireIO(search_link=empty_listing)
    empty_search_container = site.scrape()
    assert len(empty_search_container) == 0, "Empty search container is not empty"
