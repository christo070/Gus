# This file is exclusively for testing purposes. It is not used in the actual bot.

import json, os

dirname = os.path.dirname(__file__)
table_reservation_file = os.path.join(dirname, "..\\info\\table_reservation.json")


def table_reservation_reset():
    with open(table_reservation_file, "r") as f:
        json_object = json.load(f)
        tables = json_object["tables"]

        json_object["details"] = []

        for table_id in tables.keys():
            if tables[table_id]["available"] == False:
                json_object["tables"][table_id]["available"] = True

        with open(table_reservation_file, "w") as f:
            json.dump(json_object, f)


table_reservation_reset()
