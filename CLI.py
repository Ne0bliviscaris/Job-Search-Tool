# Automatic update + sync using CLI
from time import sleep

from selenium.common.exceptions import InvalidSessionIdException, TimeoutException

from modules.database.backup import backup_db
from modules.updater.data_processing.sync import sync_records
from modules.updater.log import updater_log
from modules.updater.updater import update_site
from modules.updater.webdriver import setup_webdriver
from modules.websites import search_links


def main():
    """Run scraping with error handling and requeueing."""
    with setup_webdriver() as web_driver:
        # Convert dict to list for iteration, to remove items on success/failure
        remaining_links = list(search_links.items())
        updater_log("CLI").info("Starting CLI Update Process.")
        while remaining_links:
            key, value = remaining_links.pop(0)
            try:
                update_site(web_driver, key, value)
                print(f"Updated {key}.")
            except TimeoutException:
                print(f"Timeout error on {key}, will retry in 5 minutes.")
                updater_log("CLI").error(f"Timeout error on {key}, will retry in 5 minutes.")
                remaining_links.append((key, value))  # Requeue site
                sleep(300)  # Wait 5 minutes before retrying
            except InvalidSessionIdException:
                print("Session lost. Restarting WebDriver...")
                updater_log("CLI").error("Session lost. Restarting WebDriver...")
                # Quit the broken driver
                web_driver.quit()
                # Create new instance
                with setup_webdriver() as new_driver:
                    update_site(new_driver, key, value)
                    print(f"Updated {key} after session restart.")
                    updater_log("CLI").info(f"Updated {key} after session restart.")
        updater_log("CLI").info("Update process complete.")

    backup_db()
    print("Database backed up.")
    updater_log("CLI").info("Database backed up.")
    sync_records()
    print("Records synced.")
    updater_log("CLI").info("Records synced.")
    updater_log("CLI").info("CLI Update Process Complete.")


main()
