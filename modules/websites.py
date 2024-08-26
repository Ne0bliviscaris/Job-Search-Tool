NOFLUFFJOBS = "https://nofluffjobs.com"
JUSTJOIN = "justjoin"
THEPROTOCOL = "theprotocol"
ROCKETJOBS = "rocketjobs"

current_website = None

search_links = [
    # NFJ Data AI Trainee Junior
    "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior",
]


def identify_website(search_link):
    """
    Set current website as global variable based on search link
    """
    global current_website
    if "nofluffjobs.com" in search_link:
        current_website = NOFLUFFJOBS
    elif "justjoin.it" in search_link:
        current_website = JUSTJOIN
    elif "theprotocol.it" in search_link:
        current_website = THEPROTOCOL
    elif "rocketjobs.pl" in search_link:
        current_website = ROCKETJOBS
    else:
        current_website = "Error: Website not recognized"

    return current_website
