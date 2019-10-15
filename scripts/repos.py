GAME = "game"
TOOL = "tool"
EMULATOR = "emu"
POC = "proof-of-concept"

APACHE2 = "Apache License 2.0"
GPL3 = "GPL3"
GPL2 = "GPL2"
MIT = "MIT"
BSD2 = "BSD v2"
NA = "n/a"

SUBFOLDER_SWITCH = "switch"

SAVE_TOOL = "save tool"

template = {
    "name" : None,
    "store_equivalent" : None,
    "githubapi" : None,
    "author" : None,
    "projectpage": None,
    "description" : None,
    "group" : None,
    "install_subfolder": None,
    "pattern" : [[],],
    "license" : None,
    "tags" : []
}

homebrewlist = [
    {
    "name" : "Homebrew Store",
    "store_equivalent" : "appstore",
    "githubapi" : "https://api.github.com/repos/vgmoose/hb-appstore/releases", 
    "author" : "vgmoose", 
    "projectpage": "https://github.com/vgmoose/hb-appstore/releases",
    "description" : "A graphical frontend to the get package manager for downloading and managing homebrew on video game consoles, such as the Nintendo Switch and Wii U. This is a replacement to the older Wii U Homebrew App Store.",
    "group" : TOOL,
    "install_subfolder": "switch/appstore",
    "pattern" : [['appstore'],".nro"],
    "license" : GPL3
    },


    {
    "name": "Edizon",
    "store_equivalent" : "Edizon",
    "githubapi": "https://api.github.com/repos/WerWolv/EdiZon/releases",
    "author": "WerWolv",    
    "projectpage": "https://github.com/WerWolv/EdiZon",
    "description": """EdiZon consists of 3 different main functionalities. 

#Save file management. Extraction of game saves.
 - Injection of extracted game saves (Your own and your friends save files).
 - Uploading of savefiles directly to https://transfer.sh.
 - Batch extraction of all save files of all games on the system.

#Save file editing
 - Easy to use, scriptable and easily expandable on-console save editing.
   - Lua and Python script support.
 - Built-in save editor updater.

#On-the-fly memory editing
 - Cheat Engine like RAM editing.
 - Freezing of values in RAM via Atmosphère's cheat module.
 - Interface for loading, managing and updating Atmosphère cheats.
    
All packed into one easy to use and easy to install Homebrew.""",
    "group": "save manager",
    "install_subfolder": None,
    "pattern" : [["SD"], ".zip"],
    "license" : GPL2,
    "tags" : [SAVE_TOOL]
    },


    {
    "name": "Lockpick",
    "githubapi": "https://api.github.com/repos/shchmue/Lockpick/releases",
    "author": "shchmue",
    "projectpage": "https://github.com/shchmue/Lockpick/",
    "description": """Lockpick is a ground-up C++17 rewrite of homebrew key derivation software, namely kezplez-nx. It also dumps titlekeys. This will dump all keys through *_key_05 on firmwares below 6.2.0 and through *_key_06 on 6.2.0.

Due to key generation changes introduced in 7.0.0, Lockpick is not able to dump keys ending in 07 at all. Furthermore, unfortunately the public method to dump tsec_root_key is only available on firmware 6.2.0 so 7.x consoles can only dump through keys ending in 05.""",
    "group": TOOL,
    "install_subfolder": "switch",
    "pattern" : [["Lockpick"], ".nro"],
    "license" : GPL2
    },

    {
    "name" : "Gag-Order",
    "store_equivalent" : "gagorder",
    "githubapi" : "https://api.github.com/repos/Adubbz/Gag-Order/releases",
     
    "author" : "Adubbz", 
    "projectpage": "https://github.com/Adubbz/Gag-Order/",
    "description" : "A homebrew application which patches the 'Supernag' on the Nintendo Switch.",
    "group" : TOOL,
    "install_subfolder": "switch",
    "pattern" : [["gag-order"],".nro"],
    "license" : NA
    },


    {
    "name" : "JKSV",
    "store_equivalent" : "jksv",
    "githubapi" : "https://api.github.com/repos/J-D-K/JKSV/releases",
    "author" : "J-D-K", 
    "projectpage": "https://gbatemp.net/threads/release-jks-savemanager-homebrew-cia-save-manager.413143/",
    "description": """WIP Save manager for the Switch, JKSV on Switch started as a small project/port to test some things and get familiar with libnx. A list of what it currently can do:

#Dump and restore save data.
 - This includes the ability to dump and restore to/from any location on SD by pressing minus and using the Advanced Mode.

#Dump system save data
 - Pressing all four shoulder buttons at once will rescan and include the previously unlisted system saves.
 - Dumping this data is allowed, but writing back is not.

#Open and explore bis storage partitions via the Extras menu
 - BIS Storage is opened inside a basic filebrowser. The partition's listing is on the left. Your SD is on the right.
 - Only copying to SD and file properties work on BIS partitions. Writing to and deleting are disabled for now.

#Misc Extras:
 - NAND Dumping
 - Ability to remove downloaded firmware updates from NAND.
 - Terminating processes by ID. Allowing you to dump normally unopenable system archives.
 - Mount by System Save ID. Normally used when the terminated process makes JKSV unable to rescan titles without the Switch crashing.""",
    "group": "save manager",
    "install_subfolder": "switch",
    "pattern" : [["JKSV"], ".nro"],
    "license" : GPL2
    },


    {
    "name" : "NX-Shell",
    "store_equivalent" : "NX-shell",
    "githubapi" : "https://api.github.com/repos/joel16/NX-Shell/releases",
    "author" : "joel16",
    "projectpage": "https://gbatemp.net/threads/nx-shell-multipurpose-file-manager-for-nintendo-switch.505332/",
    "description": "Work in progress port of 3DShell (Multi purpose file manager) to the Nintendo Switch.",
    "group": TOOL,
    "install_subfolder": "switch/NX-Shell",
    "pattern" : [["NX-Shell"], ".nro"],
    "license" : GPL3
    },


    {
    "name": "NxThemesInstaller",
    "store_equivalent" : "NXthemes_Installer",
    "githubapi": "https://api.github.com/repos/exelix11/SwitchThemeInjector/releases",
     
    "author" : "exelix11", 
    "projectpage": "https://gbatemp.net/download/nxthemes-installer.35408/",
    "description": """The Switch theme injector project is composed of three parts:

 - Switch theme injector (Windows app): An app to create and edit custom themes

 - NXThemes installer: An homebrew app that runs on the switch itself and can be used to install and manage themes.

 - Switch theme injector online (also called WebInjector): A port of the windows injector as a web app, it lacks some features like image to DDS conversion.

The main objective is to develop a complete toolset to create and install custom themes on the switch. As the console os doesn't implement custom themes natively most of this is done by patching system SZS files to get the desidered aspect.

Unfortunately SZS files from the switch os contain copyrighted data so to make theme sharing legal the nxtheme format has been developed, it's 100% legal and works on every firmware, unless you're dealing with making your own patches and custom layouts you should only use nxtheme files.""",
    "group": TOOL,
    "install_subfolder": "switch/NXthemes_Installer",
    "pattern" : [["NxThemesInstaller"],".nro"],
    "license" : NA
    },

    {
    "name": "SwitchIdent Console",
    "store_equivalent" : "switchident-console",
    "githubapi": "https://api.github.com/repos/joel16/SwitchIdent/releases",
    "author" : "joel16", 
    "projectpage": "https://gbatemp.net/threads/switchident.504134/",
    "description": "This is yet another identity tool that is continuing the series of <device name here>ident. This tool allows users to get various bits of information from your Nintendo Switch device, hence the name 'ident' as in identifying your Nintendo Switch.",
    "group": TOOL,
    "install_subfolder": "switch",
    "pattern" : [["SwitchIdent_Console"], ".nro"],
    "license" : GPL3
    },


    {
    "name": "SwitchIdent (GUI)",
    "store_equivalent" : "switchident-GUI",
    "githubapi": "https://api.github.com/repos/joel16/SwitchIdent/releases",
    "author" : "joel16", 
    "projectpage": "https://gbatemp.net/threads/switchident.504134/",
    "description": "This is yet another identity tool that is continuing the series of <device name here>ident. This tool allows users to get various bits of information from your Nintendo Switch device, hence the name 'ident' as in identifying your Nintendo Switch.",
    "group": TOOL,
    "install_subfolder": "switch",
    "pattern" : [["SwitchIdent_GUI"], ".nro"],
    "license" : GPL3
    },


    {
    "name":  "Checkpoint",
    "store_equivalent" : "Checkpoint",
    "githubapi": "https://api.github.com/repos/FlagBrew/Checkpoint/releases",
    "author" : "FlagBrew", 
    "projectpage": "https://gbatemp.net/threads/checkpoint-save-manager-released-for-nintendo-switch.503370/",
    "description": "A fast and simple homebrew save manager for 3DS and Switch written in C++.",
    "group": "save manager",
    "install_subfolder": "switch/Checkpoint",
    "pattern" : [["Checkpoint"], ".nro"],
    "license" : GPL3,
    "tags" : [SAVE_TOOL]
    },

    {
    "name" : "PyNX",
    "store_equivalent" : "pynx",
    "githubapi" : "https://api.github.com/repos/nx-python/PyNX/releases",
    "author" : "elnardu", 
    "projectpage": "https://gbatemp.net/threads/nx-python-create-python-homebrew-for-the-switch.499150/",
    "description" : """nx-python is an ecosystem for developing and running Python homebrew applications on the Nintendo Switch. 

PyNX serves as the entry point to running Python apps on your Switch. It is a homebrew app that contains a port of the CPython interpreter and allows you to run Python applications from the Homebrew Menu. Just name your application main.py and place it next to the PyNX.nro, and it will be executed as soon as you launch PyNX from the Homebrew Menu. Currently, Python 3.5 is supported.""",
    "group" : "interpreter",
    "install_subfolder": "switch",
    "pattern" : [["PyNX"],".zip"],
    "license" : "ISC License"
    },

    #Temporailly unavailable
    # {
    # "name": "sdsetup-switch",
    # "store_equivalent" : "Homebrew_SD_Setup",
    # "githubapi" : "https://api.github.com/repos/noahc3/sdsetup-switch/releases",
    # "author" : "noahc3", 
    # "projectpage": "https://gbatemp.net/threads/guide-sdsetup-com-the-official-guide-for-sdfilesswitch-and-sdsetup.518641/",
    # "description" : "This app allows you to access and download packages from www.sdsetup.com right on your Switch, no PC required! Many homebrews and CFWs can be updated without ever taking out your SD card.",
    # "group" : TOOL,
    # "install_subfolder": "switch/Homebrew_SD_Setup",
    # "pattern" : [["sdsetup-switch"], ".nro"],
    # "license" : NA
    # },


    {
    "name": "ftpd",
    "store_equivalent" : "ftpd",
    "githubapi" : "https://api.github.com/repos/mtheall/ftpd/releases",
    "author" : "mtheall, TuxSH", 
    "projectpage": "https://github.com/mtheall/ftpd/",
    "description" : "FTP Server for Switch",
    "group" : TOOL,
    "install_subfolder": "switch",
    "pattern" : [["ftpd"], ".nro"],
    "license" : "Public Domain"
    },

    {
    "name" : "Brainfuck Interpreter",
    "store_equivalent" : "brainfuck",
    "githubapi" : "https://api.github.com/repos/TheKgg/switch-brainfuck/releases",
    "author" : "TheKgg", 
    "projectpage": "https://github.com/TheKgg/switch-brainfuck/releases",
    "description" : """A brainfuck interpreter for the Nintendo Switch

#Usage
 - Put a .bf file with code (only code, no comments) in either the root of your emulator's SD card or in the same folder as your .nro. It will be booted on start.
 
 - When it asks for input move the left joystick to select a number.

#Compiling
 - Just install devkitPro using this guide, replace the source folder in your new project with the source folder here, and run make build in the same folder as the Makefile.""",
    "group" : "interpreter",
    "install_subfolder": "switch/brainfuck",
    "pattern" : [["Brainfuck_Interpreter"], ".nro"],
    },

    {
    "name" : "Argon-NX SD Files",
    "store_equivalent" : "argon-nx",
    "githubapi" : "https://api.github.com/repos/Guillem96/argon-nx/releases",
    "author" : "Guillem96", 
    "projectpage": "https://github.com/Guillem96/argon-nx/",
    "description" : """#What Argon is?
 - Argon is a noble gas. "Argon" comes from Greek "Argon", neuter of "argos" meaning lazy , idle or inactive. Argon recieved this name because of its chemical inactivity.

 - Argon NX is an immutable payload which is injected to your Nintendo Switch via Fusee Gelee exploit.

#Purpose
 - The purpose of Argon NX is to stay immutable, so you can always inject it, without caring about other payloads getting updated (Always use ArgonNX for TegraSmash, TegraGUI, TrinkedM0...).

#How can it be immutable?
 - When Argon NX is injected, it automatically launches the payload.bin locacted at argon directory on your SD Card root.

 - If payload.bin is not present or VOLUME DOWN button is pressed on payload injection, Argon NX will list all payloads located at argon/payloads, and you will be able to select one of them to launch it.
""",
    "group" : "loader",
    "install_subfolder": None,
    "pattern" : [["sd-files", "argon-nx"], ".zip"]
    },

    {
    "name": "Hekate",
    "githubapi": "https://api.github.com/repos/CTCaer/hekate/releases",
    "store_equivalent" : "Hekate",
    "author" : "CTCaer", 
    "projectpage": "https://gbatemp.net/threads/rcm-payload-hekate-ctcaer-mod.502604/",
    "description": """Custom Nintendo Switch bootloader, firmware patcher, and more.
This version supports booting ALL current OS/CS CFW, Linux chainloading and payload tools.
No more SD card removals""",
    "group": "loader",
    "install_subfolder": None,
    "pattern" : [["hekate_ctcaer"], ".zip"]
    },

    # {
    # "name": "Hekate Joonie86",
    # "githubapi": "https://api.github.com/repos/Joonie86/hekate/releases",
    # "store_equivalent" : "Hekate_Joonie86",
    # "author" : "CTCaer, Joonie86",
    # "projectpage": "https://gbatemp.net/threads/rcm-payload-hekate-ctcaer-mod.502604/",
    # "description": """Fork of Hekate with Joonie Patches""",
    # "group": "loader",
    # "install_subfolder": None,
    # "pattern" : [["Kosmos_patches"], ".7z"]
    # },

    {
    "name": "Homebrew Menu",
    "githubapi": "https://api.github.com/repos/switchbrew/nx-hbmenu/releases",
    "store_equivalent" : "hbmenu",
    "author" : "yellows8, plutoo", 
    "projectpage": "https://github.com/switchbrew/nx-hbmenu/",
    "description": """Allows you to launch homebrew apps, hold 'r' and open the photo album to launch""",
    "group": TOOL,
    "install_subfolder": "",
    "pattern" : [["nx-hbmenu"], ".zip"]
    },

    {
    "name": "Apollo",
    "githubapi": "https://api.github.com/repos/evo-brut3/Apollo/releases",
    "store_equivalent" : "Apollo",
    "author" : "evo-brut3", 
    "projectpage": "https://gbatemp.net/threads/apollo-file-explorer-for-nintendo-switch.543080/",
    "description": """Apollo is a File Explorer Homebrew for the Nintendo Switch. Its goal is to be the most convenient and reliable method to manage console's files.

Apollo's current features are:
-Graphical User Interface: Minimalist design which is based on default hbmenu and official home menu esthetic.
-Selecting items: A simple but mandatory feature.
-Copying files and directories: Before doing so, application checks whether user is trying to overwrite currently existing files or directories and then asks about overwriting them.
-Recursive directory deletion: It allows for complete deletion of directories' content and obviously for file deletion.
-Renaming files and directories: Speaks for itself.
-Sorting items: Alphabetically or reversed.

Credits:
devkitPro for providing toolchain.
XorTroll for the amazing Plutonium which allowed Apollo to look like this and the Goldleaf which is a mine of knowledge.
GilFerraz for his beautiful Miiverse UI concept which inspired me to create sidebar.
Lucas Lacerda for his Nintendo Switch UI Concept.
jaames for the nx-hbmenu mockup which helped me with the design.
Nintendo for security <3.
""",
    "group": TOOL,
    "install_subfolder": "switch/Apollo",
    "pattern" : [["Apollo"], ".nro"]
    },


    {
    "name" : "fakenews-injector",
    "store_equivalent" : "fakenews-injector",
    "githubapi" : "https://api.github.com/repos/noahc3/fakenews-injector/releases",
    "author" : "noahc3",
    "projectpage": "https://switch.homebrew.guide/hacking/nereba/pegascape",
    "description" : """Simple homebrew to inject the "Fake News" save data for an easy browser entry point on Switch.

Kills BCAT, so reboot is required after use.

Tested on 1.0.0, 3.0.0, 4.0.1 and 4.1.0, works both in CFW and with hbl launched via PegaSwitch/PegaScape.""",
    "group" : TOOL,
    "install_subfolder": "switch",
    "pattern" : [["fakenews-injector"],".nro"],
    "license" : GPL3
    },

    {
    "name" : "nxdumptool",
    "store_equivalent" : "gcdumptool",
    "githubapi" : "https://api.github.com/repos/DarkMatterCore/nxdumptool/releases",
    "author" : "DarkMatterCore",
    "projectpage": "https://gbatemp.net/threads/nxdumptool-nintendo-switch-dump-tool.508343/",
    "description" : """Nintendo Switch Game Card Dump Tool
Main features:
- Generates full Cartridge Image dumps (XCI) with optional certificate removal and optional trimming.
- Generates installable Nintendo Submission Packages (NSP) from base applications, updates and DLCs stored in the inserted game card.
- Compatible with multigame carts.
- CRC32 checksum calculation for XCI/NSP dumps.
- Full XCI dump verification using XML database from NSWDB.COM (NSWreleases.xml).XML database and in-app update via libcurl.
- Precise HFS0 raw partition dumping, using the root HFS0 header from the game card.
- HFS0 partition file data dumping.
- HFS0 partition file browser with manual file dump support.
- RomFS section file data dumping.
- RomFS section file browser with manual file dump support.
- Manual game card certificate dump.
- Free SD card space checks in place.
- File splitting support for all operations.
- Game card metadata retrieval using NCM and NS services.
- Dump speed calculation, ETA calculation and progress bar.
Compatibility:
- Doesn't work under 1.0.0, and probably never will. The application needs some IPC calls that are only available from 2.0.0 onwards.
- Doesn't work under FW > 1.0.0 and < 4.0.0 if the application is launched using PegaSwitch. This is because PegaSwitch doesn't give full access permissions to the application. This is a known bug that's being looked into.
- Works under SX OS v1.2 and later, but only is your Switch is on FW > 1.0.0.
- When used with the inserted gamecard, the NSP dumping, ExeFS dumping/browsing and RomFS dumping/browsing capabilities depend entirely on the FW version the console is on. This is because the SPL services are used to decrypt the NCA key area directly without deriving for key area encryption keys. If the console is not updated to a FW version that supports the crypto/keyslot used by the inserted gamecard, these features will fail.
- NSP dumping, ExeFS dumping/browsing and RomFS dumping/browsing capabilities for installed SD/eMMC require the "sdmc:/switch/prod.keys" file. Likewise, update NSP dumping from gamecards requires this file to be available. Use Lockpick_RCM to generate it.
- If you go back to Horizon and get an error or black screen when trying to launch the inserted gamecard, just pull it out and re-insert it. No reboot needed. Any help on fixing this bug will be greatly appreciated.
""",
    "group" : TOOL,
    "install_subfolder": "switch/gcdumptool",
    "pattern" : [["nxdumptool"],".nro"],
    "license" : GPL2
    },

    {
    "name" : "sys-audioplayer",
    "store_equivalent" : "sys-audioplayer",
    "githubapi" : "https://api.github.com/repos/KranKRival/sys-audioplayer/releases",
    "author" : "KranKRival",
    "projectpage": "https://github.com/KranKRival/sys-audioplayer",
    "description" : """sys-audioplayer updated for official firmware 9
This is a WIP background-audio-player as a custom Boot2 sysmodule for the Nintendo Switch.

instructions:
this is developed for Atmosphere/Kosmos , Not tested on other CFW

Compiled Module Goes to /atmosphere/titles/4200000000000000/exefs.nsp
flag the Module activated by making blank file /atmosphere/titles/4200000000000000/flags/boot2.flag
add your songs (MP3 ONLY) to /music Directory on Root of your Sd Card
enable the module nor by restart console, or using latest Kosmos ToolBox.
Note:
Music will start playing as soon as the module is Activated
this is a beta version and the songs repeat 100 times by default / for future Repeat song Implementation !!!
right now it just plays all the mp3s in the /music folder of your sdcard once the switch boots.""",
    "group" : TOOL,
    "install_subfolder": None,
    "pattern" : [["Sys_AudioPlayer"],".zip"],
    "license" : GPL3,
    "tags" : [TOOL]
    },

    {
    "name" : "JoyConMouse",
    "store_equivalent" : "JoyConMouse",
    "githubapi" : "https://api.github.com/repos/KranKRival/JoyConMouse/releases",
    "author" : "KranKRival",
    "projectpage": "https://github.com/KranKRival/JoyConMouse",
    "description" : "this is a proof of concept of a mouse created with sdl2 and controlled by the left analog stick of the joycon there's button added to determine the button press",
    "group" : POC,
    "install_subfolder": SUBFOLDER_SWITCH,
    "pattern" : [["JoyConMousePOC"],".zip"],
    "license" : APACHE2,
    "tags" : [POC, APACHE2],
    },
]

