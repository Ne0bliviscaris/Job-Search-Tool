NOFLUFFJOBS = "https://nofluffjobs.com"
THEPROTOCOL = "https://theprotocol.it"
BULLDOGJOB = "https://bulldogjob.pl"
ROCKETJOBS = "https://rocketjobs.pl"
JUSTJOINIT = "https://justjoin.it"
SOLIDJOBS = "https://solid.jobs"
PRACUJPL = "https://it.pracuj.pl"

search_links = {
    # # Remote offers
    "nofluffjobs_data-ai-trainee-junior-remote": "https://nofluffjobs.com/pl/praca-zdalna/artificial-intelligence?criteria=category%3Ddata%20seniority%3Dtrainee,junior",
    "theprotocol_python-big-data-ai-ml-junior-assistant-trainee-remote": "https://theprotocol.it/filtry/python;t/big-data-science,ai-ml;sp/junior,assistant,trainee;p/zdalna;rw",
    "bulldogjob_data-remote": "https://bulldogjob.pl/companies/jobs/s/locationDistance,50/role,data/city,Remote",
    "rocketjobs_data-junior-remote": "https://rocketjobs.pl/wszystkie-lokalizacje/bi-data/doswiadczenie_staz-junior/praca-zdalna_tak",
    "justjoinit_data-junior-remote": "https://justjoin.it/all-locations/data/experience-level_junior/remote_yes?orderBy=DESC&sortBy=newest",
    "justjoinit_ai-junior-remote": "https://justjoin.it/all-locations/ai/experience-level_junior/remote_yes?orderBy=DESC&sortBy=newest",
    "solidjobs_data-junior-remote": "https://solid.jobs/offers/it;cities=Praca%20zdalna;categories=Data%20Science;experiences=Junior",
    "pracujpl_data-ai-junior-remote": "https://it.pracuj.pl/praca/praca%20zdalna;wm,home-office?et=17&ap=true&its=ai-ml%2Cbig-data-science",
    "pracujpl_data-ai-junior-remote": "https://it.pracuj.pl/praca/praca%20zdalna;wm,home-office?et=17&ap=true&its=ai-ml%2Cbig-data-science",
    # # Hybrid/local offers
    # "nofluffjobs_data-ai-trainee-junior-poznan": "https://nofluffjobs.com/pl/hybrid/artificial-intelligence?criteria=city%3Dpoznan%20category%3Ddata%20seniority%3Dtrainee,junior",
    # "theprotocol_python-big-data-ai-ml-junior-assistant-trainee-poznan": "https://theprotocol.it/filtry/python;t/big-data-science,ai-ml;sp/junior,assistant,trainee;p/poznan;wp/hybrydowa,zdalna;rw",
    # "bulldogjob_data-poznan": "https://bulldogjob.pl/companies/jobs/s/locationDistance,50/role,data/city,Pozna%C5%84",
    # "pracujpl_data-ai-junior-poznan": "https://it.pracuj.pl/praca/poznan;wp/praca%20hybrydowa;wm,hybrid?rd=30&et=17&ap=true&its=ai-ml%2Cbig-data-science",
}

websites = {
    "nofluffjobs": NOFLUFFJOBS,
    "bulldogjob": BULLDOGJOB,
    "theprotocol": THEPROTOCOL,
    "rocketjobs": ROCKETJOBS,
    "justjoin": JUSTJOINIT,
    "solid": SOLIDJOBS,
    "pracuj": PRACUJPL,
}


def identify_website(search_link: str) -> str:
    """
    Set current website based on search link
    """
    # Iterate over the website_map to find the matching website
    for key, website in websites.items():
        if key in search_link:
            return website
    return "Error: Website not recognized"
