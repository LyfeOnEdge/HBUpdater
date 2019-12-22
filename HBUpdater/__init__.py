from .HBUpdater_parser import parser
from .HBUpdater import HBUpdater_handler
store_handler = HBUpdater_handler("SWITCH")
local_packages_handler = HBUpdater_handler("GENERIC")
repo_parser = parser()