emulist = [
    {
    "name": "VBA Next",
    "store_equivalent" : "VBA_NEXT",
    "githubapi": "https://api.github.com/repos/RSDuck/vba-next-switch/releases",
    "author" : "RSDuck", 
    "projectpage": "https://gbatemp.net/threads/vba-next-for-switch-works-4-1.504947/",
    "description" :  """A VBA-M port for Nintendo Switch. It's based of the libretro port(the actual emulator) and 3DSGBA(the GUI, although heavily refactored).

After porting 3DSGBA(which often crashed probably because of a huge amount of memory leaks), I tried porting mGBA which ran not so well. That's why I decided to experiment with a lighter less accurate emulator, which lead to this port.""",
    "group" : EMULATOR,
    "install_subfolder": "switch/VBA_NEXT",
    "pattern" : [["vba-next"],".zip"],
    "license" : GPL2,
    },

    {
    "name": "CHIP8-NX",
    "store_equivalent" : "CHIP8",
    "githubapi" : "https://api.github.com/repos/Marice/CHIP8-NX/releases",
    "author" : "Marice", 
    "projectpage": "https://github.com/Marice/CHIP8-NX",
    "description" : "A working early stage CHIP8 emulator for the Nintendo Switch.\\n\\nFeel free to help and improve the code!\\n\\nExit to HBmenu using PLUS button",
    "group" : EMULATOR,
    "install_subfolder": None,
    "pattern" : [["CHIP8-NX"], ".zip"],
    "license" : "Copyright"
    },

    {
    "name": "uae4all2",
    "store_equivalent" : "uae4all2",
    "githubapi" : "https://api.github.com/repos/rsn8887/uae4all2/releases",
    "author" : "rsn8887", 
    "projectpage": "https://github.com/rsn8887/uae4all2/",
    "description" : "A fast and optimized Amiga Emulator",
    "group" : EMULATOR,
    "install_subfolder": "switch",
    "pattern" : [["uae4all2"], "switch.zip"],
    "license" : GPL2
    },

    {
    "name": "pFBA: final burn alpha",
    "store_equivalent" : "pFBA",
    "githubapi" : "https://api.github.com/repos/Cpasjuste/pemu/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://github.com/Cpasjuste/pemu",
    "description" : "final burn alpha emulator",
    "group" : EMULATOR,
    "install_subfolder": "switch/pfba",
    "pattern" : [["pfba"], "switch.zip"],
    "license" : NA
    },

    {
    "name": "pNES",
    "store_equivalent" : "pNES",
    "githubapi" : "https://api.github.com/repos/Cpasjuste/pemu/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://github.com/Cpasjuste/pemu",
    "description" : "Portable NES Emulator",
    "group" : EMULATOR,
    "install_subfolder": "switch/pnes",
    "pattern" : [["pnes"], "switch.zip"],
    "license" : NA
    },

    {
    "name": "pSNES",
    "store_equivalent" : "psnes",
    "githubapi" : "https://api.github.com/repos/Cpasjuste/pemu/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://github.com/Cpasjuste/pemu",
    "description" : "Portable NES Emulator",
    "group" : EMULATOR,
    "install_subfolder": "switch/psnes",
    "pattern" : [["psnes"], "switch.zip"],
    "license" : NA
    },

    {
    "name": "OpenBor",
    "store_equivalent" : "openbor",
    "githubapi" : "https://api.github.com/repos/Cpasjuste/openbor/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://github.com/Cpasjuste/openbor",
    "description" : "OpenBOR is the ultimate 2D gaming engine with over 10+ years of active development behind it. With OpenBOR you can build anything from simple button mashers to elaborate projects rivaling the most lavish professional offerings. Download one of the dozens of ready to play game modules available here, or grab the development kit and start up one of your own!\\n\\n\\nPut your *.pak files in a Paks folder, inside OpenBOR.nro directory.\\n\\nOpenBOR official website: http://www.chronocrash.com/forum/",
    "group" : EMULATOR,
    "install_subfolder": "switch/openbor",
    "pattern" : [["OpenBOR"], ".nro"],
    "license" : NA
    },

    {
    "name": "ScummVM",
    "store_equivalent" : "scummvm",
    "githubapi" : "https://api.github.com/repos/Cpasjuste/scummvm/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://github.com/Cpasjuste/scummvm/",
    "description" : "Here is a port of the excellent ScummVM engine to the switch.\\n\\nKNOW BUGS\\nno sfx in some scumm engine games (curse of monkey island, full throttle) ! :(\\nintro in the secret of monkey island CD version hang, audio play fine and can be skipped. Other versions seems to works fine.\\nmp3 decoder doesn't seems to work (crash), but this format should not be used anyway.",
    "group" : EMULATOR,
    "install_subfolder": "switch",
    "pattern" : [["scummvm_switch"], ".zip"],
    "license" : NA
    },

    {
    "name": "NoiES",
    "store_equivalent" : "noies",
    "githubapi" : "https://api.github.com/repos/Hydr8gon/NoiES/releases",
    "author" : "Hydr8gon", 
    "projectpage": "https://github.com/Hydr8gon/NoiES",
    "description" : "A noice NES emulator",
    "group" : EMULATOR,
    "install_subfolder": None,
    "pattern" : [["noies"], "switch.zip"],
    "license" : GPL3
    },

    {
    "name": "melonDS",
    "store_equivalent" : "melonDS",
    "githubapi" : "https://api.github.com/repos/Hydr8gon/melonDS/releases",
    "author" : "Hydr8gon", 
    "projectpage": "https://github.com/Hydr8gon/melonDS/",
    "description" : "DS emulator",
    "group" : EMULATOR,
    "install_subfolder": None,
    "pattern" : [["melonds"], ".zip"],
    "license" : GPL3
    },

    {
    "name": "DeSmuME-NX",
    "store_equivalent" : "desmume",
    "githubapi" : "https://api.github.com/repos/Laproxi/DeSmuME-NX/releases",
    "author" : "Laproxi", 
    "projectpage": "https://github.com/Laproxi/DeSmuME-NX",
    "description" : "Play DS roms! (in sd:/switch/desmume/roms)",
    "group" : EMULATOR,
    "install_subfolder": "switch/desmume",
    "pattern" : [["DeSmuME-NX"], ".nro"],
    "license" : GPL2
    },
]





