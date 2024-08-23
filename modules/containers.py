from websites import JUSTJOIN, NOFLUFFJOBS, ROCKETJOBS, THEPROTOCOL


def set_search_containers(current_website):
    """
    Zwraca wartości kontenerów dla każdej strony internetowej
    """
    if current_website == NOFLUFFJOBS:
        search_container = "nfj-postings-list"
        record_container = lambda id_name: id_name and id_name.startswith("nfjPostingListItem")

    elif current_website == JUSTJOIN:
        search_container = "TO BE DONE --------------"
        record_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        search_container = "TO BE DONE --------------"
        record_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        search_container = "TO BE DONE --------------"
        record_container = "TO BE DONE --------------"

    return search_container, record_container


# Backup - containers within records
def set_record_containers(current_website):
    """
    Zwraca wartości kontenerów dla każdej strony internetowej
    """
    if current_website == NOFLUFFJOBS:
        title_container = {"data-cy": "title position on the job offer listing"}
        tags_container = {"data-cy": "category name on the job offer listing"}
        company_container = "h4"
        logo_container = "img"

    elif current_website == JUSTJOIN:
        search_container = "TO BE DONE --------------"
        record_container = "TO BE DONE --------------"

    elif current_website == ROCKETJOBS:
        search_container = "TO BE DONE --------------"
        record_container = "TO BE DONE --------------"

    elif current_website == THEPROTOCOL:
        search_container = "TO BE DONE --------------"
        record_container = "TO BE DONE --------------"

    return title_container, tags_container, company_container, logo_container
