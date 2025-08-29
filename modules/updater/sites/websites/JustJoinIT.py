from modules.updater.data_processing.helper_functions import process_remote_status
from modules.updater.error_handler import scraping_error_handler
from modules.updater.sites.JobSite import TAG_SEPARATOR
from modules.updater.sites.websites.RocketJobs import RocketJobs


class JustJoinIT(RocketJobs):
    """Class to scrape JustJoinIT website.
    Identical structure as RocketJobs"""

    def website(self) -> str:
        """Returns site name as link."""
        return "JustJoin.it"

    @scraping_error_handler
    def remote_status(self):
        """Extract remote status from job record."""
        remote_icon = self.html.find("svg", {"data-testid": "ShareLocationRoundedIcon"})
        if remote_icon:
            status = "Remote"
            return process_remote_status(status)
        return process_remote_status(False)

    @scraping_error_handler
    def salary_container(self):
        """Extract salary container from record."""
        salary_block = self.html.h6
        if salary_block:
            salary = salary_block.text
            return salary

    @scraping_error_handler
    def tags(self):
        """Extracts job tags from record."""
        # Starting from company SVG icon
        company_icon = self.html.find("svg", {"data-testid": "ApartmentRoundedIcon"})
        company_location_bar = company_icon.parent.parent
        # Tags bar contains tags and posting remaining duration
        tags_bar = company_location_bar.find_next_sibling("div")
        posting_remaining_duration = tags_bar.div.decompose()
        tags = tags_bar.find_all("div")
        tags_list = [tag.text for tag in tags]
        if tags_list:
            return TAG_SEPARATOR.join(tags_list)