#GAMES

gameslist = [
    {
    "name" : "Meritous",
    "store_equivalent" : "meritous",
    "githubapi" : "https://api.github.com/repos/Nop90-Switch/Meritous-Switch/releases",
    "author" : "Lancer-X, nop90", 
    "projectpage": "https://gbatemp.net/threads/release-meritous-for-switch.498356/",
    "description" : "Top View Dungeon Game",
    "group" : GAME,
    "install_subfolder": None,
    "pattern" : [["Meritous"], ".zip"],
    "license" : NA
    },

    {
    "name" : "eduke32",
    "store_equivalent" : "eduke32",
    "githubapi" : "https://api.github.com/repos/Cpasjuste/eduke32/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://gbatemp.net/threads/duke-nukem-3d.502386/",
    "description" : "EDuke32 is an awesome, free homebrew game engine and source port of the classic PC first person shooter Duke Nukem 3D",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["eduke32"], ".zip"],
    "license" : GPL2
    },


    {
    "name" : "InvadersNX",
    "store_equivalent" : "InvadersNX",
    "githubapi" : "https://api.github.com/repos/MaesterRowen/InvadersNX/releases",
    "author" : "MaesterRowen", 
    "projectpage": "https://gbatemp.net/threads/homebrew-space-game-nx.493643/",
    "description" : """This is a port of a space invaders type game I wrote for the Xbox 360 homebrew scene. Initially, I was going to remove the Xbox 360 specific artwork, but then figured it sort of made sense to have the xbox boss be an "Invader" on the Nintendo Switch.

The project has always been a learning project so I hope others can get use out of the source code and are able to improve upon or learn from it.

Known Bugs: There appears to be some bug that causes the screen to flicker during transitions. I am not sure if that's a VSYNC issue with SDL2/libnx or something I am doing incorrectly.""",
    "group" : GAME,
    "install_subfolder": "switch/InvadersNX",
    "pattern" : [["InvadersNX"], ".nro"],
    "license" : NA
    },


    {
    "name" : "Ken's Labyrinth",
    "store_equivalent" : "Kens-Labyrinth",
    "githubapi" : "https://api.github.com/repos/sacredbanana/lab3d-sdl/releases", 
    "author" : "sacredbanana", 
    "projectpage": "https://gbatemp.net/threads/kens-labyrinth-enhanced-port-for-nintendo-switch.529434/",
    "description" : "Classic MS-DOS shooter with enhanced features such as HD textures and 60fps support",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["Kens-Labyrinth"], ".zip"],
    "license" : NA
    },

    {
    "name": "2048",
    "store_equivalent" : "2048",
    "githubapi" : "https://api.github.com/repos/BernardoGiordano/2048/releases",
    "author" : "BernardoGiordano", 
    "projectpage": "https://gbatemp.net/threads/release-2048-port-for-switch-homebrew.501678/",
    "description" : "2048 port for Switch Homebrew",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["2048"], ".nro"],
    "license" : NA
    },

    {
    "name": "OpenLara",
    "store_equivalent" : "Openlara",
    "githubapi" : "https://api.github.com/repos/XProger/OpenLara/releases",
    "author" : "XProger", 
    "projectpage": "https://github.com/XProger/OpenLara",
    "description" : "Classic Tomb Raider open-source engine",
    "group" : GAME,
    "install_subfolder": "switch/OpenLara",
    "pattern" : [["OpenLara_switch"], ".zip"],
    "license" : BSD2
    },

    {
    "name": "TicTacToeNX",
    "store_equivalent" : "TicTacToeNX",
    "githubapi" : "https://api.github.com/repos/lorrdfarquad/TikTacToeNX/releases",
    "author" : "lorrdfarquad", 
    "projectpage": "https://github.com/lorrdfarquad/TikTacToeNX",
    "description" : "My version of tic tac toe ported to the nintendo switch.",
    "group" : GAME,
    "install_subfolder": "switch/TicTacToeNX",
    "pattern" : [["TicTacToeNx"], ".nro"],
    "license" : NA
    },

    {
    "name" : "Super Mario War NX",
    "store_equivalent" : "supermariowar-nx",
    "githubapi" : "https://api.github.com/repos/retronx-team/supermariowar-nx/releases",
    "author" : "p-sam",
    "projectpage": "https://github.com/p-sam/supermariowar-nx/releases",
    "description" : """Super Mario War is, quoting the main project, a fan-made multiplayer Super Mario Bros. style deathmatch game. You can find more information about the game itself and its history on the main readme.

This uses:

the devkitA64 toolchain, libnx and multiple portlibs from devkitpro
a subrepo of supermariowar with switch specific changes
Usage
Download the latest release, and extract the archive in the /switch folder on your SD Card. Then, run the game from the hbmenu using hbl.

Todo
networking""",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["smw"],".zip"],
    "license" : "n/a",
    },


    {
    "name" : "MarioBrosNX",
    "store_equivalent" : "MarioBrosNX",
    "githubapi" : "https://api.github.com/repos/KranKRival/MarioBrosNX/releases",
    "author" : "KranKRival",
    "projectpage": "https://gbatemp.net/threads/mariobrosnx-super-mario-bros-clone-for-the-nintendo-switch.546623/",
    "description" : """MarioBrosNX C++/SDL2, Created by Łukasz Jakowski 2014, Ported to the Nintendo Switch By Krank/KuranKu 2019
All ingame images and sound belong to its authors and none other, the right for mario bros title belongs to nintendo. 
this game created for fun and love of the community.""",
    "group" : GAME,
    "install_subfolder": None,
    "pattern" : [["MarioBrosNX"],".zip"],
    "license" : GPL2
    },


    {
    "name" : "OpenJazzNX",
    "store_equivalent" : "OpenJazzNX",
    "githubapi" : "https://api.github.com/repos/KranKRival/OpenJazzNX/releases",
    "author" : "KranKRival",
    "projectpage": "https://github.com/KranKRival/OpenJazzNX/",
    "description" : "Port of OpenJazz to the nintendo switch With SDL2 Support.",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["OpenJazzNX"],".zip"],
    "license" : GPL2
    },

    {
    "name" : "BomberManNX",
    "store_equivalent" : "BomberManNX",
    "githubapi" : "https://api.github.com/repos/KranKRival/BomberManNX/releases",
    "author" : "KranKRival",
    "projectpage": "https://gbatemp.net/threads/bombermannx-classic-bomberman-clone-for-the-nintendo-switch.549187/",
    "description" : """BomberManNX
Clone of Bomberman game in C++ using SDL2 for the nintendo switch

Authors:
* Aleksandar Miletic / developer
* Mirko Brkusanin / developer
* KranK / Port to the nintendo switch
Original Game
https://github.com/Sandman1705/Bombermaniac""",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["BomberManNX"],".zip"],
    "license" : MIT,
    "tags" : [GAME]
    },

    {
    "name" : "PacManNX",
    "store_equivalent" : "PacManNX",
    "githubapi" : "https://api.github.com/repos/KranKRival/PacManNX/releases",
    "author" : "KranKRival",
    "projectpage": "https://github.com/KranKRival/PacManNX",
    "description" : "A Clone of original PacMan For The Nintendo Switch made in C++ using SDL2",
    "group" : GAME,
    "install_subfolder": "switch",
    "pattern" : [["PacManNX"],".zip"],
    "license" : GPL2,
    "tags" : [GAME]
    },
]


