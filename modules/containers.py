from websites import JUSTJOIN, NOFLUFFJOBS, ROCKETJOBS, THEPROTOCOL, identify_website


def search(search_link: str) -> str:
    """
    Returns search container for each website
    """
    current_website = identify_website(search_link)
    if NOFLUFFJOBS in current_website:
        return "nfj-postings-list"
    elif THEPROTOCOL in current_website:
        return '[data-test="offersList"]'
    elif JUSTJOIN in current_website:
        return '[data-test-id="virtuoso-item-list"]'
    elif ROCKETJOBS in current_website:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {current_website}")


def detect_records(html, search_link) -> list[str]:
    """
    Returns record container content for each website
    """
    if NOFLUFFJOBS in search_link:
        record_container = {"id": lambda id_name: id_name and id_name.startswith("nfjPostingListItem")}
        return [job for job in html.find_all(attrs=record_container)]

    elif THEPROTOCOL in search_link:
        record_container = {"data-test": "list-item-offer"}
        return [job for job in html.find_all(attrs=record_container)]

    elif JUSTJOIN in search_link:
        return {"class": "offer_list_offer_link css-3qyn8a"}

    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def job_title(html, search_link) -> str:
    """
    Returns title container content for each website
    """
    if NOFLUFFJOBS in search_link:
        title_container = {"data-cy": "title position on the job offer listing"}
        title = html.find(attrs=title_container)
        return title.text if title else None

    elif THEPROTOCOL in search_link:
        title_container = {"data-test": "text-jobTitle"}
        title = html.find(attrs=title_container)
        return title.text if title else None

    elif JUSTJOIN in search_link:
        return {"class": "css-3hs82j"}
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def tags(html, search_link: str) -> list[str]:
    """
    Returns tags container content for each website
    """
    if NOFLUFFJOBS in search_link:
        tags_container = {"data-cy": "category name on the job offer listing"}
        job_tags = [job.text for job in html.find_all(attrs=tags_container)]
        return job_tags if job_tags else None

    elif THEPROTOCOL in search_link:
        tags_container = {"data-test": "chip-expectedTechnology"}
        job_tags = [job.text for job in html.find_all(attrs=tags_container)]
        return job_tags if job_tags else None

    elif JUSTJOIN in search_link:
        return {"class": "MuiBox-root css-vzlxkq"}

    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"

    else:
        raise ValueError(f"Unknown website: {search_link}")


def company(html, search_link: str) -> dict:
    """
    Returns company name container content for each website
    """
    if NOFLUFFJOBS in search_link:
        company_container = {
            "class": "tw-text-gray-60 company-name tw-w-[50%] desktop:tw-w-auto tw-mb-0 !tw-text-xs !desktop:tw-text-sm tw-font-semibold desktop:tw-font-normal"
        }
        company = html.find(attrs=company_container)
        return company.text if company else None

    elif THEPROTOCOL in search_link:
        company_container = {"data-test": "text-employerName"}
        company = html.find(attrs=company_container)
        return company.text if company else None

    elif JUSTJOIN in search_link:
        return {"class": "css-7e0395"}

    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"

    else:
        raise ValueError(f"Unknown website: {search_link}")


def logo(html, search_link: str) -> dict:
    """
    Returns logo container content for each website
    """
    if NOFLUFFJOBS in search_link:
        logo_container = {"alt": "Company logo"}
        logo = html.find(attrs=logo_container)
        return logo.get("src") if logo else None

    elif THEPROTOCOL in search_link:
        logo_container = {"data-test": "icon-companyLogo"}
        logo = html.find(attrs=logo_container)
        return logo.get("src") if logo else None

    elif JUSTJOIN in search_link:
        logo_container = {"class": "MuiBox-root css-677aw9"}
        logo = html.find(attrs=logo_container)
        return logo.get("src") if logo else None

    elif ROCKETJOBS in search_link:
        logo_container = "TO BE DONE --------------"
        logo = html.find(attrs=logo_container)
        return logo.get("src") if logo else None

    else:
        raise ValueError(f"Unknown website: {search_link}")


def location(html, search_link: str) -> dict:
    """
    Returns location container content for each website
    """
    if NOFLUFFJOBS in search_link:
        location_container = {"data-cy": "location on the job offer listing"}
        job_location_elements = html.find_all(attrs=location_container)
        job_location = [job.text.strip() for job in job_location_elements]
        return job_location if job_location else None
    elif THEPROTOCOL in search_link:
        location_container = {"data-test": "text-workModes"}
        job_location_elements = html.find_all(attrs=location_container)
        job_location = [job.text.strip() for job in job_location_elements]
        return job_location if job_location else None
    elif JUSTJOIN in search_link:
        location_container = {"class": "css-1o4wo1x"}
    elif ROCKETJOBS in search_link:
        location_container = "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def salary(html, search_link: str) -> dict:
    """
    Returns salary container content for each website
    """
    if NOFLUFFJOBS in search_link:
        salary_container = {"data-cy": "salary ranges on the job offer listing"}
        return html.find(attrs=salary_container)

    elif THEPROTOCOL in search_link:
        salary_container = {"data-test": "text-salary"}
        return html.find(attrs=salary_container)

    elif JUSTJOIN in search_link:
        salary_container = {"class": "css-19u0lmu"}
    elif ROCKETJOBS in search_link:
        salary_container = "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")
