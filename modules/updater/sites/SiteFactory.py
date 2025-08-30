from modules.updater.sites.JobSite import JobSite
from modules.updater.sites.websites.Bulldogjob import Bulldogjob
from modules.updater.sites.websites.InhireIO import InhireIO
from modules.updater.sites.websites.JustJoinIT import JustJoinIT
from modules.updater.sites.websites.NoFluffJobs import NoFluffJobs
from modules.updater.sites.websites.PracujPL import PracujPL
from modules.updater.sites.websites.RocketJobs import RocketJobs
from modules.updater.sites.websites.SOLIDJobs import Solidjobs
from modules.updater.sites.websites.Theprotocol import Theprotocol


class SiteFactory:
    """A factory class for creating site instances."""

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

    @staticmethod
    def identify_website(search_link) -> JobSite:
        """Creates site instance based on search link."""
        for url, site_class in SiteFactory.scrapers.items():
            if url in search_link:
                return site_class(search_link=search_link)
        return "Error: Website not recognized"
