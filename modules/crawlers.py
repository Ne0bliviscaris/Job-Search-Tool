from containers import set_search_containers
from JobRecord import JobRecord
from scrappers.listing_scrappers import detect_records, get_search_block
from websites import identify_website, search_links


def search_all_sites():
    """
    Search all websites in search_links
    """
    all_search_results = []
    for site in search_links:
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

    # Process HTML code into JobRecord objects
    extracted_record = [JobRecord(record, current_website) for record in search_records]
    return extracted_record
    # return search_results


# Test full search and return the first record
# full_search = search_all_sites()
# print(full_search[0][0])


# Test search for a single website
single_search = search_site(search_links[0])
print(single_search[0])
