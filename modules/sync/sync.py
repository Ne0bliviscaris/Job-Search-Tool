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


def filter_records(df, records):
    """Returns only df records matching given records.
    Compares content of columns specified in COLUMNS_TO_COMPARE."""
    columns = df[COLUMNS_TO_COMPARE]
    df_rows = columns.apply(tuple, axis=1)
    is_in_records = df_rows.isin(records)
    return df[is_in_records]


def sync_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """
    missing_records, new_records, current_file, update = changed_records()

    # Archive missing records
    cleaned_current_file = archive_records(current_file, missing_records)

    # If the record is new, add a timestamp
    new_records_df = filter_records(update, new_records)
    if not new_records_df.empty:
        new_records_df = add_timestamp(new_records_df, "added_date")
        cleaned_current_file = pd.concat([cleaned_current_file, new_records_df], ignore_index=True)

    # Save the updated synced file
    cleaned_current_file.to_csv(SYNCED_FILE, index=False)


def archive_records(current_file, missing_records):
    """
    Archive missing records from synced file
    """
    records_to_archive = filter_records(current_file, missing_records)

    if not records_to_archive.empty:
        records_to_archive = add_timestamp(records_to_archive, "archived_date")

        # Append records to the archive file, adding header if the file is empty
        is_empty_archive = not os.path.exists(ARCHIVE_FILE) or os.stat(ARCHIVE_FILE).st_size == 0
        save_csv(records_to_archive, ARCHIVE_FILE, mode="a", header=is_empty_archive)

        # Remove archived records from current_file
        current_file = remove_archived_records(current_file, missing_records)

    return current_file


def remove_archived_records(df, records_to_remove):
    """
    Remove records from DataFrame based on compared columns content.
    """
    columns = df[COLUMNS_TO_COMPARE]
    rows_as_tuples = columns.apply(tuple, axis=1)
    not_in_records_to_remove = ~rows_as_tuples.isin(records_to_remove)
    return df[not_in_records_to_remove]


def changed_records():
    """Load files and return missing and new records."""
    update = load_csv(RAW_FILE)
    current_file = load_csv(SYNCED_FILE)
    current_records = set_columns(current_file) if not current_file.empty else set()
    update_records = set_columns(update)

    missing_records = current_records - update_records
    new_records = update_records - current_records

    return missing_records, new_records, current_file, update


def show_records(file) -> pd.DataFrame:
    """Load and display records from a CSV file."""
    return load_csv(file)


def add_timestamp(records_frame, column_name):
    """
    Add a timestamp to the records DataFrame
    """
    records_frame[column_name] = datetime.now().strftime("%Y-%m-%d %H:%M")
    return records_frame
