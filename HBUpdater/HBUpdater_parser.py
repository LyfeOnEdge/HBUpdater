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

        self.package_dict = {}

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
                for package in self.all:
                    if not "package" in package.keys():
                        package["package"] = package["name"]
                    if not "license" in package.keys():
                        package["license"] = "N/A"
                    if not package["category"] in self.category_blacklist:
                        new_all.append(package)
                    self.map[package["category"]].append(package)

                    self.package_dict[package["package"]] = package

                self.all = new_all
                self.sorted = True

    def get_package(self, package):
        return self.package_dict[package]

    def get_latest_version(self, package):
        return self.get_package(package)["github_content"][0]["tag_name"]
