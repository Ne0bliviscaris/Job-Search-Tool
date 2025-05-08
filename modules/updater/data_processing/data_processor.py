from bs4 import BeautifulSoup


def html_to_soup(filename: str) -> BeautifulSoup:
    """Convert HTML file to BeautifulSoup object"""
    with open(filename, "r", encoding="utf-8") as file:
        return BeautifulSoup(file, "html.parser")
