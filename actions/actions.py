# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import ijson

try:
    with open('../data/info/table_reservation.json', 'r') as f:
        reservation = ijson.items(f, 'table_reservation.item')
except Exception as e:
    print(e)
    reservation = {}

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
        return "action_check_availability"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        with open('../data/info/table_reservation.json', 'r') as f:
            table_reservation = ijson.items(f, 'table_reservation.item')

            for item in table_reservation:
                print(item)
        dispatcher.utter_message(text="Hello World!")

        return []
