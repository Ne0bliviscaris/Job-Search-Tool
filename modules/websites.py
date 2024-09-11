NOFLUFFJOBS = "https://nofluffjobs.com"
THEPROTOCOL = "https://theprotocol.it"
BULLDOGJOB = "https://bulldogjob.pl"
ROCKETJOBS = "https://rocketjobs.pl"
JUSTJOINIT = "https://justjoin.it"
SOLIDJOBS = "https://solid.jobs"
PRACUJPL = "https://it.pracuj.pl"
INHIRE = "https://inhire.io"

current_website = None

search_links = {
    "nofluffjobs_data-ai-trainee-junior": "https://nofluffjobs.com/pl/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior",
    "theprotocol_big-data-ai-ml-junior-assistant-trainee": "https://theprotocol.it/filtry/big-data-science,ai-ml;sp/junior,assistant,trainee;p",
    "bulldogjob_remote-data": "https://bulldogjob.pl/companies/jobs/s/locationDistance,50/role,data/city,Remote",
    "rocketjobs_remote-data": "https://rocketjobs.pl/wszystkie-lokalizacje/bi-data/praca-zdalna_tak",
    "justjoinit_data-junior-remote": "https://justjoin.it/all-locations/data/experience-level_junior/remote_yes?orderBy=DESC&sortBy=newest",
    "solidjobs_data-regular-remote": "https://solid.jobs/offers/it;categories=Data%20Science;cities=Praca%20zdalna;experiences=Regular",
    # "pracujpl_data-ai-junior-remote": "https://it.pracuj.pl/praca/praca%20zdalna;wm,home-office?et=17&ap=true&its=ai-ml%2Cbig-data-science",
    # "inhire_it-data-etl-ml-junior-remote": "https://inhire.io/?experiences=1_2,0_1&locations=1,39&roles=it,data_science,etl_developer,big_data,machine_learning_engineer",
}


def identify_website(search_link: str) -> str:
    """
    Set current website based on search link
    """
    if "nofluffjobs" in search_link:
        current_website = NOFLUFFJOBS
    elif "bulldogjob" in search_link:
        current_website = BULLDOGJOB
    elif "theprotocol" in search_link:
        current_website = THEPROTOCOL
    elif "rocketjobs" in search_link:
        current_website = ROCKETJOBS
    elif "justjoin" in search_link:
        current_website = JUSTJOINIT
    elif "solid" in search_link:
        current_website = SOLIDJOBS
    elif "pracuj" in search_link:
        current_website = PRACUJPL
    elif "inhire" in search_link:
        current_website = INHIRE
    else:
        current_website = "Error: Website not recognized"

    return current_website
