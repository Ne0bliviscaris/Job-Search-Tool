import requests
import search_links
from bs4 import BeautifulSoup


def index_nofluffjobs(block_class):
    """
    Index offers from nofluffjobs.com and return them to file
    """
    response = requests.get(search_links.nofluffjobs)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find  <nfj-postings-list> block
    job_listing = soup.find("nfj-postings-list")

    jobs_index = [
        job.text
        for job in job_listing.find_all(class_=lambda class_name: class_name and class_name.startswith(block_class))
    ]
    return jobs_index


listing = index_nofluffjobs("posting-list-item")[0]
print(f"{listing}\n\n")
