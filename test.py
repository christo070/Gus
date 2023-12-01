import json

available_tables = {} 
with open('/home/christos/Projects/Gus/data/info/table_reservation.json', 'r') as f:
    json_object = json.load(f)
    tables = json_object["tables"]
    for table_id in tables.keys():
        if tables[table_id]["status"] == "available" and tables[table_id]["capacity"] >= 5:
            available_tables[table_id] = tables[table_id]["capacity"]


m = min(available_tables.values())
print(available_tables, m)
table = ""
for k,v in available_tables.items():
    print(k,v)
    if v == m:
        table = k
        print("here")
        break

print(f"table -> {table}")

count = 5
email = "john@gmail.com"

# assign table to customer
if table != "":
    with open('/home/christos/Projects/Gus/data/info/table_reservation.json', 'r') as f:
        json_object = json.load(f)
        json_object["details"].append(
            {
                "customer_email": email,
                "table": table,
                "people_count": count
            }
        )
        json_object["tables"][table]["status"] = "reserved"
        with open('../data/info/table_reservation.json', 'w') as f:
            json.dump(json_object, f)

        print("Success")
else:
    print("Failure")