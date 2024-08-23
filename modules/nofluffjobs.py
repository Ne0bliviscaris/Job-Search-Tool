import requests
import search_links
from bs4 import BeautifulSoup


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


def extract_data_from_offer(jobs_listing, index=0):
    records = split_records(jobs_listing)

    job_name = extract_job_name(records, index)
    job_tags = extract_job_tags(records, index)
    job_salary = extract_salary(records, index)
    job_location = extract_job_location(records, index)
    job_url = extract_job_url(records, index)
    company_name = extract_company_name(records, index)

    return job_name, job_tags, job_salary, job_location, job_url, company_name


# Przykład użycia
nfj_search_results = nofluffjobs_search_results()
single_job_offer = extract_data_from_offer(nfj_search_results)
print(single_job_offer)
# print(extract_data_from_offers())
