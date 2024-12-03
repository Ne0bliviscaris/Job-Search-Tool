import pandas as pd

# Sync debug mode switch
DEBUG_SYNC = False
# DEBUG_SYNC = True


# Manually paste the URL of the record to compare
URL = """



""".strip()


def find_differences(db_records, update_records):
    """Find differences between records in the database and new records based on URL."""
    db_record = db_records[db_records["url"] == URL]
    update_record = update_records[update_records["url"] == URL]

    if db_record.empty:
        print("Record not found in current_db.")
    if update_record.empty:
        print("Record not found in update.")

    if not db_record.empty and not update_record.empty:
        # Find common columns
        common_columns = db_record.columns.intersection(update_record.columns)

        # Create a comparison DataFrame with common columns
        comparison = pd.DataFrame(
            {
                "Field": common_columns,
                "Current DB": db_record[common_columns].iloc[0].values,
                "Update": update_record[common_columns].iloc[0].values,
            }
        )

        print("Differences between records:")
        for index, row in comparison.iterrows():
            current_db_value = row["Current DB"]
            update_value = row["Update"]
            if current_db_value != update_value:
                print(f"{row['Field']}:")
                print(f"  In DB:        {current_db_value}")
                print(f"  Updated:      {update_value}")

                different_types = type(current_db_value) != type(update_value)
                if different_types:
                    print(f"(In DB Type:    {type(current_db_value)}")
                    print(f" Updated Type:  {type(update_value)}")
