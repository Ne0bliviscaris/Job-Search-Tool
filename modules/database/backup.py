import os
import shutil
from datetime import datetime

from pandas import Timestamp

from modules.updater.log import updater_log


def fetch_all_backups():
    """Fetch all database backups."""
    backup_dir = "modules\\database\\db backup"
    if os.path.exists(backup_dir):
        backups = os.listdir(backup_dir)
        backups = sorted(backups, key=lambda f: get_date_from_filename(f), reverse=True)
        return backups
    else:
        return []


def backup_db():
    """Create a backup of the database."""
    db_file = "modules\\database\\database.db"
    timestamp = Timestamp.now().strftime("%d-%m-%Y-%H-%M")
    backup_dir = "modules\\database\\db backup"

    backup_path = backup_dir + "\\" + f"{timestamp}.db"
    if not os.path.exists(backup_path):
        shutil.copy(db_file, backup_path)
        print(f"Database backup created: {backup_path}")
        updater_log("DB").info(f"Database backup created: {backup_path}")
    else:
        print("Database has already been backed up within the last minute.")


def get_date_from_filename(filename):
    """Return datetime extracted from backup filename."""
    basename = os.path.basename(filename)
    timestamp_str, _ = os.path.splitext(basename)
    # Expected format: "day-month-year-hour-minute"
    try:
        date = datetime.strptime(timestamp_str, "%d-%m-%Y-%H-%M")
    except ValueError:
        date = filename
    return date


def restore_backup(selected_backup):
    """Restore a database backup."""
    db_file = "modules\\database\\database.db"
    backup_dir = "modules\\database\\db backup"

    backup_path = backup_dir + "\\" + selected_backup

    try:
        shutil.copy(backup_path, db_file)
        print(f"Database backup restored: {backup_path}")
        updater_log("DB").info(f"Database backup restored: {backup_path}")
    except PermissionError as error:
        print("Error: Ensure all connections to the database are closed before restoring backup.")
        raise error
