from websites import JUSTJOIN, NOFLUFFJOBS, ROCKETJOBS, THEPROTOCOL


def search(search_link: str) -> str:
    """
    Returns search container for each website
    """
    if NOFLUFFJOBS in search_link:
        return "nfj-postings-list"
    elif THEPROTOCOL in search_link:
        return '[data-test="offersList"]'
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def record(search_link: str) -> dict:
    """
    Returns record container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"id": lambda id_name: id_name and id_name.startswith("nfjPostingListItem")}
    elif THEPROTOCOL in search_link:
        return {"data-test": "list-item-offer"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def job_title(search_link: str) -> dict:
    """
    Returns title container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "title position on the job offer listing"}
    elif THEPROTOCOL in search_link:
        return {"data-test": "text-jobTitle"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def tags(search_link: str) -> dict:
    """
    Returns tags container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "category name on the job offer listing"}
    elif THEPROTOCOL in search_link:
        return {"data-test": "chip-expectedTechnology"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def company(search_link: str) -> dict:
    """
    Returns company name container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {
            "class": "tw-text-gray-60 company-name tw-w-[50%] desktop:tw-w-auto tw-mb-0 !tw-text-xs !desktop:tw-text-sm tw-font-semibold desktop:tw-font-normal"
        }
    elif THEPROTOCOL in search_link:
        return {"data-test": "text-employerName"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def logo(search_link: str) -> dict:
    """
    Returns logo container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"alt": "Company logo"}
    elif THEPROTOCOL in search_link:
        return {"data-test": "icon-companyLogo"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def location(search_link: str) -> dict:
    """
    Returns location container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "location on the job offer listing"}
    elif THEPROTOCOL in search_link:
        return {"data-test": "text-workModes"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def salary(search_link: str) -> dict:
    """
    Returns salary container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "salary ranges on the job offer listing"}
    elif THEPROTOCOL in search_link:
        return {"data-test": "text-salary"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")
