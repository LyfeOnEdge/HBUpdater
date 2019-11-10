import os, sys, json
from shutil import copyfile

PARENT_PARENT = os.path.dirname(os.path.dirname(__file__))
SETTINGS_FILE = os.path.join(PARENT_PARENT, "settings.json")
DEFAULT_SETTINGS_FILE = os.path.join(PARENT_PARENT, "settings_default.json")

if not os.path.isfile(SETTINGS_FILE):
	copyfile(DEFAULT_SETTINGS_FILE, SETTINGS_FILE)

class settingsTool():
	def __init__(self):
		self.settings = None
		self.file = None
		self.load(SETTINGS_FILE)

	def load(self, file):
		with open(file) as f:
			self.settings = json.load(f)
			self.file = file

	def save(self):
		with open(self.file, mode = "w+") as f:
			json.dump(self.settings, f, indent = 4)
		print("saved settings: {}".format(json.dumps(self.settings, indent = 4)))

	def get_setting(self, key):
		return self.settings.get(key)

	def set_setting(self, key, value):
		self.settings[key] = value