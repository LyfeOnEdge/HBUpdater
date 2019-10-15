import os, json
from .updater import updater_object
#get parent directory of parent directory
parent_parent = os.path.dirname(os.path.dirname(__file__))

downloader_config = os.path.join(parent_parent, "updater_settings.json")

with open(downloader_config, encoding="utf-8") as json_file:
    downloader_config = json.load(json_file)

updater = updater_object(downloader_config["UPDATENAME"], downloader_config["UPDATEURL"], downloader_config["ASSETPATTERN"],)