from websites import JUSTJOIN, NOFLUFFJOBS, ROCKETJOBS, THEPROTOCOL


def search(search_link):
    """
    Returns search container for each website
    """
    if NOFLUFFJOBS in search_link:
        return "nfj-postings-list"
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return {"data-test": "offersList"}
    else:
        raise ValueError(f"Unknown website: {search_link}")


def record(search_link):
    """
    Returns record container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"id": lambda id_name: id_name and id_name.startswith("nfjPostingListItem")}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return {"data-test": "list-item-offer"}
    else:
        raise ValueError(f"Unknown website: {search_link}")


def job_title(search_link):
    """
    Returns title container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "title position on the job offer listing"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def tags(search_link):
    """
    Returns tags container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "category name on the job offer listing"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def company(search_link):
    """
    Returns company name container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {
            "class": "tw-text-gray-60 company-name tw-w-[50%] desktop:tw-w-auto tw-mb-0 !tw-text-xs !desktop:tw-text-sm tw-font-semibold desktop:tw-font-normal"
        }
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def logo(search_link):
    """
    Returns logo container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"alt": "Company logo"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def location(search_link):
    """
    Returns location container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "location on the job offer listing"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")


def salary(search_link):
    """
    Returns salary container for each website
    """
    if NOFLUFFJOBS in search_link:
        return {"data-cy": "salary ranges on the job offer listing"}
    elif JUSTJOIN in search_link:
        return "TO BE DONE --------------"
    elif ROCKETJOBS in search_link:
        return "TO BE DONE --------------"
    elif THEPROTOCOL in search_link:
        return "TO BE DONE --------------"
    else:
        raise ValueError(f"Unknown website: {search_link}")
