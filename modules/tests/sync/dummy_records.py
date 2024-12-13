import pandas as pd


def get_dummy_db_records():
    """Return a DataFrame with all dummy records."""
    return pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 6, 7],
            "title": ["Job1", "Job2", "Job3", "Job4", "Job5", "Job6", "Job7"],
            "company_name": ["Company1", "Company2", "Company3", "Company4", "Company5", "Company6", "Company7"],
            "website": [
                "www.company1.com",
                "www.company2.com",
                "www.company3.com",
                "www.company4.com",
                "www.company5.com",
                "www.company6.com",
                "www.company7.com",
            ],
            "remote_status": ["Remote", "On-site", "Hybrid", "Remote", "On-site", "Remote", "Hybrid"],
            "salary_details": ["50k-60k", "70k-80k", "90k-100k", "110k-120k", "130k-140k", "150k-160k", "170k-180k"],
            "tags": [
                "tag1, tag2",
                "tag3, tag4",
                "tag5, tag6",
                "tag7, tag8",
                "tag9, tag10",
                "tag11, tag12",
                "tag13, tag14",
            ],
            "location": ["Location1", "Location2", "Location3", "Location4", "Location5", "Location6", "Location7"],
            "min_salary": [50000, 70000, 90000, 110000, 130000, 150000, 170000],
            "max_salary": [60000, 80000, 100000, 120000, 140000, 160000, 180000],
            "personal_rating": [5, 4, 3, 5, 4, 3, 5],
            "users_id": [1, 2, 3, 4, 5, 1, 2],
            "added_date": pd.to_datetime(
                ["2023-01-01", "2023-01-02", "2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07"]
            ),
            "application_date": pd.to_datetime(
                ["2023-01-03", "2023-01-04", "2023-01-05", "2023-01-06", "2023-01-07", "2023-01-08", "2023-01-09"]
            ),
            "feedback_date": pd.to_datetime(
                ["2023-01-05", "2023-01-06", "2023-01-07", "2023-01-08", "2023-01-09", "2023-01-10", "2023-01-11"]
            ),
            "archived_date": pd.to_datetime(
                ["2023-01-07", "2023-01-08", "2023-01-09", "2023-01-10", "2023-01-11", "2023-01-12", "2023-01-13"]
            ),
            "feedback_received": [True, False, True, False, True, False, True],
            "application_status": [
                "Applied",
                "Not applied",
                "Applied",
                "Not applied",
                "Applied",
                "Not applied",
                "Applied",
            ],
            "offer_status": ["archived", "archived", "active", "archived", "active", "active", "archived"],
        }
    )


def get_dummy_scraped_records():
    """Return scraped records including some new and some existing."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job2", "Job8", "Job9", "Job10"],
            "company_name": ["Company1", "Company2", "Company8", "Company9", "Company10"],
            "website": [
                "www.company1.com",
                "www.company2.com",
                "www.company8.com",
                "www.company9.com",
                "www.company10.com",
            ],
            "remote_status": ["Remote", "On-site", "Hybrid", "Remote", "On-site"],
            "salary_details": ["50k-60k", "70k-80k", "190k-200k", "210k-220k", "230k-240k"],
            "tags": ["tag1, tag2", "tag3, tag4", "tag15, tag16", "tag17, tag18", "tag19, tag20"],
            "location": ["Location1", "Location2", "Location8", "Location9", "Location10"],
        }
    )


def get_dummy_empty_records():
    """Return an empty DataFrame."""
    return pd.DataFrame()


def get_dummy_fully_overlapping_records():
    """Return records that exactly match records from dummy database."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job2", "Job3"],
            "company_name": ["Company1", "Company2", "Company3"],
            "website": ["www.company1.com", "www.company2.com", "www.company3.com"],
            "remote_status": ["Remote", "On-site", "Hybrid"],
            "salary_details": ["50k-60k", "70k-80k", "90k-100k"],
            "tags": ["tag1, tag2", "tag3, tag4", "tag5, tag6"],
            "location": ["Location1", "Location2", "Location3"],
        }
    )


def get_dummy_partially_overlapping_records():
    """Return mix of existing and new records without modifications."""
    return pd.DataFrame(
        {
            "title": ["Job1", "Job2", "Job8", "Job9"],
            "company_name": ["Company1", "Company2", "Company8", "Company9"],
            "website": ["www.company1.com", "www.company2.com", "www.company8.com", "www.company9.com"],
            "remote_status": ["Remote", "On-site", "Hybrid", "Remote"],
            "salary_details": ["50k-60k", "70k-80k", "190k-200k", "210k-220k"],
            "tags": ["tag1, tag2", "tag3, tag4", "tag15, tag16", "tag17, tag18"],
            "location": ["Location1", "Location2", "Location8", "Location9"],
        }
    )


def get_dummy_already_archived_records():
    """Return archived records filtered from dummy database."""
    db_records = get_dummy_db_records()
    return db_records[db_records["offer_status"] == "archived"]


def get_dummy_active_records():
    """Return active records filtered from dummy database."""
    db_records = get_dummy_db_records()
    return db_records[db_records["offer_status"] == "active"]


def get_changed_records():
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
