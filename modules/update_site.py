import os

import containers as containers
from data_collector import generate_filename, get_search_block


def update_site(key, search_link):
    """
    Download HTML content from the search link and save it to a file.
    """
    PRINTS = False
    current_website = key.split("_")[0]
    search_container = containers.search(current_website)

    search_block = get_search_block(search_link, search_container)

    # Ensure the directory exists
    directory = "modules/sites/"
    os.makedirs(directory, exist_ok=True)

    # Save HTML to file
    filename = os.path.join(directory, generate_filename(key))
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(search_block))

    if PRINTS:
        print(f"[updater.py - update_site] HTML content saved to: {filename}")
    return filename


def update_all_sites(search_links):
    """
    Download HTML content for all search links and save them to files.
    """
    PRINTS = False
    for key, search_link in search_links.items():
        if PRINTS:
            print(f"[updater.py - update_all_sites] Updating site with key: {key}")
        update_site(key, search_link)


if __name__ == "__main__":
    search_links = {
        "nofluffjobs_data-ai-trainee-junior": "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior",
        # Add more websites and their search links with tags here
    }
    update_all_sites(search_links)
