from modules.data_collector import search_all_sites

records = search_all_sites()

record = records[0][0]

print(record.website)
print(record.remote_status)
