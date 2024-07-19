from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import mysql.connector as mc


class ActionSaveData(Action):
    def name(self) -> Text:
        return "ActionSaveData"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        name = tracker.get_slot("name")
        snnum = tracker.get_slot("snnum")
        contact = tracker.get_slot("contact")

        if not name or not snnum or not contact:
            dispatcher.utter_message(response="utter_incomplete_data")
            return []

        try:
            print("1")
            db = mc.connect(
                host="localhost",
                user="root",
                password="",
                database="chatbotrasadb"
            )
            cur = db.cursor()
            insert_query = "INSERT INTO posreqs (name, snnum, contact) VALUES (%s, %s, %s)"
            data = (name, snnum, contact)
            cur.execute(insert_query, data)
            db.commit()
            db.close()
            print("2")
        except Exception as e:
            print("General error:", e)

        dispatcher.utter_message(response="utter_snteidugaar_avah_Complete")
        return []
