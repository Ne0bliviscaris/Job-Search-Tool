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


def split_records():
    job_listing = nofluffjobs_search_results()
    records_html = [
        job
        for job in job_listing.find_all(
            class_=lambda class_name: class_name and class_name.startswith("posting-list-item")
        )
    ]
    return records_html


def extract_data_from_offer(records_html, index=0):
    job = records_html[index]

    job_name = job.find(attrs={"data-cy": "title position on the job offer listing"}).text
    job_tags = [tag.text for tag in job.find_all(attrs={"data-cy": "category name on the job offer listing"})]
    salary_elements = job.find(attrs={"data-cy": "salary ranges on the job offer listing"})
    job_location = [loc.text.strip() for loc in job.find_all(attrs={"data-cy": "location on the job offer listing"})]
    job_url = "https://nofluffjobs.com" + job["href"]
    company_name = job.find("h4").text.strip()

    if salary_elements:
        salary_text = (
            salary_elements.get_text(strip=True)
            .replace("PLN", "")
            .replace("–", "-")
            .replace("\xa0", "")
            .replace(",", "")
            .strip()
        )
        if "-" in salary_text:
            min_salary, max_salary = map(int, salary_text.split("-"))
        else:
            min_salary = max_salary = int(salary_text)
    else:
        min_salary = max_salary = None

    return {
        "job_name": job_name,
        "job_tags": job_tags,
        "job_salary": (min_salary, max_salary),
        "job_location": job_location,
        "job_url": job_url,
        "company_name": company_name,
    }


# Przykład użycia
nfj_search_results = split_records()
single_job_offer = extract_data_from_offer(nfj_search_results)
for key, value in single_job_offer.items():
    print(f"{key}: {value}")