nxpythonlist = [
    {
    "name" : "Generic Mod Manager",
    "githubapi" : "https://api.github.com/repos/Genwald/Generic-Mod-Manager/releases",
    "author" : "Genwald", 
    "projectpage": "https://gbatemp.net/threads/generic-mod-manager-a-mod-manager.517626/",
    "description" : """Generic Mod Manager is a simple mod manager written in python, for use with the homebrew PyNX. 
It lets you easily activate and deactivate mods as well as handle conflicting mod files. Its mods folder and layeredFS folder can be set in the ModManager.ini in order to support multiple cfw's and user preferences.""",
    "group" : TOOL,
    "install_subfolder": "switch\\PyNX",
    "pattern" : [["Generic-Mod-Manager"],".py"],
    },

    {
    "name" : "timefix",
    "store_equivalent" : "timefix",
    "githubapi" : "https://api.github.com/repos/LyfeOnEdge/timefix/releases",
    "author" : "Retr0id",
    "projectpage": "https://github.com/LyfeOnEdge/timefix",
    "description" : "Fixes the 'can't initialize time' bug with PyNX, this will set your system clock to something incorrect, you may want to adjust it afterwards.\nSource code by Retr0id.",
    "group" : TOOL,
    "install_subfolder": "switch/timefix",
    "pattern" : [["timefix"],".nro"],
    "license" : None
    },

    {
    "name" : "PyNX",
    "store_equivalent" : "pynx",
    "githubapi" : "https://api.github.com/repos/nx-python/PyNX/releases",
    "author" : "elnardu", 
    "projectpage": "https://gbatemp.net/threads/nx-python-create-python-homebrew-for-the-switch.499150/",
    "description" : """nx-python is an ecosystem for developing and running Python homebrew applications on the Nintendo Switch. 

PyNX serves as the entry point to running Python apps on your Switch. It is a homebrew app that contains a port of the CPython interpreter and allows you to run Python applications from the Homebrew Menu. Just name your application main.py and place it next to the PyNX.nro, and it will be executed as soon as you launch PyNX from the Homebrew Menu. Currently, Python 3.5 is supported.""",
    "group" : "interpreter",
    "install_subfolder": "switch",
    "pattern" : [["PyNX"],".zip"],
    "license" : "ISC License"
    },

]


