import pandas as pd
import streamlit as st

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
    "website",
    "tags",
    "url",
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
    "website",
    "tags",
    "url",
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
    "added_date",
    "url",
    "application_date",
    "feedback_received",
    "notes",
    "personal_rating",
    "archived_date",
]


def set_column_config():
    """Return column configuration for the data editor."""
    return {
        "url": st.column_config.LinkColumn("URL", width=100),
        "logo": st.column_config.ImageColumn("Logo", width=100),
        "application_date": st.column_config.DateColumn("Application date", format="DD-MM-YYYY"),
        "added_date": st.column_config.DateColumn("Added date", format="DD-MM-YYYY"),
        "feedback_date": st.column_config.DateColumn("Feedback date", format="DD-MM-YYYY"),
        "feedback_received": st.column_config.CheckboxColumn("Feedback received"),
        "notes": st.column_config.TextColumn("Notes"),
        "application_status": st.column_config.SelectboxColumn(
            "Application Status", options=["Not applied", "Applied", "Interview", "Hired"], default="Not applied"
        ),
    }


def column_conversions(frame, archive=False):
    """Return column conversions for the data editor."""
    if archive is False:
        columns = MAIN_FRAME_COLUMNS
    else:
        columns = ARCHIVE_COLUMNS
    frame["notes"] = frame["notes"].fillna("").astype(str)
    frame["feedback_received"] = frame["feedback_received"].fillna(False).astype(bool)
    frame["added_date"] = pd.to_datetime(frame["added_date"], errors="coerce")
    if "archived_date" not in frame.columns:
        frame["archived_date"] = pd.NaT
    frame["archived_date"] = pd.to_datetime(frame["archived_date"], errors="coerce")
    frame["application_date"] = pd.to_datetime(frame["application_date"], errors="coerce")
    frame["feedback_date"] = pd.to_datetime(frame["feedback_date"], errors="coerce")
    frame["application_status"] = frame["application_status"].fillna("Not applied").astype(str)

    frame = calculate_elapsed_days(frame, archive=archive)
    frame = check_application_status(frame)
    frame = check_feedback_status(frame)

    edited_df = st.data_editor(frame[columns], disabled=archive, column_config=set_column_config())
    return edited_df


def calculate_elapsed_days(frame, archive=False):
    """Calculate elapsed days since the job offer was added."""
    if archive is False:
        frame["elapsed_days"] = (pd.Timestamp.now() - frame["added_date"]).dt.days
    else:
        frame["elapsed_days"] = (frame["archived_date"] - frame["added_date"]).dt.days

    if frame["application_date"] is not None:
        frame["time_until_feedback"] = (pd.Timestamp.now() - frame["application_date"]).dt.days
    else:
        frame["time_until_feedback"] = (frame["feedback_date"] - frame["application_date"]).dt.days
    return frame


def check_application_status(frame):
    """Tick unticked application status if applied."""
    frame.loc[
        (frame["application_status"] == "Not applied") & (frame["application_date"].notna()), "application_status"
    ] = "Applied"
    return frame


def check_feedback_status(frame):
    """Tick unticked feedback status if received."""
    frame.loc[(frame["feedback_received"] == False) & (frame["feedback_date"].notna()), "feedback_received"] = True
    return frame
