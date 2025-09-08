from modules.updater.sites.JobSite import JobSite
from modules.updater.sites.websites.Bulldogjob import Bulldogjob
from modules.updater.sites.websites.InhireIO import InhireIO
from modules.updater.sites.websites.JustJoinIT import JustJoinIT
from modules.updater.sites.websites.NoFluffJobs import NoFluffJobs
from modules.updater.sites.websites.PracujPL import PracujPL
from modules.updater.sites.websites.RocketJobs import RocketJobs
from modules.updater.sites.websites.SOLIDJobs import Solidjobs
from modules.updater.sites.websites.Theprotocol import Theprotocol

scrapers = {
    "https://nofluffjobs.com": NoFluffJobs,
    "https://bulldogjob.pl": Bulldogjob,
    "https://inhire.io": InhireIO,
    "https://it.pracuj.pl": PracujPL,
    "https://theprotocol.it": Theprotocol,
    "https://rocketjobs.pl": RocketJobs,
    "https://justjoin.it": JustJoinIT,
    "https://solid.jobs": Solidjobs,
}


def scraper_factory(search_link) -> JobSite:
    """Creates site instance based on search link."""
    for url, scraper in scrapers.items():
        if url in search_link:
            # print(
            #     f"{scraper_factory.__name__}: Using scraper: {scraper.__name__} for URL: {search_link}"  # noqa
            # )
            return scraper(search_link=search_link)
    # print(f"{scraper_factory.__name__}: Error: Website not recognized")
    return "Error: Website not recognized"
