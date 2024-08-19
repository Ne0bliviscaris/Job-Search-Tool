import crawlers
import requests
import search_links
from bs4 import BeautifulSoup

# def extract_nofluffjobs():
#     """
#     Index offers from nofluffjobs.com and return them to file
#     """
#     response = requests.get(search_links.nofluffjobs)
#     soup = BeautifulSoup(response.content, "html.parser")

#     # Znajdź wszystkie bloki <nfj-postings-list>
#     postings_lists = soup.find_all("nfj-postings-list")

#     if postings_lists:
#         main_search_results = postings_lists[0]
#         job_titles = [
#             job.text
#             for job in main_search_results.find_all(
#                 class_=lambda class_name: class_name and class_name.startswith("posting-list-item")
#             )
#         ]
#         print("\n\nJobs found:")
#         for job in job_titles:
#             print(f"{job}\n")

nfj = crawlers.index_nofluffjobs()
print(nfj[0])
