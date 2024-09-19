import os
from datetime import datetime

import pandas as pd

RAW_FILE = "modules/sites/records.csv"
SYNCED_FILE = "modules/sites/synced_records.csv"
ARCHIVE_FILE = "modules/sites/archived_records.csv"


def load_csv(csv):
    """
    Load raw CSV file with job offers
    Return empty DataFrame if file does not exist
    """
    try:
        file = pd.read_csv(csv)
        return file
    except FileNotFoundError:
        return pd.DataFrame()


def sync_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """
    raw = load_csv(RAW_FILE)
    current_file = load_csv(SYNCED_FILE)
    current_ids = set(current_file["id"]) if not current_file.empty else set()
    raw_ids = set(raw["id"])

    # Archive missing records
    missing_ids = current_ids - raw_ids
    if missing_ids:
        cleaned_current_file = archive_records(current_file, missing_ids)
    else:
        cleaned_current_file = current_file

    # # If the record is new, mark it and add a timestamp
    new_ids = raw_ids - current_ids
    new_records = raw[raw["id"].isin(new_ids)]
    if not new_records.empty:
        new_records = add_timestamp(new_records, "added_date")

    # If there are new records, append them to the synced DataFrame
    if not new_records.empty:
        synced_df = pd.concat([cleaned_current_file, new_records], ignore_index=True)
    else:
        synced_df = cleaned_current_file

    # Save the updated synced file
    synced_df.to_csv(SYNCED_FILE, index=False)


def archive_records(synced, missing_ids):
    """
    Archive records with ids in missing_ids from synced to archive file
    """
    records_to_archive = synced[synced["id"].isin(missing_ids)]

    if not records_to_archive.empty:
        # Add archived_date column
        records_to_archive = add_timestamp(records_to_archive, "archived_date")

        # Append records to the archive file, adding header if the file is empty
        is_empty_archive = not os.path.exists(ARCHIVE_FILE) or os.stat(ARCHIVE_FILE).st_size == 0
        records_to_archive.to_csv(ARCHIVE_FILE, mode="a", header=is_empty_archive, index=False)

        # Remove archived records from synced
        synced = synced[~synced["id"].isin(missing_ids)]

    return synced


def show_synced_records():
    """
    Load and display the synced records
    """
    synced = load_csv(SYNCED_FILE)
    return pd.DataFrame(synced) if not synced.empty else pd.DataFrame()


def show_archive():
    """
    Load and display the archived records
    """
    archived = load_csv(ARCHIVE_FILE)
    return pd.DataFrame(archived) if not archived.empty else pd.DataFrame()


def add_timestamp(records_frame, column_name):
    """
    Add a timestamp to the records DataFrame
    """
    records_frame[column_name] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return records_frame
