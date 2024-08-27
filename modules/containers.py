from websites import JUSTJOIN, NOFLUFFJOBS, ROCKETJOBS, THEPROTOCOL


def search(current_website):
    """
    Zwraca wartość kontenera wyszukiwania dla każdej strony internetowej
    """
    if current_website == NOFLUFFJOBS:
        return "nfj-postings-list"
    elif current_website == JUSTJOIN:
        return "TO BE DONE --------------"
    elif current_website == ROCKETJOBS:
        return "TO BE DONE --------------"
    elif current_website == THEPROTOCOL:
        return {"data-test": "offersList"}
    else:
        raise ValueError(f"Unknown website: {current_website}")


def record(current_website):
    """
    Zwraca wartość kontenera rekordu dla każdej strony internetowej
    """
    if current_website == NOFLUFFJOBS:
        return lambda id_name: id_name and id_name.startswith("nfjPostingListItem")
    elif current_website == JUSTJOIN:
        return "TO BE DONE --------------"
    elif current_website == ROCKETJOBS:
        return "TO BE DONE --------------"
    elif current_website == THEPROTOCOL:
        return {"data-test": "list-item-offer"}
    else:
        raise ValueError(f"Unknown website: {current_website}")


def job_title(current_website):
    """
    Returns title container for each website
    """
    if current_website == NOFLUFFJOBS:
        title_container = {"data-cy": "title position on the job offer listing"}

    elif current_website == JUSTJOIN:
        title_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        title_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        title_container = "TO BE DONE --------------"
    return title_container


def tags(current_website):
    """
    Returns tags container for each website
    """
    if current_website == NOFLUFFJOBS:
        tags_container = {"data-cy": "category name on the job offer listing"}

    elif current_website == JUSTJOIN:
        tags_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        tags_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        tags_container = "TO BE DONE --------------"
    return tags_container


def company(current_website):
    """
    Returns company name container for each website
    """
    if current_website == NOFLUFFJOBS:
        company_name = "h4"

    elif current_website == JUSTJOIN:
        company_name = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        company_name = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        company_name = "TO BE DONE --------------"
    return company_name


def logo(current_website):
    """
    Returns logo container for each website
    """
    if current_website == NOFLUFFJOBS:
        logo_container = {"alt": "Company logo"}

    elif current_website == JUSTJOIN:
        logo_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        logo_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        logo_container = "TO BE DONE --------------"
    return logo_container


def location(current_website):
    """
    Returns location container for each website
    """
    if current_website == NOFLUFFJOBS:
        location_container = {"data-cy": "location on the job offer listing"}

    elif current_website == JUSTJOIN:
        location_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        location_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        location_container = "TO BE DONE --------------"
    return location_container


def salary(current_website):
    """
    Returns salary container for each website
    """
    if current_website == NOFLUFFJOBS:
        salary_container = {"data-cy": "salary ranges on the job offer listing"}

    elif current_website == JUSTJOIN:
        salary_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        salary_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        salary_container = "TO BE DONE --------------"
    return salary_container
