# This file is exclusively for testing purposes. It is not used in the actual bot.

import json, os

dirname = os.path.dirname(__file__)
RESERVATION_FILE = os.path.join(dirname, "../info/reservation.json")
MENU_FILE = os.path.join(dirname, "../info/menu.json")
ORDER_FILE = os.path.join(dirname, "../info/order.json")

FOOD_CATEGORY = ["Appetizers", "Main Course", "Desserts", "Beverages"]

def table_reservation_reset():
    with open(RESERVATION_FILE, "r") as f:
        json_object = json.load(f)
        tables = json_object["tables"]

        json_object["details"] = []

        for table_id in tables.keys():
            if tables[table_id]["available"] == False:
                json_object["tables"][table_id]["available"] = True

        with open(RESERVATION_FILE, "w") as f:
            json.dump(json_object, f)


def readmenu():
    with open(MENU_FILE, "r") as f:
        json_object = json.load(f)
        for item in json_object:
            print((item["name"]).lower())

# table_reservation_reset()
# readmenu()


# category = "Appetizers"
# message = f"Please select the item you want to order from {category}:"
# i = 1
# with open(MENU_FILE, "r") as f:
#     json_object = json.load(f)
#     for item in json_object:
#         if item["category"] == category:
#             message += f"\n{i}. {item['name']}"
#             i += 1

# print(message)