from modules.updater.sites.websites.RocketJobs import RocketJobs


class JustJoinIT(RocketJobs):
    """Class to scrape JustJoinIT website.
    Identical structure as RocketJobs"""

    def website(self) -> str:
        """Returns site name as link."""
        return "JustJoin.it"