customfirmwarelist = [
    {
    "name" : "Atmosphere",
    "store_equivalent" : "Atmosphere",
    "githubapi" : "https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases",
    "author" : "Atmosphere-NX",
    "projectpage": "https://github.com/Atmosphere-NX/Atmosphere/releases",
    "description": "Atmosphère is a customized firmware for the Nintendo Switch.",
    "group": "CFW",
    "install_subfolder": None,
    "license" : None,
    "pattern" : [["atmosphere"],".zip"]
    },

    {
    "name" : "Kosmos",
    "githubapi" : "https://api.github.com/repos/AtlasNX/Kosmos/releases",
    "author" : "AtlasNX",
    "projectpage": "https://github.com/AtlasNX/Kosmos/releases",
    "description" : "All-in-One CFW Package for the Nintendo Switch - previously SDFilesSwitch",
    "group" : "CFW",
    "install_subfolder": None,
    "pattern" : [["kosmos", "sdfiles"],".zip"]
    },

    {
    "name" : "ReiNX",
    "store_equivalent" : "ReiNX",
    "githubapi" : "https://api.github.com/repos/Reisyukaku/ReiNX/releases",
    "author" : "Reisyukaku", 
    "projectpage": "https://github.com/Reisyukaku/ReiNX",
    "description" : "A modular Switch custom firmware",
    "group" : "CFW",
    "install_subfolder": None,
    "pattern" : [["reinx"],".zip"]
    },

]

