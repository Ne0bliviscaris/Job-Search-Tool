import pandas as pd


def load_raw_csv():
    """
    Load raw CSV file with job offers
    """
    file_path = "modules/sites/records.csv"
    return pd.read_csv(file_path)


raw = load_raw_csv()

print(raw.head())


def process_records():
    """
    Main function to oversee the synchronisation process
    Extract records from raw, add additional information and return processed data into a new file
    """
    raw = load_raw_csv()
    return raw
