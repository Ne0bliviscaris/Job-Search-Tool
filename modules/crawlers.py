from containers import set_record_containers, set_search_containers
from scrappers.listing_scrappers import (
    detect_records,
    fetch_company_logo,
    fetch_company_name,
    fetch_job_tags,
    fetch_job_title,
    fetch_job_url,
    get_search_block,
)
from websites import identify_website, search_links


def search_all_sites():
    all_search_results = []
    for link in search_links:
        site = search_links[link]
        search_result = search_site(site)
        all_search_results.append(search_result)
    return all_search_results


# This function will manage the search for each website
def search_site(search_link):
    """
    Get HTML block containing job search results
    """
    current_website = identify_website(search_link)
    search_container, record_container = set_search_containers(current_website)
    search_block = get_search_block(search_link, search_container)
    search_records = detect_records(search_block, record_container)

    # Przetwarzanie każdego rekordu w search_records
    extracted_record = [extract_from_record(current_website, record) for record in search_records]
    return extracted_record
    # return search_results


def extract_from_record(current_website, search_records):
    """
    Extract job title, tags, salary, location, URL and company name from the record
    """
    title_container, tags_container, company_container, logo_container = set_record_containers(current_website)
    job_url = fetch_job_url(search_records)
    job_title = fetch_job_title(search_records, title_container)
    job_tags = fetch_job_tags(search_records, tags_container)
    company_name = fetch_company_name(search_records, company_container)
    logo = fetch_company_logo(search_records, logo_container)
    return job_title, job_url, job_tags, company_name, logo


# Test the code
nfj = search_links[0]
job_listing = search_site(nfj)[0]

# job_title = fetch_job_title(job_listing)
# print(job_listing)
print(job_listing)
