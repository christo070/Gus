# https://rasa.com/docs/rasa/custom-actions

import json, os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset, ConversationPaused, UserUtteranceReverted

dirname = os.path.dirname(__file__)
table_reservation_file = os.path.join(dirname, "info\\table_reservation.json")


class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_table_availability"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        with open(table_reservation_file, "r") as f:
            json_object = json.load(f)
            tables = json_object["tables"]
            people_count = int(tracker.get_slot("people_count"))

            for table_id in tables.keys():
                if (tables[table_id]["available"] == True) and (
                    tables[table_id]["capacity"] >= people_count
                ):
                    return [SlotSet("is_table_available", True)]

        return [SlotSet("is_table_available", False)]


class ActionReserveTable(Action):
    def name(self) -> Text:
        return "action_reserve_table"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        is_table_available = tracker.get_slot("is_table_available")
        if is_table_available == False:
            dispatcher.utter_message(response="utter_reservation_housefull")
            return []

        if tracker.get_slot("is_reserved") == True:
            dispatcher.utter_message(response="utter_table_already_reserved")
            return []

        with open(table_reservation_file, "r") as f:
            json_object = json.load(f)
            tables = json_object["tables"]

            people_count = int(tracker.get_slot("people_count"))
            modifyed = False

            for table_id in tables.keys():
                if (tables[table_id]["available"] == True) and (
                    tables[table_id]["capacity"] >= people_count
                ):
                    json_object["details"].append(
                        {
                            "customer_email": tracker.get_slot("customer_email"),
                            "table": table_id,
                            "people_count": people_count,
                        }
                    )
                    json_object["tables"][table_id]["available"] = False
                    modifyed = True
                    break

            if modifyed == False:
                return [FollowupAction("utter_table_reservation_unsuccessful")]

            with open(table_reservation_file, "w") as f:
                json.dump(json_object, f)

            dispatcher.utter_message(response="utter_table_reservation_successful")

            return [SlotSet("is_reserved", True)]


class ActionReset(Action):
    def name(self) -> Text:
        return "action_reset_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        return [AllSlotsReset()]


from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import UserUtteranceReverted
from rasa_sdk.executor import CollectingDispatcher

class ActionDefaultFallback(Action):
    def name(self) -> Text:
        return "action_default_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # https://rasa.com/docs/rasa/fallback-handoff/#4-defining-an-ultimate-fallback-action
        # dispatcher.utter_message(text="I am passing you to a human...")
        # call_customer_service(tracker)     
        # return [ConversationPaused(), UserUtteranceReverted()]

        dispatcher.utter_message(response="utter_default")
        return [UserUtteranceReverted()]

# Action Class with name 'action_human_handoff' for handoff to human
class ActionHumanHandoff(Action):
    def name(self):
        return "action_human_handoff"

    def run(self, dispatcher, tracker, domain):
        # dispatcher.utter_message("I am passing you to a human...")
        # call_customer_service(tracker)
        # return [ConversationPaused(), UserUtteranceReverted()]

        dispatcher.utter_message(response="utter_human_handoff")
        return [UserUtteranceReverted()]
