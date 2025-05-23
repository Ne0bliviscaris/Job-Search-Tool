import json
import os

from bs4 import BeautifulSoup

from modules.settings import FILE_STORAGE_PATH
from modules.websites import search_links


def set_filename_from_link(link: str, extension: str = "html") -> str:
    """Generate filename based on link key in search_links dict"""
    link_name = next((key for key, value in search_links.items() if value == link), link)
    return os.path.join(FILE_STORAGE_PATH, f"{link_name}.{extension}")


def load_json(filename) -> dict:
    with open(filename, "r", encoding="utf-8") as f:
        file = f.read()
        data = json.loads(file)
        return data


def save_json(filename, data) -> None:
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def save_html(filename, data) -> None:
    """Save HTML content to a file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(str(data))


def load_html_as_soup(filename: str) -> BeautifulSoup:
    """Convert HTML file to BeautifulSoup object"""
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")
