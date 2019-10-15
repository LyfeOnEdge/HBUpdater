import json

class parser(object):
    def __init__(self):
        self.sorted = False
        self.all = []
        self.homebrew = []
        self.emulators = []
        self.games = []
        self.media = []
        self.tools = []
        self.nxpythonlist = []
        self.customfirmwarelist = []
        self.payloadlist = []

        self.category_blacklist = []

        self.map = {
            "homebrew" : self.homebrew,
            "emulators" : self.emulators,
            "games" : self.games,
            "media" : self.media,
            "python" : self.nxpythonlist,
            "cfw" : self.customfirmwarelist,
            "payloads" : self.payloadlist,
        }

        self.list_list = [ self.all ]
        for key in self.map:
            self.list_list.append(self.map[key])

    def blacklist_categories(self, categories):
        self.category_blacklist = categories

    def clear(self):
        for lis in self.list_list:
            lis = []

    #Loads HBUpdater json as a large list of dicts
    def load(self, hbupdater_json):
        self.clear()
        try:
            with open(hbupdater_json, encoding="utf-8") as repojson:
                self.all = json.load(repojson)
            self.sort()
        except Exception as e:
            print("Exception loading HBUpdater json %s" % e)
        print("Found %s software entries" % len(self.all))

    #sorts list into smaller chunks
    def sort(self):
        if not self.sorted:
            if self.all:
                new_all = []
                for genre in self.all.keys():
                    for software in self.all[genre]:
                        repo_keys = software.keys()
                        if not "store_equivalent" in repo_keys:
                            software["store_equivalent"] = software["name"]
                        if not "license" in repo_keys:
                            software["license"] = "N/A"

                        if not genre in self.category_blacklist:
                            new_all.append(software)
                        self.map[genre].append(software)
                self.all = new_all
                self.sorted = True