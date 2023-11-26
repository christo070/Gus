# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import json
# import ijson

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import (
    SlotSet,
    FollowupAction
)

# try:
#     with open('../data/info/table_reservation.json', 'r') as f:
#         table_reservation = ijson.items(f, 'table_reservation.item')
#         reservation_details = table_reservation["details"]
#         tables = table_reservation["tables"]
        
# except Exception as e:
#     print(e)
#     reservation = {}

#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

class ActionCheckAvailability(Action):

    def name(self) -> Text:
        return "action_check_table_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        available_tables = {}

        with open('../data/info/table_reservation.json', 'r') as f:
                json_object = json.load(f)
                tables = json_object["tables"]

                for table_id in tables.keys():
                    if tables[table_id]["status"] == "available" and tables[table_id]["capacity"] >= tracker.get_slot("people_count"):
                        available_tables[table_id] = tables[table_id]["capacity"]

        if len(available_tables) == 0:
            return [SlotSet("availability", False)]
        else:
            return [SlotSet("availability", True), SlotSet("available_tables", available_tables)]
    
class ActionReserveTable(Action):

    def name(self) -> Text:
        return "action_reserve_table"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # find the smallest possible table which can hold given number of people 
        available_tables = tracker.get_slot("available_tables")
        m = min(available_tables.values())
        table = ""
        for k,v in available_tables:
            if v == m:
                table = k
                break

        # assign table to customer
        if table:
            with open('../data/info/table_reservation.json', 'r') as f:
                json_object = json.load(f)
                
                json_object["details"].append(
                    {
                        "customer_email": tracker.get_slot("customer_email"),
                        "table": table,
                        "people_count": tracker.get_slot("people_count")
                    }
                )

                json_object["tables"][table]["status"] = "reserved"

                with open('../data/info/table_reservation.json', 'w') as f:
                    json.dump(json_object, f)
        else:
            dispatcher.utter_message(text="Error while reserving table. Please try again later.")
            return [FollowupAction("action_abort_reservation_process")]

        dispatcher.utter_message(text="Table reserved successfully!")
        return []

        
class ActionAbortReservation(Action):

    def name(self) -> Text:
        return "action_abort_reservation_process"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        return [SlotSet("availability", None), SlotSet("available_tables", {}), SlotSet("people_count", None)]