#Payloads
payloadlist = [
    #Message ctcaer about having hekate as its own payload
    {
    "name": "Hekate Payload",
    "store_equivalent": "Hekate",
    "githubapi": "https://api.github.com/repos/CTCaer/hekate/releases",
    "author" : "CTCaer", 
    "projectpage": "https://gbatemp.net/threads/rcm-payload-hekate-ctcaer-mod.502604/",
    "description": """Custom Nintendo Switch bootloader, firmware patcher, and more.
This version supports booting ALL current OS/CS CFW, Linux chainloading and payload tools.
No more SD card removals""",
    "group": "PAYLOADS",
    "payload": ["hekate_ctcaer",".bin"],
    "pattern": [["hekate_ctcaer"],".zip"],
    "install_subfolder" : "hekate"
    },



    {
    "name": "fusee-primary",
    "store_equivalent": "fusee-primary",
    "githubapi": "https://api.github.com/repos/Atmosphere-NX/Atmosphere/releases",
    "author" : "Atmosphere-NX", 
    "projectpage": "https://github.com/Atmosphere-NX/Atmosphere/tree/master/fusee/fusee-primary",
    "description" : "Bootloader for Atmosphere",
    "group" : "PAYLOADS",
    "pattern": [["fusee-primary"],".bin"],
    "payload": ["fusee-primary",".bin"],
    "install_subfolder" : "fusee-primary"
    },


    {
    "name" : "Argon-NX payload",
    "store_equivalent" : "argon-nx",
    "githubapi" : "https://api.github.com/repos/Guillem96/argon-nx/releases",
    "author" : "Guillem96", 
    "projectpage": "https://gbatemp.net/threads/argon-nx-payload-chainloader.527178/",
    "description": """#What Argon is?
 - Argon is a noble gas. "Argon" comes from Greek "Argon", neuter of "argos" meaning lazy , idle or inactive. Argon recieved this name because of its chemical inactivity.

 - Argon NX is an immutable payload which is injected to your Nintendo Switch via Fusee Gelee exploit.

#Purpose
 - The purpose of Argon NX is to stay immutable, so you can always inject it, without caring about other payloads getting updated (Always use ArgonNX for TegraSmash, TegraGUI, TrinkedM0...).

#How can it be immutable?
 - When Argon NX is injected, it automatically launches the payload.bin locacted at argon directory on your SD Card root.

 - If payload.bin is not present or VOLUME DOWN button is pressed on payload injection, Argon NX will list all payloads located at argon/payloads, and you will be able to select one of them to launch it.
""",
    "group" : "PAYLOADS",
    "pattern": [["argon-nx"],".zip"],
    "payload": ["argon-nx",".bin"],
    "install_subfolder": "argon"
    },


    {
    "name" : "Lockpick RCM",
    "store_equivalent" : "Lockpick_RCM",
    "githubapi" : "https://api.github.com/repos/shchmue/Lockpick_RCM/releases",
    "github_asset" : None,
    "author" : "shchmue", 
    "projectpage": "https://gbatemp.net/threads/lockpick-switch-key-derivation-homebrew.525575/",
    "description": """Lockpick_RCM is a bare metal Nintendo Switch payload that derives encryption keys for use in Switch file handling software like hactool, hactoolnet/LibHac, ChoiDujour, etc. without booting Horizon OS.

Due to changes imposed by firmware 7.0.0, Lockpick homebrew can no longer derive the latest keys. In the boot-time environment however, there are fewer limitations.""",
    "group" : "PAYLOADS",
    "pattern": [["Lockpick_RCM"],".bin"],
    "payload": ["Lockpick_RCM",".bin"],
    "install_subfolder" : "lockpick"
    },

#   {
#   "name" : "memloader",
#   "githubapi" : "https://api.github.com/repos/blawar/memloader/releases",
#   "author" : "blawar", 
#   "projectpage": "https://github.com/blawar/memloader",
#   "description": """ 
# #The life and death of Raj
# As many of you may not have heard, beloved developer Raj has met with a terrible fate. Raj's untimely passing saddens us all.

# Today, we honor him with a minor update to his code to improve memloader transfer speed by almost 20%. As you all do not know, memloader is the best way to take your nintendo switch backups.

# He was a true closed source soldier.

# RIP Raj

# memloader License GPLv2

# #Changes
# This section is required by the GPLv2 license

#  - initial code based on https://github.com/Atmosphere-NX/Atmosphere
#  - everything except fusee-primary been removed (from Atmosphere)
#  - all hwinit code has been replaced by the updated versions from https://github.com/nwert/hekate
#  - BPMP code from https://github.com/CTCaer/hekate/
#  - Memloader code from https://github.com/rajkosto/memloader/
#  - Files pinmux.c/h, carveout.c/h, flow.h, sdram.c/h, decomp.h,lz4_wrapper.c,lzma.c,lzmadecode.c,lz4.c.inc,cbmem.c/h are based on https://github.com/fail0verflow/switch-coreboot.git sources
#  - main.c has been modified to display an on-screen menu and either load binaries via ini files on microsd card, or directly via USB transfer from host

# #Responsibility
# I am not responsible for anything, including dead switches, loss of life, or total nuclear annihilation.
#   """,
#   "group" : "PAYLOADS",
#   "pattern": [["memloader"],".bin"]
#   },
]



