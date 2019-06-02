developers = {
	"LyfeOnEdge" : {
		"gravatar_url" : "http://de.gravatar.com/lyfeonedge.json",
		"project_page_url" : "https://discord.gg/cXtmY9M",
		"dev_flavor_text" : "In Soviet Russia, switch hack you.\nColorblind.\n←Join my discord for dragons"
	},

	"pprmint" : {
		"gravatar_url" : "http://de.gravatar.com/npprmint.json",
		"project_page_url" : "npprmint.github.io",
		"dev_flavor_text" : "UI concept and asset designer.\n\n←Click here to visit his website"
	}

}

GAME = "game"
TOOL = "tool"
RECOMENDED = "recomended"
TITLEINSTALLER = "title installer"
EMULATOR = "emulator"

softwarelist = [
	{
	"software" : "Homebrew Store",
	"githubapi" : "https://api.github.com/repos/vgmoose/hb-appstore/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://github.com/vgmoose/hb-appstore/releases",
	"description" : "A graphical frontend to the get package manager for downloading and managing homebrew on video game consoles, such as the Nintendo Switch and Wii U. This is a replacement to the older Wii U Homebrew App Store.",
	"group" : RECOMENDED,
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software": "Edizon",
	"githubapi": "https://api.github.com/repos/WerWolv/EdiZon/releases",
	"github_asset" : None, 
	"author": "WerWolv",	
	"projectpage": "https://github.com/WerWolv/EdiZon",
	"description": """EdiZon consists of 3 different main functionalities. 
Save file management. Extraction of game saves.
	Injection of extracted game saves (Your own and your friends save files).
	Uploading of savefiles directly to https://transfer.sh.
	Batch extraction of all save files of all games on the system.
Save file editing
	Easy to use, scriptable and easily expandable on-console save editing.
		Lua and Python script support.
	Built-in save editor updater.
On-the-fly memory editing
	Cheat Engine like RAM editing.
	Freezing of values in RAM via Atmosphère's cheat module.
	Interface for loading, managing and updating Atmosphère cheats.
	
	All packed into one easy to use and easy to install Homebrew.""",
	"group": RECOMENDED,
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software": "Lockpick",
	"githubapi": "https://api.github.com/repos/shchmue/Lockpick/releases",
	"github_asset": None,
	"author": "shchmue",
	"projectpage": "https://github.com/shchmue/Lockpick/",
	"description": """Lockpick is a ground-up C++17 rewrite of homebrew key derivation software, namely kezplez-nx. It also dumps titlekeys. This will dump all keys through *_key_05 on firmwares below 6.2.0 and through *_key_06 on 6.2.0.

Due to key generation changes introduced in 7.0.0, Lockpick is not able to dump keys ending in 07 at all. Furthermore, unfortunately the public method to dump tsec_root_key is only available on firmware 6.2.0 so 7.x consoles can only dump through keys ending in 05.""",
	"group": RECOMENDED,
	"install_subfolder": "switch",
	"zip_items": None,
	},



	{
	"software": "2048",
	"githubapi" : "https://api.github.com/repos/FlagBrew/2048/releases",
	"github_asset" : None, 
	"author" : "FlagBrew", 
	"projectpage": "https://gbatemp.net/threads/release-2048-port-for-switch-homebrew.501678/",
	"description" : "2048 port for Switch Homebrew",
	"group" : GAME,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	# {
	# "software" : "Calculator-NX",
	# "githubapi" : "https://api.github.com/repos/thomleg50/Calculator-NX/releases",
	# "github_asset" : None, 
	# "author" : "None",
	# "projectpage": "https://github.com/thomleg50/Calculator-NX/",
	# "description" : "A simple calculator for Switch !",
	# "group" : TOOL,
	# "install_subfolder": "switch",
	# "zip_items": None,
	# },


	{
	"software" : "Gag-Order",
	"githubapi" : "https://api.github.com/repos/Adubbz/Gag-Order/releases",
	"github_asset" : None, 
	"author" : "Adubbz", 
	"projectpage": "https://github.com/Adubbz/Gag-Order/",
	"description" : "A homebrew application which patches the 'Supernag' on the Nintendo Switch.",
	"group" : TOOL,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software" : "JKS's Save Manager",
	"githubapi" : "https://api.github.com/repos/J-D-K/JKSV/releases",
	"github_asset" : None, 
	"author" : "J-D-K", 
	"projectpage": "https://gbatemp.net/threads/release-jks-savemanager-homebrew-cia-save-manager.413143/",
	"description": """WIP Save manager for the Switch, JKSV on Switch started as a small project/port to test some things and get familiar with libnx. A list of what it currently can do:

Dump and restore save data.
	This includes the ability to dump and restore to/from any location on SD by pressing minus and using the Advanced Mode.
Dump system save data
	Pressing all four shoulder buttons at once will rescan and include the previously unlisted system saves.
	Dumping this data is allowed, but writing back is not.
Open and explore bis storage partitions via the Extras menu
	BIS Storage is opened inside a basic filebrowser. The partition's listing is on the left. Your SD is on the right.
	Only copying to SD and file properties work on BIS partitions. Writing to and deleting are disabled for now.
Misc Extras:
	NAND Dumping
	Ability to remove downloaded firmware updates from NAND.
	Terminating processes by ID. Allowing you to dump normally unopenable system archives.
	Mount by System Save ID. Normally used when the terminated process makes JKSV unable to rescan titles without the Switch crashing.""",
	"group": TOOL,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software" : "NX-Shell",
	"githubapi" : "https://api.github.com/repos/joel16/NX-Shell/releases",
	"github_asset" : None, 
	"author" : "joel16",
	"projectpage": "https://gbatemp.net/threads/nx-shell-multipurpose-file-manager-for-nintendo-switch.505332/",
	"description": "Work in progress port of 3DShell (Multi purpose file manager) to the Nintendo Switch.",
 	"group": TOOL,
	"install_subfolder": "NX-Shell",
	"zip_items": None,
	},


	{
	"software": "NxThemesInstaller",
	"githubapi": "https://api.github.com/repos/exelix11/SwitchThemeInjector/releases",
	"github_asset" : None, 
	"author" : "exelix11", 
	"projectpage": "https://gbatemp.net/download/nxthemes-installer.35408/",
	"description": """The Switch theme injector project is composed of three parts:

Switch theme injector (Windows app): An app to create and edit custom themes
NXThemes installer: An homebrew app that runs on the switch itself and can be used to install and manage themes.
Switch theme injector online (also called WebInjector): A port of the windows injector as a web app, it lacks some features like image to DDS conversion.
The main objective is to develop a complete toolset to create and install custom themes on the switch. As the console os doesn't implement custom themes natively most of this is done by patching system SZS files to get the desidered aspect.

Unfortunately SZS files from the switch os contain copyrighted data so to make theme sharing legal the nxtheme format has been developed, it's 100% legal and works on every firmware, unless you're dealing with making your own patches and custom layouts you should only use nxtheme files.""",
	"group": TOOL,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software": "pPlay Video Player",
	"githubapi": "https://api.github.com/repos/Cpasjuste/pplay/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/pplay-switch-video-player.526187/",
	"description" : "pPlay is a video player for the Nintendo Switch. pPlay support most popular video formats, have subtitles (embedded ass) and http streaming support.",
	"group" : TOOL,
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software": "SwitchIdent (Command Line Interface)",
	"githubapi": "https://api.github.com/repos/joel16/SwitchIdent/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/switchident.504134/",
	"description": "This is yet another identity tool that is continuing the series of <device name here>ident. This tool allows users to get various bits of information from your Nintendo Switch device, hence the name 'ident' as in identifying your Nintendo Switch.",
	"group": TOOL,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software": "SwitchIdent (GUI)",
	"githubapi": "https://api.github.com/repos/joel16/SwitchIdent/releases",
	"github_asset" : 1, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/switchident.504134/",
	"description": "This is yet another identity tool that is continuing the series of <device name here>ident. This tool allows users to get various bits of information from your Nintendo Switch device, hence the name 'ident' as in identifying your Nintendo Switch.",
	"group": TOOL,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software":  "Checkpoint",
	"githubapi": "https://api.github.com/repos/FlagBrew/Checkpoint/releases",
	"github_asset" : 2, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/checkpoint-save-manager-released-for-nintendo-switch.503370/",
	"description": "A fast and simple homebrew save manager for 3DS and Switch written in C++.",
	"group": TOOL,
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software": "VBA Next",
	"githubapi": "https://api.github.com/repos/RSDuck/vba-next-switch/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/vba-next-for-switch-works-4-1.504947/",
	"description" :  """A VBA-M port for Nintendo Switch. It's based of the libretro port(the actual emulator) and 3DSGBA(the GUI, although heavily refactored).

After porting 3DSGBA(which often crashed probably because of a huge amount of memory leaks), I tried porting mGBA which ran not so well. That's why I decided to experiment with a lighter less accurate emulator, which lead to this port.""",
	"group" : EMULATOR,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software" : "Duke Nukem 3D",
	"githubapi" : "https://api.github.com/repos/Cpasjuste/eduke32/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/duke-nukem-3d.502386/",
	"description" : "EDuke32 is an awesome, free homebrew game engine and source port of the classic PC first person shooter Duke Nukem 3D",
	"group" : GAME,
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software" : "InvadersNX",
	"githubapi" : "https://api.github.com/repos/MaesterRowen/InvadersNX/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/homebrew-space-game-nx.493643/",
	"description" : """This is a port of a space invaders type game I wrote for the Xbox 360 homebrew scene. Initially, I was going to remove the Xbox 360 specific artwork, but then figured it sort of made sense to have the xbox boss be an "Invader" on the Nintendo Switch.

The project has always been a learning project so I hope others can get use out of the source code and are able to improve upon or learn from it.

Known Bugs: There appears to be some bug that causes the screen to flicker during transitions. I am not sure if that's a VSYNC issue with SDL2/libnx or something I am doing incorrectly.""",
	"group" : GAME,
	"install_subfolder": "switch",
	"zip_items": None,
	},


	{
	"software" : "Ken's Labyrinth",
	"githubapi" : "https://api.github.com/repos/sacredbanana/lab3d-sdl/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/kens-labyrinth-enhanced-port-for-nintendo-switch.529434/",
	"description" : "Classic MS-DOS shooter with enhanced features such as HD textures and 60fps support",
	"group" : GAME,
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software" : "Meritous",
	"githubapi" : "https://api.github.com/repos/Nop90-Switch/Meritous-Switch/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/release-meritous-for-switch.498356/",
	"description" : "Top View Dungeon Game",
	"group" : GAME,
	"install_subfolder": None,
	"zip_items": None,
	},
	
	
	{
	"software" : "Incognito",
	"githubapi" : "https://api.github.com/repos/blawar/incognito/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/incognito.531924/",
	"description" : "Wipes personal information from your Nintendo Switch by removing it from prodinfo.",
	"group" : "tool, REINX ONLY",
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software" : "PyNX",
	"githubapi" : "https://api.github.com/repos/nx-python/PyNX/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/nx-python-create-python-homebrew-for-the-switch.499150/",
	"description" : """nx-python is an ecosystem for developing and running Python homebrew applications on the Nintendo Switch. PyNX serves as the entry point to running Python apps on your Switch. It is a homebrew app that contains a port of the CPython interpreter and allows you to run Python applications from the Homebrew Menu. Just name your application main.py and place it next to the PyNX.nro, and it will be executed as soon as you launch PyNX from the Homebrew Menu. Currently, Python 3.5 is supported.""",
	"group" : TOOL,
	"install_subfolder": "switch",
	"zip_items": None,
	},


]


customfirmwarelist = [
	{
		"software" : "Atmos",
		"githubapi" : "https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases",
		"github_asset" : "",
		"author" : None,
		"projectpage": "https://github.com/Atmosphere-NX/Atmosphere/releases",
		"description": "Atmosphère is a customized firmware for the Nintendo Switch.",
		"group": "CFW",
		"install_subfolder": None,
		"zip_items": None,
		"pattern" : [["atmosphere"],".zip"]
	},

	{
	 	"software" : "Kosmos",
		"githubapi" : "https://api.github.com/repos/AtlasNX/Kosmos/releases",
		"github_asset" : None, 
		"author" : None,
		"projectpage": "https://github.com/AtlasNX/Kosmos/releases",
		"description" : "All-in-One CFW Package for the Nintendo Switch - previously SDFilesSwitch",
		"group" : "CFW",
		"install_subfolder": None,
		"zip_items": None,
		"pattern" : [["kosmos", "sdfiles"],".zip"]
	},

	{
		"software" : "ReiNX",
		"githubapi" : "https://api.github.com/repos/Reisyukaku/ReiNX/releases",
		"github_asset" : None, 
		"author" : None, 
		"projectpage": "https://github.com/Reisyukaku/ReiNX",
		"description" : "A modular Switch custom firmware",
		"group" : "CFW",
		"install_subfolder": None,
		"content_type"
		"zip_items": None,
		"pattern" : [["reinx"],".zip"]
	},

	{
		"software" : "Argon-NX SD Files",
		"githubapi" : "https://api.github.com/repos/Guillem96/argon-nx/releases",
		"github_asset" : 1, 
		"author" : "Guillem96", 
		"projectpage": "https://github.com/Guillem96/argon-nx/",
		"description" : """
What Argon is?
	Argon is a noble gas. "Argon" comes from Greek "Argon", neuter of "argos" meaning lazy , idle or inactive. Argon recieved this name because of its chemical inactivity.

	Argon NX is an immutable payload which is injected to your Nintendo Switch via Fusee Gelee exploit.

Purpose
	The purpose of Argon NX is to stay immutable, so you can always inject it, without caring about other payloads getting updated (Always use ArgonNX for TegraSmash, TegraGUI, TrinkedM0...).

How can it be immutable?
	When Argon NX is injected, it automatically launches the payload.bin locacted at argon directory on your SD Card root.

	If payload.bin is not present or VOLUME DOWN button is pressed on payload injection, Argon NX will list all payloads located at argon/payloads, and you will be able to select one of them to launch it.
""",
		"group" : "CFW",

		"install_subfolder": None,
		"content_type"
		"zip_items": None,
		"pattern" : [["sd-files"], ".zip"]
	},
]


nxpythonlist = [
	{
	"software" : "Generic Mod Manager",
	"githubapi" : "https://api.github.com/repos/Genwald/Generic-Mod-Manager/releases",
	"github_asset" : 1, 
	"author" : "Genwald", 
	"projectpage": "https://gbatemp.net/threads/generic-mod-manager-a-mod-manager.517626/",
	"description" : """Generic Mod Manager is a simple mod manager written in python, for use with the homebrew PyNX. 
It lets you easily activate and deactivate mods as well as handle conflicting mod files. Its mods folder and layeredFS folder can be set in the ModManager.ini in order to support multiple cfw's and user preferences.""",
	"group" : TOOL,
	"install_subfolder": "switch\\PyNX",
	"zip_items": None,
	},

]
	






#Payloads
payloadlist = [
	{
	"software": "Hekete",
	"githubapi": "https://api.github.com/repos/CTCaer/hekate/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/rcm-payload-hekate-ctcaer-mod.502604/",
	"description": """Custom Nintendo Switch bootloader, firmware patcher, and more.
This version supports booting ALL current OS/CS CFW, Linux chainloading and payload tools.
No more SD card removals""",
	"group": "PAYLOADS",
	"install_subfolder": None,
	"zip_items": "hekate_ctcaer",
	},


	{
	"software": "fusee-primary",
	"githubapi": "https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases",
	"github_asset" : 1, 
	"author" : None, 
	"projectpage": "https://github.com/Atmosphere-NX/Atmosphere/tree/master/fusee/fusee-primary",
	"description" : "Bootloader for Atmosphere",
	"group" : "PAYLOADS",
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software" : "Argon-NX payload",
	"githubapi" : "https://api.github.com/repos/Guillem96/argon-nx/releases",
	"github_asset" : 0, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/argon-nx-payload-chainloader.527178/",
	"description": """
What Argon is?
	Argon is a noble gas. "Argon" comes from Greek "Argon", neuter of "argos" meaning lazy , idle or inactive. Argon recieved this name because of its chemical inactivity.

	Argon NX is an immutable payload which is injected to your Nintendo Switch via Fusee Gelee exploit.

Purpose
	The purpose of Argon NX is to stay immutable, so you can always inject it, without caring about other payloads getting updated (Always use ArgonNX for TegraSmash, TegraGUI, TrinkedM0...).

How can it be immutable?
	When Argon NX is injected, it automatically launches the payload.bin locacted at argon directory on your SD Card root.

	If payload.bin is not present or VOLUME DOWN button is pressed on payload injection, Argon NX will list all payloads located at argon/payloads, and you will be able to select one of them to launch it.
""",
	"group" : "PAYLOADS",
	"install_subfolder": None,
	"zip_items": None,
	},


	{
	"software" : "Lockpick RCM",
	"githubapi" : "https://api.github.com/repos/shchmue/Lockpick_RCM/releases",
	"github_asset" : None, 
	"author" : None, 
	"projectpage": "https://gbatemp.net/threads/lockpick-switch-key-derivation-homebrew.525575/",
	"description": """Lockpick_RCM is a bare metal Nintendo Switch payload that derives encryption keys for use in Switch file handling software like hactool, hactoolnet/LibHac, ChoiDujour, etc. without booting Horizon OS.

Due to changes imposed by firmware 7.0.0, Lockpick homebrew can no longer derive the latest keys. In the boot-time environment however, there are fewer limitations.""",
	"group" : "PAYLOADS",
	"install_subfolder": None,
	"zip_items": None,
	},


]
	


# 	},
# #other switch content
# 	{
# 	"software": "sigpatches",
# 	"githubapi": None, #yet, added this at last moment, will be dynamic next version
# 	"projectpage": "https://gbatemp.net/threads/i-heard-that-you-guys-need-some-sweet-patches-for-atmosphere.521164/",
# 	"directlink": "https://github.com/AtlasNX/Kosmos/releases/download/v11.11.1/Additional.SigPatches.espatches.zip",
	
	
# 	"asset" : 0,
# 	"author": None,
# 	"image" : "https://avatars1.githubusercontent.com/u/205276?s=400&v=4",
# 	"description":"""Ok, Here you are
# and No, they are just IPS patches, they don't contain anything illegal

# es patches are Rajkosto ones, Credits goes to him

# FAQ:
# Q: What are patches?
# A: Patches are modifications in firmware that changes it's default behavior, usually using for disabling/bypassing some checks

# Q: What do these patches do?
# A:
# 1- Running custom (unsigned, modified) nsps(ncas) such as homebrew nsps and converted xcis to nsps (nosigchk+acid, fs)
# 2- Installing fake (unsigned, modified) tickets (es)
# 3- nocmac, fs""",
# 	"group": "Patches",
# 	},


payloadinjector = [
	{
	"software" : "fusee-launcher",
	"githubapi" : "https://api.github.com/repos/Cease-and-DeSwitch/fusee-launcher/releases",
	"github_asset" : "tarball_url", 
	"author" : "Qyriad", 
	"projectpage": None,
	"description" : "",
	"group" : "SPECIAL",
	"install_subfolder": None,
	"zip_items": None,
	},
]


nutserverdict = {
	"software" : "Nut Server",
	"githubapi" : "https://api.github.com/repos/blawar/nut/releases",
	"author" : "blawar", 
	"projectpage": "https://gbatemp.net/threads/nut.515530/",
	"description" : "Nut server for installing title backups",
	"group" : "SPECIAL",
	"dependencies" : [
		"colorama", 
		"pyopenssl", 
		"requests", 
		"tqdm", 
		"unidecode", 
		"image", 
		"bs4", 
		"urllib3", 
		"flask", 
		"pyqt5"
		]
	}

fluffydict = {
	"software" : "Fluffy",
	"githubapi" : "https://api.github.com/repos/fourminute/Fluffy/releases",
	"author" : "Fluffy", 
	"projectpage": "https://gbatemp.net/threads/fluffy-a-tinfoil-and-goldleaf-gui.528930/",
	"description" : "Fluffy server for installing title backups",
	"group" : "SPECIAL",
	"dependencies" : [
		"pyusb",
		"pyqt5",
		"libusb",
		"libusb1",
		"qdarkstyle",
		"configparser"
		]
	}

