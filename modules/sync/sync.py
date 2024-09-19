import os
from datetime import datetime

import pandas as pd

RAW_FILE = "modules/sites/records.csv"
SYNCED_FILE = "modules/sites/synced_records.csv"
ARCHIVE_FILE = "modules/sites/archived_records.csv"
COLUMNS_TO_COMPARE = ["title", "company_name", "website", "remote_status", "salary_text"]


def load_csv(file):
    """Load CSV file, return empty DataFrame if file does not exist."""
    if os.path.exists(file):
        return pd.read_csv(file)
    return pd.DataFrame()


def save_csv(dataframe, file_path, mode="w", header=True):
    """Save DataFrame to CSV file."""
    dataframe.to_csv(file_path, mode=mode, header=header, index=False)


def set_columns(file):
    """Set columns for the DataFrame."""
    return set(file[COLUMNS_TO_COMPARE].apply(tuple, axis=1))


def sync_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """
    raw = load_csv(RAW_FILE)
    current_file = load_csv(SYNCED_FILE)
    current_records = set_columns(current_file) if not current_file.empty else set()
    raw_records = set_columns(raw)

    # Archive missing records
    missing_records = current_records - raw_records
    cleaned_current_file = archive_records(current_file, missing_records) if missing_records else current_file

    # # If the record is new, mark it and add a timestamp
    new_records = raw_records - current_records
    new_records_df = raw[raw[COLUMNS_TO_COMPARE].apply(tuple, axis=1).isin(new_records)]
    if not new_records_df.empty:
        new_records_df = add_timestamp(new_records_df, "added_date")
        cleaned_current_file = pd.concat([cleaned_current_file, new_records_df], ignore_index=True)

    # Save the updated synced file
    cleaned_current_file.to_csv(SYNCED_FILE, index=False)


def archive_records(synced, missing_records):
    """
    Archive missing records from synced file
    """
    records_to_archive = synced[synced[COLUMNS_TO_COMPARE].apply(tuple, axis=1).isin(missing_records)]

    if not records_to_archive.empty:
        records_to_archive = add_timestamp(records_to_archive, "archived_date")

        # Append records to the archive file, adding header if the file is empty
        is_empty_archive = not os.path.exists(ARCHIVE_FILE) or os.stat(ARCHIVE_FILE).st_size == 0
        save_csv(records_to_archive, ARCHIVE_FILE, mode="a", header=is_empty_archive)

        # Remove archived records from synced
        synced = synced[~synced[COLUMNS_TO_COMPARE].apply(tuple, axis=1).isin(missing_records)]

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
