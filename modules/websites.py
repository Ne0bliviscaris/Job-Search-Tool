NOFLUFFJOBS = "nofluffjobs"
JUSTJOIN = "justjoin"
THEPROTOCOL = "theprotocol"
ROCKETJOBS = "rocketjobs"

current_website = None

search_links = [
    "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior"
]


def identify_website(search_link):
    """
    Set current website as global variable based on search link
    """
    # print(f"Link received: {search_link}")
    global current_website
    if "nofluffjobs.com" in search_link:
        current_website = NOFLUFFJOBS
    elif "justjoin.it" in search_link:
        current_website = JUSTJOIN
    elif "theprotocol.it" in search_link:
        current_website = THEPROTOCOL
    elif "rocketjobs.pl" in search_link:
        current_website = ROCKETJOBS
    else:
        current_website = "Error: Website not recognized"
    # print(f"Current website: {current_website}")
    return current_website


# def set_site_parameters(site, job):

#     # NoFluffJobs
#     if site == "nofluffjobs":
#         search_container = "nfj-postings-list"
#         job_name = job.find(attrs={"data-cy": "title position on the job offer listing"}).text
#         job_tags = [tag.text for tag in job.find_all(attrs={"data-cy": "category name on the job offer listing"})]
#         salary_elements = job.find(attrs={"data-cy": "salary ranges on the job offer listing"})
#         job_location = [
#             loc.text.strip() for loc in job.find_all(attrs={"data-cy": "location on the job offer listing"})
#         ]
#         job_url = "https://nofluffjobs.com" + job["href"]
#         company_name = job.find("h4").text.strip()
#     return search_container, job_name, job_tags, salary_elements, job_location, job_url, company_name
