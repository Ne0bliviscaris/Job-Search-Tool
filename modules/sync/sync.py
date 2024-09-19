import os
from datetime import datetime

import pandas as pd

RAW_FILE = "modules/sites/records.csv"
SYNCED_FILE = "modules/sites/synced_records.csv"
ARCHIVE_FILE = "modules/sites/archived_records.csv"


def load_csv(file):
    """Load CSV file, return empty DataFrame if file does not exist."""
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()


def save_csv(dataframe, file_path, mode="w", header=True):
    """Save DataFrame to CSV file."""
    dataframe.to_csv(file_path, mode=mode, header=header, index=False)


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
    cleaned_current_file = archive_records(current_file, missing_ids) if missing_ids else current_file

    # # If the record is new, mark it and add a timestamp
    new_ids = raw_ids - current_ids
    new_records = raw[raw["id"].isin(new_ids)]
    if not new_records.empty:
        new_records = add_timestamp(new_records, "added_date")
        cleaned_current_file = pd.concat([cleaned_current_file, new_records], ignore_index=True)

    # Save the updated synced file
    cleaned_current_file.to_csv(SYNCED_FILE, index=False)


def archive_records(synced, missing_ids):
    """
    Archive records with ids in missing_ids from synced to archive file
    """
    records_to_archive = synced[synced["id"].isin(missing_ids)]

    if not records_to_archive.empty:
        records_to_archive = add_timestamp(records_to_archive, "archived_date")

        # Append records to the archive file, adding header if the file is empty
        is_empty_archive = not os.path.exists(ARCHIVE_FILE) or os.stat(ARCHIVE_FILE).st_size == 0
        save_csv(records_to_archive, ARCHIVE_FILE, mode="a", header=is_empty_archive)

        # Remove archived records from synced
        synced = synced[~synced["id"].isin(missing_ids)]

    return synced


def show_records(file):
    """Load and display records from a CSV file."""
    return load_csv(file)


def add_timestamp(records_frame, column_name):
    """
    Add a timestamp to the records DataFrame
    """
    records_frame[column_name] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return records_frame
