import requests
import search_links
from bs4 import BeautifulSoup


def nofluffjobs_search_results():
    """
    Index offers from nofluffjobs.com and return them to file
    """
    response = requests.get(search_links.nofluffjobs)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find block <nfj-postings-list>
    job_listing = soup.find("nfj-postings-list")

    return job_listing


# List of job offers
def split_records(job_listing):
    records_html = [
        job
        for job in job_listing.find_all(
            class_=lambda class_name: class_name and class_name.startswith("posting-list-item")
        )
    ]
    return records_html


def extract_job_url(records_html, index=0):
    urls = [job["href"] for job in records_html if job.has_attr("href")]
    if len(urls) == 1:
        return "https://nofluffjobs.com" + urls[0]
    return "https://nofluffjobs.com" + urls[index] if index < len(urls) else None


# List of job offer names - fetches 2 objects with same name and returns first one
def extract_job_name(records_html, index=0):
    job_title = [
        job.text for job in records_html[index].find_all(attrs={"data-cy": "title position on the job offer listing"})
    ]
    return job_title[0]


# List of job offer tags
def extract_job_tags(records_html, index=0):
    job_tags = [
        job.text for job in records_html[index].find_all(attrs={"data-cy": "category name on the job offer listing"})
    ]
    return job_tags


def extract_salary(records_html, index=0):
    salary_elements = records_html[index].find_all(attrs={"data-cy": "salary ranges on the job offer listing"})

    # Strip salary text from unwanted characters
    if salary_elements:
        salary_text = salary_elements[0].get_text(strip=True)
        salary_text = salary_text.replace("PLN", "").replace("–", "-").replace("\xa0", "").replace(",", "").strip()
        # Split salary text into min and max salary if range is provided
        if "-" in salary_text:
            min_salary_text, max_salary_text = salary_text.split("-")
            min_salary = int(min_salary_text.strip())
            max_salary = int(max_salary_text.strip())
        else:
            min_salary = max_salary = int(salary_text.strip())

        return min_salary, max_salary
    return None, None


def extract_job_location(records_html, index=0):
    job_location_elements = records_html[index].find_all(attrs={"data-cy": "location on the job offer listing"})
    job_location = [job.text.strip() for job in job_location_elements]
    return job_location


def extract_data_from_offer(index=0):
    job_listing = nofluffjobs_search_results()
    records = split_records(job_listing)

    job_name = extract_job_name(records, index)
    job_tags = extract_job_tags(records, index)
    job_salary = extract_salary(records, index)
    job_location = extract_job_location(records, index)
    job_url = extract_job_url(records, index)

    return job_name, job_tags, job_salary, job_location, job_url


# Przykład użycia
single_job_offer = extract_data_from_offer(0)
print(single_job_offer)
# print(extract_data_from_offers())
