# Automatic update + sync using CLI
import asyncio
from time import sleep

from modules.database.backup import backup_db
from modules.updater.data_processing.sync import sync_records
from modules.updater.log import updater_log
from modules.updater.updater import update_site
from modules.websites import search_links


async def update_link(link_name, site_url):
    """Update single site with retry once."""
    try:
        await update_site(site_url)
        print(f"Updated {link_name}.")
        updater_log("CLI").info(f"Updated {link_name}.")
    except Exception as e:
        print(f"Error on {link_name}: {e}. Retrying in 5 minutes.")
        updater_log("CLI").error(f"Error on {link_name}: {e}. Retrying in 5 minutes.")
        await asyncio.sleep(300)
        try:
            await update_site(site_url)
            print(f"Updated {link_name} after retry.")
            updater_log("CLI").info(f"Updated {link_name} after retry.")
        except Exception as e:
            print(f"Failed again on {link_name}: {e}. Skipping.")
            updater_log("CLI").error(f"Failed again on {link_name}: {e}. Skipping.")


async def main():
    """Run parallel scraping and sync."""
    updater_log("CLI").info("Starting CLI Update Process.")
    tasks = [update_link(name, url) for name, url in search_links.items()]
    await asyncio.gather(*tasks)
    updater_log("CLI").info("Update process complete.")
    backup_db()
    print("Database backed up.")
    updater_log("CLI").info("Database backed up.")
    sync_records()
    print("Records synced.")
    updater_log("CLI").info("Records synced.")
    updater_log("CLI").info("CLI Update Process Complete.")
    await asyncio.sleep(15)


if __name__ == "__main__":
    asyncio.run(main())