payloadinjector = [
    {
    "name" : "fusee-launcher",
    "githubapi" : "https://api.github.com/repos/Cease-and-DeSwitch/fusee-launcher/releases",
    "github_asset" : "tarball_url", 
    "author" : "Qyriad", 
    "projectpage": "https://gbatemp.net/threads/web-fusee-launcher.502423/",
    "description" : "",
    "group" : "SPECIAL",
    "install_subfolder": None,
    },
]

medialist = [
    {
    "name": "pplay",
    "store_equivalent" : "pplay",
    "githubapi": "https://api.github.com/repos/Cpasjuste/pplay/releases",
    "author" : "Cpasjuste", 
    "projectpage": "https://gbatemp.net/threads/pplay-switch-video-player.526187/",
    "description" : "pPlay is a video player for the Nintendo Switch. pPlay support most popular video formats, have subtitles (embedded ass) and http streaming support.",
    "group" : "video player",
    "install_subfolder": "switch",
    "pattern" : [["pplay"], ".zip"],
    "license" : NA
    },

    {
    "name": "ComicNX",
    "githubapi": "https://api.github.com/repos/HookedBehemoth/ComicNX/releases",
    "store_equivalent" : "ComicNX",
    "author" : "HookedBehemoth", 
    "projectpage": "https://github.com/HookedBehemoth/ComicNX",
    "description": """Shitty comic-browser for your Nintendo Switch.

This uses my [HookedBehemoth's] Plutonium fork because I don't need Audio + Web (- ~1MiB) and I rescale Image-Elements on reloading an Image.

Licensing
- This software is licensed under the terms of the GPLv2.

Credits
- switchbrew for the libnx project and the extensive documentation, research and tool development pertaining to the Nintendo Switch.
- devkitPro for the devkitA64 toolchain and libnx support.
- atlasnx for Swurl and some util methods
- XorTroll for Plutonium
    """,
    "group": TOOL,
    "install_subfolder": "switch",
    "pattern" : [["comic-browser", "ComicNX"], ".nro"],
    "license" : GPL2,
    },

    {
    "name": "lennytube",
    "githubapi": "https://api.github.com/repos/noirscape/lennytube/releases",
    "store_equivalent" : "lennytube",
    "author" : "noirscape", 
    "projectpage": "https://gbatemp.net/threads/lennytube-homebrew-youtube-nro.545824/",
    "description": """Youtube on the Nintendo Switch.

Rationale
The YouTube title on the Switch is only usable if one is not banned, since the title in question logs in on Nintendo Network. Whilst it's possible to bypass this by patching the YouTube app, this is far from ideal as the resulting file is not allowed to be shared.

This application aims to circumvent that last problem by launching it's own WifiApplet, meaning no copyrighted data is ever involved.

Limitations
Desktop mode only (TV mode is inaccessible, Mobile doesn't play videos properly).
Works only from APPLICATION mode (it will display a warning and instructions how to do this if you're still running from APPLET).""",
    "group": "video player",
    "install_subfolder": "switch",
    "pattern" : [["lennytube"], ".nro"]
    }

]










# name = {
#   "tool" : homebrewlist,
#   "game" : gameslist,
#   "cfw" : customfirmwarelist,
#   "emu" : emulist,
#   "scripts" : nxpythonlist,
# }

#   },
# #other switch content
#   {
#   "name": "sigpatches",
#   "githubapi": None, #yet, added this at last moment, will be dynamic next version
#   "projectpage": "https://gbatemp.net/threads/i-heard-that-you-guys-need-some-sweet-patches-for-atmosphere.521164/",
#   "directlink": "https://github.com/AtlasNX/Kosmos/releases/download/v11.11.1/Additional.SigPatches.espatches.zip",
    
    
#   "asset" : 0,
#   "author": None,
#   "image" : "https://avatars1.githubusercontent.com/u/205276?s=400&v=4",
#   "description":"""Ok, Here you are
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
#   "group": "Patches",
#   },

# experimentallist = [
#   {
#   "name" : "Incognito",
#   "githubapi" : "https://api.github.com/repos/blawar/incognito/releases",
#   "author" : "blawar", 
#   "projectpage": "https://gbatemp.net/threads/incognito.531924/",
#   "description" : "Wipes personal information from your Nintendo Switch by removing it from prodinfo.",
#   "group" : "tool, REINX ONLY",
#   "install_subfolder": None,
#   "pattern" : [["incognito"], ".nro"],
#   },

# ]






#No Repo Data
# {
# "category": "game", 
# "binary": "/switch/MysteryOfSolarusDX.nro", 
# "updated": "29/12/2018", 
# "name": "solarus", 
# "license": "GPLv3", 
# "title": "Mystery of Solarus DX", 
# "url": "https://github.com/carstene1ns/zsdx/tree/switch-port", 
# "author": "carstene1ns, solarus-games", 
# "changelog": "n/a", 
# "extracted": 25924, 
# "version": "1.0", 
# "filesize": 22594, 
# "web_dls": 4082, 
# "details": "The Legend of Zelda: Mystery of Solarus DX is set to be a direct sequel to The Legend of Zelda: A Link to the Past on the SNES, using the same graphics and game mechanisms. Zelda Mystery of Solarus DX is the first game made with the Solarus engine and in fact, Solarus was primarily designed for this game.", 
# "app_dls": 16629, 
# "description": "Fanmade Legend of Zelda game"
# }, 

#Static location
# {
# "category": "tool", 
# "binary": "/switch/RCMReboot/RCMReboot.nro", 
# "updated": "03/12/2018", 
# "name": "RCMReboot", 
# "license": "n/a", 
# "title": "RCMReboot", 
# "url": "https://gbatemp.net/download/rcmreboot.35294/", 
# "author": "hippydave", 
# "changelog": "v1.0f - Fixed release zip to get rid of hidden MacOS files. Actual files unchanged.\\nv1.0 - first version", 
# "extracted": 9784, 
# "version": "1.0f", 
# "filesize": 3825, 
# "web_dls": 215, 
# "details": "I do not condone using this app if your SD card is EXFAT formatted.\\nnatinusala & ctcaer pointed out that Atmosphere's method to reboot to RCM, and therefore the method used by this app, does not properly shutdown HOS so there is some unquantified risk of file corruption. Still use at your own risk on fat32, but just don't use it on exfat please.\\n\\nIntended for use on Switches that don't have AutoRCM installed.\\n\\nThis uses a new feature added to exosphere in Atmosphere 0.8.1, so it won't work in other CFWs unless they add it in a compatible way. Also Atmosphere 0.8.1 got a silent update with a bug fix to get this feature working, so if you already downloaded it before sometime on 1st Dec you might need to update it again (if it crashes with an orange screen instead of going to RCM, you need to update). There's a commit hash in the filename, make sure you have atmosphere-0.8.1-master-bd76e73 (or if you're living in the future, Atmosphere 0.8.2 or higher will be fine too). It sounds like it currently only works if you load Atmosphere using fusee-primary.bin, not if you use hekate to load Atmosphere as separate files (using hekate to load fusee-primary.bin is ok). This will likely be fixed when hekate is updated.\\n\\nThere are two versions included in the zip, each available as an .nro (put it in its folder inside the \"switch\" folder on the root of your sd card) and as an installable .nsp (install with the stupidly-named installer of your choice).\\n- RCMRebootInstant will reboot to RCM as soon as it loads.\\n- RCMReboot will give you a 5 second countdown with a chance to change your mind.\\n\\nThe reason RCMReboot is a much bigger file than the Instant version is that I used cpasjuste's cross2d library to put stuff on screen, mostly because I've been using it for the other project I'm working on and it saved me time. Sweet library, check it out.\\n\\nCredits to cpasjuste for the aforementioned cross2d, re.lax for nro2nsp (which uses hacbrewpack by the-4n), SciresM for Atmosphere, libnx, and for fixing the bugs in them I found while making this, and everyone else who worked on Atmosphere, libnx, devkitpro and all that good stuff.\\n\\nSource included for peace of mind, and in case of licence requirement. If I've got anything horribly wrong with licensing or credits just let me know. If you want to build it yourself you'll need libnx updated with the latest commit (which isn't in a release build at the time of writing), and to figure out the cross2d setup for the non-Instant version.", 
# "app_dls": 1468, 
# "description": "Reboot into RCM"
# }, 











