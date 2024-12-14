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
                "added_date": pd.to_datetime(f"2023-01-0{i+1}"),
                "application_date": pd.to_datetime(f"2023-01-0{i+3}"),
                "feedback_date": pd.to_datetime(f"2023-01-0{i+5}"),
                "archived_date": pd.to_datetime(f"2023-01-0{i+7}"),
                # Boolean columns
                "feedback_received": [True, False, True, False, True, False, True][i],
            }
            for i in range(7)
        ]
    )


def get_dummy_scraped_records():
    """Return scraped records in JobRecord DataFrame format."""
    return pd.DataFrame(
        [
            {
                "title": "Job1",
                "logo": "logo1.png",
                "company_name": "Company1",
                "location": "Location1",
                "remote_status": "Remote",
                "min_salary": 50000,
                "max_salary": 60000,
                "salary_details": "50k-60k",
                "salary_text": "50 000 - 60 000 PLN",
                "tags": "tag1, tag2",
                "url": "www.company1.com/jobs/1",
                "website": "www.company1.com",
            },
            {
                "title": "Job2",
                "logo": "logo2.png",
                "company_name": "Company2",
                "location": "Location2",
                "remote_status": "On-site",
                "min_salary": 70000,
                "max_salary": 80000,
                "salary_details": "70k-80k",
                "salary_text": "70 000 - 80 000 PLN",
                "tags": "tag3, tag4",
                "url": "www.company2.com/jobs/2",
                "website": "www.company2.com",
            },
            {
                "title": "Job8",
                "logo": "logo8.png",
                "company_name": "Company8",
                "location": "Location8",
                "remote_status": "Hybrid",
                "min_salary": 190000,
                "max_salary": 200000,
                "salary_details": "190k-200k",
                "salary_text": "190 000 - 200 000 PLN",
                "tags": "tag15, tag16",
                "url": "www.company8.com/jobs/8",
                "website": "www.company8.com",
            },
            {
                "title": "Job9",
                "logo": "logo9.png",
                "company_name": "Company9",
                "location": "Location9",
                "remote_status": "Remote",
                "min_salary": 210000,
                "max_salary": 220000,
                "salary_details": "210k-220k",
                "salary_text": "210 000 - 220 000 PLN",
                "tags": "tag17, tag18",
                "url": "www.company9.com/jobs/9",
                "website": "www.company9.com",
            },
            {
                "title": "Job10",
                "logo": "logo10.png",
                "company_name": "Company10",
                "location": "Location10",
                "remote_status": "On-site",
                "min_salary": 230000,
                "max_salary": 240000,
                "salary_details": "230k-240k",
                "salary_text": "230 000 - 240 000 PLN",
                "tags": "tag19, tag20",
                "url": "www.company10.com/jobs/10",
                "website": "www.company10.com",
            },
        ]
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
