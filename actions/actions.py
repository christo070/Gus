# https://rasa.com/docs/rasa/custom-actions

import json, os
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset, ConversationPaused, UserUtteranceReverted

dirname = os.path.dirname(__file__)

RESERVATION_FILE = os.path.join(dirname, "../info/table_reservation.json")
MENU_FILE = os.path.join(dirname, "../info/menu.json")
ORDER_FILE = os.path.join(dirname, "../info/order.json")



class ActionHumanHandoff(Action):
    def name(self):
        return "action_human_handoff"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        # dispatcher.utter_message("I am passing you to a human...")
        # call_customer_service(tracker)
        # return [ConversationPaused(), UserUtteranceReverted()]

        dispatcher.utter_message(response="utter_human_handoff")
        return []
    
    
# -------------------------------------
# Action involved in Table Reservation
# -------------------------------------

class ActionCheckAvailability(Action):
    def name(self) -> Text:
        return "action_check_table_availability"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        with open(RESERVATION_FILE, "r") as f:
            json_object = json.load(f)
            tables = json_object["tables"]
            people_count = int(tracker.get_slot("people_count") or 0)

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

        with open(RESERVATION_FILE, "r") as fr:
            json_object = json.load(fr)
            tables = json_object["tables"]

            people_count = int(tracker.get_slot("people_count") or 0)
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

            with open(RESERVATION_FILE, "w") as fw:
                json.dump(json_object, fw)

            dispatcher.utter_message(response="utter_table_reservation_successful")

            return [SlotSet("is_reserved", True)]

        return [FollowupAction("utter_table_reservation_unsuccessful")]
    

# --------------------------------------
# Actions involved in taking Food Order 
# --------------------------------------





class ActionShowSelectedItems(Action):
    def name(self):
        return "action_show_selected_food_items"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        message = "Here is your order summary:"
        for item in tracker.get_slot("selected_items"):
            message += f"\nItem: {item['name']}\nCategory: {item['category']}\nQuantity: {item['quantity']}\n"
        dispatcher.utter_message(message)
        return []

class ActionSendOrder(Action):
    def name(self):
        return "action_send_food_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        with open(ORDER_FILE, "r") as fr:
            json_object = json.load(fr)
            with open(ORDER_FILE, "w") as fw:
                d = {}
                d[tracker.get_slot("table")] = tracker.get_slot("selected_items")
                json_object.append(d)
                json.dump(json_object, fw)

        dispatcher.utter_message(response="utter_order_confirmed")
        return []
    
class ActionCancelOrder(Action):
    def name(self):
        return "action_cancel_food_order"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        
        dispatcher.utter_message(response="utter_order_cancelled")
        return [SlotSet("selected_items", None)]

class ActionAddToSelectedItems(Action):
    def name(self):
        return "action_add_to_selected_food_items"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        item = {}
        item["name"] = tracker.get_slot("food_item")
        item["category"] = tracker.get_slot("food_category")
        item["quantity"] = tracker.get_slot("food_quantity")

        selected = tracker.get_slot("selected_items") or []
        selected.append(item)

        return [SlotSet("selected_items", selected)]
    
class ActionResetOrderForm(Action):
    def name(self):
        return "action_reset_food_order_form_slots"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        return [SlotSet("food_item", None), SlotSet("food_category", None), SlotSet("food_quantity", None)]