#7zip
# https://github.com/CVFireDragon/PowerToolsNX/releases

#Complex handling
# https://github.com/HarryPeach/DinoRunNX/releases

# {
# "category": "tool", 
# "binary": "none", 
# "updated": "20/12/2018", 
# "name": "Switch_Media_Host", 
# "license": "n/a", 
# "title": "Switch-Media-Host", 
# "url": "https://github.com/ImmaSpoon/Switch-Media-Host/releases", 
# "author": "ImmaSpoon", 
# "changelog": "v1.2.0\\n\\n-No longer using root directory for main file\\n-Cleaner UI, with nice scrollbar.\\n-GitHub button\\n-'Game Folders' changed to 'Sort by Games'\\n-Move announcement to bottom of the page\\n-Moved file count to top right of photo list\\n-Added new screen to the Switch screen\\n\\nv1.1.0\\n\\nAdded new page, allows for organized game screenshots.\\nFixed a few things under-the-hood.", 
# "extracted": 280, 
# "version": "1.2.0", 
# "filesize": 99, 
# "web_dls": 47, 
# "details": "PYNX is Required for this to run.\\n\\nThis is a simple python script that allows you to see your Switch screenshots directly from your smart devices browser! This allows for easier transfering, and has a simple design to it. This only works over LAN, and will not publicly show your screenshots to all of the internet.\\n\\nCurrently only works with photos for now, video clips will come soon.\\n\\n\\nUsage:\\nOnce you have it installed, open PyNX from the hbmenu.\\n\\nNext, select the 'Switch Media Host.py' file and run.\\n\\nIt should show a blank screen for 5-10 seconds, shouldn't take long.\\n\\nYour switch should show you an address, go to that address on any device on the same network.\\n\\nBoom! You can see and download your screenshots easily.\\n", 
# "app_dls": 1013, 
# "description": "Host your Switch media over LAN"
# }, 



#Later
# {
# "category": "game", 
# "binary": "/switch/simon-nx/SIMON-NX.nro", 
# "updated": "28/10/2018", 
# "name": "SimonNX", 
# "license": "none", 
# "title": "Simon NX", 
# "url": "https://github.com/K3yn/simon-nx/releases", 
# "author": "K3yn", 
# "changelog": "simon-nx0.2\\n\\nadded 2 levels\\nplayable touch and only with joy in dock mode\\n\\nv0.1 - Initial Release", 
# "extracted": 5302, 
# "version": "simon-nx0.2", 
# "filesize": 3857, 
# "web_dls": 30, 
# "details": "Simon is an electronic game of memory skill invented by Ralph H. Baer and Howard J. Morrison, with software programming by Lenny Cope. The device creates a series of tones and lights and requires a user to repeat the sequence. If the user succeeds, the series becomes progressively longer and more complex. Once the user fails or the time limit runs out, the game is over. The original version was manufactured and distributed by Milton Bradley and later by Hasbro after it took over Milton Bradley. Much of the assembly language was written by Charles Kapps[citation needed], who taught computer science at Temple University and also wrote one of the first books on the theory of computer programming. Simon was launched in 1978 at Studio 54 in New York City and was an immediate success, becoming a pop culture symbol of the 1970s and 1980s.\\n\\nFeatures :\\n\\n- U can use differents accounts for play.\\n- Highscores\\n- Tactil\\nControls : - Double Touch or D-pad + A : Menu Selection - Short Touch or Short A : enable color - - : Back to menu - : Restart game - Plus : Exit game", 
# "app_dls": 383, 
# "description": "Memory Game"
# }, 



# {
# "name": "nx-hbloader",
# "githubapi": "https://api.github.com/repos/switchbrew/nx-hbloader/releases",
# "store_equivalent" : 
# "author" : "switchbrew", 
# "projectpage": "",
# "description": """Switchbrew has released a major update to nx-hbloader, a host process for loading NRO files for Switch homebrew applications. This new version makes some improvements such as now allowing for applications to run with the full amount of 3.2GB RAM, as opposed to the past, where it could only use ~400MB of RAM. Library applets are still usable, and older homebrew NRO files will still work, but they are limited to using 442MB of RAM max, this also counts when running it through the album app. Other changes were made, including making the program less prone to issues by disabling core3 access, and more.""",
# "group": "tool",
# "install_subfolder": "switch",
# "pattern" : [["hbl"], ".nsp"]
# },






    # "name" : None,
    # "store_equivalent" : None,
    # "githubapi" : None,
    # "author" : None,
    # "projectpage": None,
    # "description" : None,
    # "group" : None,
    # "install_subfolder": None,
    # "pattern" : [[],],
    # "license" : None,
    # "tags" : []

    # "name" : None,
    # "store_equivalent" : None,
    # "githubapi" : None,
    # "author" : None,
    # "projectpage": None,
    # "description" : None,
    # "group" : None,
    # "install_subfolder": None,
    # "pattern" : [[],],
    # "license" : None,
    # "tags" : []

    # "name" : None,
    # "store_equivalent" : None,
    # "githubapi" : None,
    # "author" : None,
    # "projectpage": None,
    # "description" : None,
    # "group" : None,
    # "install_subfolder": None,
    # "pattern" : [[],],
    # "license" : None,
    # "tags" : []

    # "name" : None,
    # "store_equivalent" : None,
    # "githubapi" : None,
    # "author" : None,
    # "projectpage": None,
    # "description" : None,
    # "group" : None,
    # "install_subfolder": None,
    # "pattern" : [[],],
    # "license" : None,
    # "tags" : []

    # "name" : None,
    # "store_equivalent" : None,
    # "githubapi" : None,
    # "author" : None,
    # "projectpage": None,
    # "description" : None,
    # "group" : None,
    # "install_subfolder": None,
    # "pattern" : [[],],
    # "license" : None,
    # "tags" : []

    # "name" : None,
    # "store_equivalent" : None,
    # "githubapi" : None,
    # "author" : None,
    # "projectpage": None,
    # "description" : None,
    # "group" : None,
    # "install_subfolder": None,
    # "pattern" : [[],],
    # "license" : None,
    # "tags" : []












#https://github.com/KranKRival/BootSoundNX/releases # Bad release structure
