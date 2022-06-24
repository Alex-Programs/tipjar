import json
import os.path
import time
from secrets import token_hex


class DatabaseManager():
    def __init__(self):
        self.tip_list = self.load_tips_from_file()
        self.dumped_cache = None

    def load_tips_from_file(self):
        if not os.path.isfile("tips.json"):
            with open("tips.json", "w") as f:
                f.write(json.dumps({
                    "categories": [
                        {
                            "name": "F-14 Tomcat",
                            "image": "F14.png",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                        },
                        {
                            "name": "AC-130",
                            "image": "AC130.png",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                        },
                        {
                            "name": "Two seat fixed wing",
                            "image": "Multiseat.png",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                        },
                        {
                            "name": "Thrust Vectoring",
                            "image": "thrustvectoring.png",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                        },
                        {
                            "name": "Air Traffic Control",
                            "image": "ATC.png",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                        },
                        {
                            "name": "A-10 Thunderbolt II",
                            "image": "A-10.png",
                            "description": "A10 bEsT cAs AiRcRaFt",
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                        },
                        {
                            "name": "Quest 2 Standalone",
                            "image": "q2.png",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": False,
                        } # TO ADD A NEW AIRCRAFT CHANGE THIS AND MODIFY tips.json
                    ],
                }, indent=4))

        with open("tips.json") as f:
            return json.loads(f.read())

    def basic_category_list(self):
        for category in self.tip_list["categories"]:
            yield category["name"]

    def dump_tips_to_file(self):
        with open("tips.json", "w") as f:
            f.write(json.dumps(self.tip_list, indent=4))

    def add_new_tip(self, messageid, text, category):
        found = False
        for i in self.tip_list["categories"]:
            if i["name"] == category:
                i["tips"].append(
                    {"uid": self.gen_random_id(), "messageid": messageid, "text": text, "time": time.time()})

                i["count"] = i["count"] + 1

                found = True
                break

        if not found:
            return False

        self.dump_tips_to_file()

        self.dumped_cache = None

        return True

    def messageid_exists(self, messageid):
        for category in self.tip_list["categories"]:
            for tip in category["tips"]:
                if str(tip["messageid"]) == str(messageid):
                    return True

        return False

    def tip_list_to_json_cached(self):
        if not self.dumped_cache:
            text = json.dumps(self.tip_list)
            self.dumped_cache = text
            return text

        return self.dumped_cache

    def gen_random_id(self):
        return token_hex(32)


if __name__ == "__main__":
    db = DatabaseManager()
