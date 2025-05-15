import re

from modules.dicts import remote_work_dict

# Salary processing for JobRecord class


def ensure_string(salary):
    """Get the salary text from the salary tag"""
    if not salary:
        return None
    return salary if isinstance(salary, str) else salary.get_text(strip=True)


def salary_cleanup(salary_text):
    """Convert to lower case and remove PLN, "zł", and anything inside parentheses like "(B2B)"""
    processed_salary = re.sub(r"\(.*?\)", "", salary_text.lower())
    processed_salary = re.sub(r"(usd.*|pln.*|eur.*|zł.*)", "", processed_salary)
    processed_salary = (
        processed_salary.replace("–", "-").replace("\xa0", "").replace(",", "").replace("Znamy widełki", "").strip()
    )
    return processed_salary


def convert_k_notation(salary_range):
    """Convert 'k' notation (e.g., 4.5k, 5k) to full numbers"""
    return re.sub(r"(\d+(\.\d+)?)k", lambda x: str(int(float(x.group(1)) * 1000)), salary_range)


def extract_salary_details(cleaned_salary, salary_text):
    """Cut off the salary range from the string"""
    last_two_chars = cleaned_salary[-2:]
    index = salary_text.lower().rfind(last_two_chars)
    salary_details = salary_text[index + 2 :].strip() if index != -1 else None
    # Handle Bulldogjobs and NoFluffJobs case
    if salary_text == "Znamy widełki" or "Sprawdź" or "Undisclosed salary" in salary_text:
        salary_details = salary_text

    return salary_details


def get_salary_range(processed_salary):
    """Remove any non-digit or non-range characters"""
    return "".join(filter(lambda x: x.isdigit() or x == "-", processed_salary))


def split_salary(processed_salary):
    """Split salary range into min and max salary"""
    salary_parts = processed_salary.split("-")
    if len(salary_parts) >= 2:
        # Use first 2 parts as min and max salary
        min_salary = int(salary_parts[0].strip())
        max_salary = int(salary_parts[1].strip())
    else:
        min_salary = max_salary = int(processed_salary.strip()) if processed_salary else None

    return min_salary, max_salary


def remove_remote_status(location: str) -> str:
    """Remove remote work indicators from location string"""
    if not location:
        return None

    location = location.strip()
    parts = location.split(" | ")

    # Remove remote indicators
    filtered_parts = [
        part.strip()
        for part in parts
        if not any(kw in part.lower() for keywords in remote_work_dict.values() for kw in keywords)
    ]

    # Join remaining locations
    clean_location = " | ".join(filtered_parts)

    return clean_location if clean_location else None


def process_remote_status(status: str) -> str:
    """Process remote work status and return standardized format"""
    if not status:
        return "Unknown"

    status = status.lower()
    for key, keywords in remote_work_dict.items():
        if any(keyword in status for keyword in keywords):
            return key

    return "Unknown"
