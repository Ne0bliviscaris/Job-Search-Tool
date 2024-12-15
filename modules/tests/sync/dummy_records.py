import pandas as pd


def get_dummy_db_records():
    """Return a DataFrame matching database records format."""
    return pd.DataFrame(
        [
            {
                # Integer columns
                "id": i + 1,
                "min_salary": (i + 1) * 20000,
                "max_salary": (i + 1) * 20000 + 10000,
                "personal_rating": [5, 4, 3, 5, 4, 3, 5][i],
                "users_id": [1, 2, 3, 4, 5, 1, 2][i],
                # String columns
                "title": f"Job{i+1}",
                "logo": f"logo{i+1}.png",
                "company_name": f"Company{i+1}",
                "location": f"Location{i+1}",
                "remote_status": ["Remote", "On-site", "Hybrid", "Remote", "On-site", "Remote", "Hybrid"][i],
                "salary_details": f"{(i+1)*20}k-{(i+1)*20 + 10}k",
                "salary_text": f"{(i+1)*20} 000 - {(i+1)*20 + 10} 000 PLN",
                "tags": f"tag{i*2+1}, tag{i*2+2}",
                "url": f"www.company{i+1}.com/jobs/{i+1}",
                "website": f"www.company{i+1}.com",
                "notes": None,
                "application_status": [
                    "Applied",
                    "Not applied",
                    "Applied",
                    "Not applied",
                    "Applied",
                    "Not applied",
                    "Applied",
                ][i],
                "offer_status": ["archived", "archived", "active", "archived", "active", "active", "archived"][i],
                # Date columns
                "added_date": pd.to_datetime(f"2023-01-{str(i+1).zfill(2)}"),
                "application_date": pd.to_datetime(f"2023-01-{str(min(i+3, 31)).zfill(2)}"),
                "feedback_date": pd.to_datetime(f"2023-01-{str(min(i+5, 31)).zfill(2)}"),
                "archived_date": pd.to_datetime(f"2023-01-{str(min(i+7, 31)).zfill(2)}"),
                # Boolean columns
                "feedback_received": [True, False, True, False, True, False, True][i],
            }
            for i in range(7)
        ]
    )


def get_dummy_scraped_records():
    """Return scraped records in JobRecord DataFrame format."""
    # Record indices for Job1, Job2, Job8, Job9, Job10
    indices = [0, 1, 7, 8, 9]
    return pd.DataFrame(
        [
            {
                "title": f"Job{i+1}",
                "logo": f"logo{i+1}.png",
                "company_name": f"Company{i+1}",
                "location": f"Location{i+1}",
                "remote_status": ["Remote", "On-site", "Hybrid", "Remote", "On-site"][j],
                "min_salary": (i + 1) * 20000,
                "max_salary": (i + 1) * 20000 + 10000,
                "salary_details": f"{(i+1)*20}k-{(i+1)*20 + 10}k",
                "salary_text": f"{(i+1)*20} 000 - {(i+1)*20 + 10} 000 PLN",
                "tags": f"tag{i*2+1}, tag{i*2+2}",
                "url": f"www.company{i+1}.com/jobs/{i+1}",
                "website": f"www.company{i+1}.com",
            }
            for j, i in enumerate(indices)
        ]
    )


def get_dummy_empty_records():
    """Return an empty DataFrame."""
    return pd.DataFrame()


def get_dummy_fully_overlapping_records():
    """Return records that exactly match first 3 records from dummy database."""
    db_records = get_dummy_db_records()
    overlapping_cols = [
        "title",
        "logo",
        "company_name",
        "location",
        "remote_status",
        "min_salary",
        "max_salary",
        "salary_details",
        "salary_text",
        "tags",
        "url",
        "website",
    ]
    return db_records.head(3)[overlapping_cols]


def get_dummy_partially_overlapping_records():
    """Return mix of existing and new records."""
    db_records = get_dummy_db_records()
    scraped_records = get_dummy_scraped_records()

    overlapping_cols = [
        "title",
        "logo",
        "company_name",
        "location",
        "remote_status",
        "min_salary",
        "max_salary",
        "salary_details",
        "salary_text",
        "tags",
        "url",
        "website",
    ]

    # Get first 2 records from DB and records 8-9 from scraped
    existing_records = db_records.head(2)[overlapping_cols]
    new_records = scraped_records[scraped_records["title"].isin(["Job8", "Job9"])][overlapping_cols]

    return pd.concat([existing_records, new_records], ignore_index=True)


def get_dummy_already_archived_records():
    """Return archived records filtered from dummy database."""
    db_records = get_dummy_db_records()
    return db_records[db_records["offer_status"] == "archived"]


def get_dummy_active_records():
    """Return active records filtered from dummy database."""
    db_records = get_dummy_db_records()
    return db_records[db_records["offer_status"] == "active"]


def get_dummy_changed_records():
    """Return records with modified values in comparable columns."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job2", "Job3"],
            "company_name": ["Company1", "Company2", "Company3"],
            "website": ["www.company1.com", "www.company2.com", "www.company3.com"],
            "remote_status": ["Hybrid", "Remote", "On-site"],  # Changed
            "salary_details": ["60k-70k", "80k-90k", "100k-110k"],  # Changed
            "tags": ["tag1, tag3", "tag3, tag5", "tag5, tag7"],  # Changed
            "location": ["Location2", "Location3", "Location4"],  # Changed
        }
    )
