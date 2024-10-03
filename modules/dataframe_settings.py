import pandas as pd
import streamlit as st

pd.set_option("future.no_silent_downcasting", True)

ALL_COLUMNS = [
    # From JobRecords class
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
    # Custom added columns
    "added_date",
    "elapsed_days",
    "application_status",
    "application_date",
    "feedback_received",
    "feedback_date",
    "time_until_feedback",
    "notes",
    "personal_rating",
    "archived_date",
]

MAIN_FRAME_COLUMNS = [
    # From JobRecords class
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
    # Custom added columns
    "notes",
    "personal_rating",
    "added_date",
    "elapsed_days",
    "application_status",
    "application_date",
    "feedback_received",
    "feedback_date",
    "time_until_feedback",
]

ARCHIVE_COLUMNS = [
    "title",
    "logo",
    "company_name",
    "location",
    "remote_status",
    "min_salary",
    "max_salary",
    "salary_details",
    "tags",
    "url",
    "website",
    "added_date",
    "elapsed_days",
    "application_date",
    "feedback_received",
    "notes",
    "personal_rating",
    "archived_date",
]


def set_column_config(archive=False):
    """Return column configuration for the data editor."""
    date_format = "DD-MM-YYYY"
    date_column = lambda name: st.column_config.DateColumn(name, format=date_format)
    application_statuses = ["Not applied", "Applied", "Interview", "Hired"]

    static_columns = {
        "title": st.column_config.TextColumn("Title", disabled=True),
        "company_name": st.column_config.TextColumn("Company Name", disabled=True),
        "location": st.column_config.TextColumn("Location", disabled=True),
        "remote_status": st.column_config.TextColumn("Remote Status", disabled=True),
        "salary_details": st.column_config.TextColumn("Salary Details", disabled=True),
        "salary_text": st.column_config.TextColumn("Salary Text", disabled=True),
        "tags": st.column_config.TextColumn("Tags", disabled=True),
        "logo": st.column_config.ImageColumn("Logo", width=100),
        "min_salary": st.column_config.NumberColumn("Min Salary", disabled=True),
        "max_salary": st.column_config.NumberColumn("Max Salary", disabled=True),
        "elapsed_days": st.column_config.NumberColumn("Elapsed Days", disabled=True),
        "website": st.column_config.LinkColumn("Website", disabled=True),
        "added_date": date_column("Added date"),
        "archived_date": date_column("Archived date"),
    }

    conditionally_editable_columns = {
        "application_status": st.column_config.SelectboxColumn(
            "Application Status", options=application_statuses, default="Not applied", disabled=archive
        ),
        "notes": st.column_config.TextColumn("Notes", disabled=archive),
        "personal_rating": st.column_config.NumberColumn("Personal Rating", disabled=False),
        "time_until_feedback": st.column_config.NumberColumn("Time Until Feedback", disabled=archive),
        "feedback_received": st.column_config.CheckboxColumn("Feedback received", disabled=archive),
        "application_date": date_column("Application date"),
        "feedback_date": date_column("Feedback date"),
        "url": st.column_config.LinkColumn("URL", width=100, disabled=archive),
    }

    # Combine both dictionaries
    column_config = {**static_columns, **conditionally_editable_columns}
    return column_config


def column_conversions(frame, archive=False):
    """Return column conversions for the data editor."""
    columns = MAIN_FRAME_COLUMNS if not archive else ARCHIVE_COLUMNS

    frame = fill_missing_values(frame)
    frame = convert_date_columns(frame)
    frame = calculate_elapsed_days(frame, archive=archive)
    frame = check_application_status(frame)
    frame = check_feedback_status(frame)

    edited_df = st.data_editor(frame[columns], disabled=archive, column_config=set_column_config(archive))
    return edited_df


def convert_date_columns(frame):
    """Convert date columns to datetime."""
    date_columns = ["added_date", "application_date", "feedback_date", "archived_date"]
    for col in date_columns:
        if col not in frame.columns:
            frame[col] = pd.NaT
        frame[col] = pd.to_datetime(frame[col], errors="coerce")
    return frame


def fill_missing_values(frame):
    """Fill missing values and convert types."""
    frame["notes"] = frame["notes"].fillna("").astype(str)
    frame["feedback_received"] = frame["feedback_received"].fillna(False).astype(bool)
    frame["application_status"] = frame["application_status"].fillna("Not applied").astype(str)
    return frame


def calculate_elapsed_days(frame, archive=False):
    """Calculate elapsed days since the job offer was added."""
    now = pd.Timestamp.now()
    # Calculate elapsed days

    added_date = frame["added_date"]
    archived_date = frame["archived_date"]
    application_date = frame["application_date"]
    feedback_date = frame["feedback_date"]

    if not archive:
        frame["elapsed_days"] = (now - added_date).dt.days
    else:
        frame["elapsed_days"] = (archived_date - added_date).dt.days

    # Calculate time until feedback
    if application_date is None:
        frame["time_until_feedback"] = pd.NA
    else:
        frame["time_until_feedback"] = (feedback_date - application_date).dt.days
    return frame


def check_application_status(frame):
    """Tick unticked application status if applied."""
    not_applied = frame["application_status"] == "Not applied"
    has_application_date = frame["application_date"].notna()
    manually_marked = frame["application_status"].isin(["Applied", "Rejected", "Interview", "Hired"])

    # Update application status only if not manually marked
    frame.loc[not_applied & has_application_date & ~manually_marked, "application_status"] = "Applied"
    return frame


def check_feedback_status(frame):
    """Tick unticked feedback status if received."""
    no_feedback = frame["feedback_received"] == False
    has_feedback_date = frame["feedback_date"].notna()
    manually_marked = frame["feedback_received"].isin([True])

    # Update feedback status only if not manually marked
    frame.loc[no_feedback & has_feedback_date & ~manually_marked, "feedback_received"] = True
    return frame
