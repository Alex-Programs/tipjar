import json
import os.path
import time
from secrets import token_hex


class DatabaseManager():
    def __init__(self):
        self.tip_list = self.load_tips_from_file()
        self.dumped_cache = None
        self.regenerate_counts()

    def regenerate_counts(self):
        broken = False

        for category in self.tip_list["categories"]:
            count = 0
            for tip in category["tips"]:
                count += 1

            if category["count"] != count:
                category["count"] = count
                broken = True

        if broken:
            self.dump_tips_to_file()

    def load_tips_from_file(self):
        if not os.path.isfile("tips.json"):
            with open("tips.json", "w") as f:
                f.write(json.dumps({
                    "categories": [
                        {
                            "name": "F-14 Tomcat",
                            "image": "F14.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["F14", "F-14", "Tomcat"],
                        },
                        {
                            "name": "AC-130",
                            "image": "AC130.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["AC130", "C130", "AC-130", "Gunship"],
                        },
                        {
                            "name": "Two seat fixed wing",
                            "image": "Multiseat.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["Two seat", "Back seat", "Multi seat", "Rear seat", "Dual seat", "Multiseat"],
                        },
                        {
                            "name": "Misc. New Aircraft",
                            "image": "newaircraft.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["New aircraft", "Next aircraft", "Next plane", "new Plane"],
                        },
                        {
                            "name": "Air Traffic Control",
                            "image": "ATC.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["ATC", "traffic control", "JTAC"]
                        },
                        {
                            "name": "A-10 Thunderbolt II",
                            "image": "A-10.webp",
                            "description": "A10 bEsT cAs AiRcRaFt",
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["A10", "A-10", "GAU-8", "brrrr", "rrrt", "10C", "CAS aircraft"],
                        },
                        {
                            "name": "Quest 2 Standalone",
                            "image": "q2.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": False,
                            "keywords": ["Quest 2", "standalone", "oculus", "store", "native"]
                        },
                        {
                            "name": "Electronic Warfare",
                            "image": "EWAR.webp",
                            "description": None,
                            "count": 0,
                            "tips": [],
                            "circleCrop": True,
                            "keywords": ["EWAR", "electronic warfare", "EW", "jamming", "growler"]
                        }# TO ADD A NEW AIRCRAFT CHANGE THIS AND MODIFY tips.json AND MODIFY submit.html
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

    def add_new_tip(self, messageid, text, category, fulllink, ip):
        found = False
        for i in self.tip_list["categories"]:
            if i["name"] == category:
                i["tips"].append(
                    {"uid": self.gen_random_id(), "messageid": messageid, "text": text, "time": time.time(), "link": fulllink})

                i["count"] = i["count"] + 1

                found = True
                break

        if not found:
            return False

        self.dump_tips_to_file()

        self.dumped_cache = None

        with open("ip-easy-to-clear-list.txt", "a") as f:
            f.write(str(ip) + " @@@@@@ " + str(text) + "\n")

        return True

    def messageid_exists(self, messageid):
        for category in self.tip_list["categories"]:
            for tip in category["tips"]:
                if str(tip["messageid"]) == str(messageid):
                    return True

        return False

    def remove_by_id(self, uid):
        for category in self.tip_list["categories"]:
            for tip in category["tips"]:
                if str(tip["uid"]).strip() == str(uid).strip():
                    category["tips"].remove(tip)
                    category["count"] = category["count"] - 1

                    self.dump_tips_to_file()
                    self.dumped_cache = None
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
