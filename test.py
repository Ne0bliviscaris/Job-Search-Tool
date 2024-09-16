from modules.data_collector import search_all_sites

records = search_all_sites()
print(records[0][0].html.prettify())
