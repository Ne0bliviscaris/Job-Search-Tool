import requests
import websites as websites
from bs4 import BeautifulSoup


def get_search_block(search_link, search_container):
    """
    Get HTML block containing job search results
    """

    response = requests.get(search_link)
    soup = BeautifulSoup(response.content, "html.parser")
    job_listing = soup.find(search_container)
    # print(job_listing) # TEST PRINT
    return job_listing


def detect_records(search_results_block, record_container):
    """
    Split given HTML code block into records
    """
    records = [job for job in search_results_block.find_all(id=record_container)]
    return records

    # return records


def fetch_job_url(record):
    """
    Fetch job URL from the record."""
    url = record["href"]
    if url:
        return "https://nofluffjobs.com" + url
    return None


def fetch_job_title(record, title_container):
    """
    Fetch job title from the record.
    """
    job_title = [job.text for job in record.find(attrs=title_container)]
    return job_title


def fetch_job_tags(record, tags_container):
    """
    Fetch job tags from the record.
    """
    job_tags = [job.text for job in record.find_all(attrs=tags_container)]
    return job_tags


def fetch_company_name(record, company_container):
    company_name = record.find(company_container).text.strip()
    return company_name


def fetch_company_logo(record, logo_container):
    company_logo = record.find(logo_container)
    return company_logo


def fetch_job_location(records_html, location_container):
    job_location_elements = records_html.find_all(attrs=location_container)
    job_location = [job.text.strip() for job in job_location_elements]
    return job_location


def fetch_salary_range(records_html, salary_container):
    salary_elements = records_html.find_all(attrs=salary_container)

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
