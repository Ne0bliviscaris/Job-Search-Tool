NOFLUFFJOBS = "https://nofluffjobs.com"
THEPROTOCOL = "https://theprotocol.it"
BULLDOGJOB = "https://bulldogjob.pl"
ROCKETJOBS = "rocketjobs"
SOLIDJOBS = "solidjobs"

current_website = None

search_links = {
    "nofluffjobs_data-ai-trainee-junior": "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior",
    "nofluffjobs_data-ai-trainee-junior-mid": "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior,mid",
    "theprotocol_big-data-ai-ml-junior-assistant-trainee": "https://theprotocol.it/filtry/big-data-science,ai-ml;sp/junior,assistant,trainee;p",
    "bulldogjob_remote-data": "https://bulldogjob.pl/companies/jobs/s/locationDistance,50/role,data/city,Remote",
}


def identify_website(search_link):
    """
    Set current website as global variable based on search link
    """
    if "nofluffjobs" in search_link:
        current_website = NOFLUFFJOBS
    elif "bulldogjob" in search_link:
        current_website = BULLDOGJOB
    elif "theprotocol" in search_link:
        current_website = THEPROTOCOL
    elif "rocketjobs" in search_link:
        current_website = ROCKETJOBS
    else:
        print("identify_website: Error: Website not recognized")
        current_website = "Error: Website not recognized"

    return current_website
