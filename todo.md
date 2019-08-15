THIS IS MY PERSONAL TODO LIST
NONE OF THESE IDEAS, PIECES OF SOFTWARE, OR TODOS ARE SET IN STONE, THEY MAY NEVER MAKE THEIR WAY INTO HBUPDATER

todo:
    make auto-zip building script utilizing .gitignore
    build stand-alone with pyinstaller
    warn when repos collide (multiple heketes etc)
    move more stuff to style.py instead of format.py

Priority:
    (Highest to lowest)
    High:
        Create test function script
        settings:
            ftp tool
        features:
            warn user when no json was downloaded
    Medium:
        features:
            Home page features:
            implement auto-injection
            option to not clean-install
    Low:
        break json handling in to a function called get_repo_object()
        preset packs
        on-the-fly toggle off infobox
       
        navbox moved to pagetemplate
        file structure:
            clean up imports

        HBUpdater updater
            use github api (duh)
            "skip this version" button
            use yes/no screen when new update is available (disable screen in settings)
        pattern-based payloads
        move folders definitions to guisettings.json

        Dangerous things:
            settings menu button to delete userrepos.json and guisettings.json

    game randomizer: pick a random game from list of installed
    Code clean-up:
   
    Aesthetic:
        borderless window, settings on top bar with quick-access
        fix linux icon
        implement gross light theme

    cleanup todo

Prerelease checklist 
Try:
    Nut
    Fluffy
    Fusee
    inject
    Serial Checker
    Install
    Uninstall
    add repo
    make backup

ongoing:
No releases (Issue created on github)
    Python:
        https://gbatemp.net/threads/pynx-game-redirector.507726/
    Homebrew:
        https://github.com/Chrs2324/SSBUStageInjector
    Tools:
        https://github.com/friedkeenan/GoldtreePy
To add:
    
    https://github.com/Marice/ScreenTester-NX/releases <- Inconsistent release format but it will work due to flexible handling
    https://github.com/colin969/switch-reader/releases
    https://github.com/SilentFlyBy/Blobby-Volley-2-Switch/releases
    https://github.com/ELY3M/Lighting-up-LED-on-right-joycon-for-Nintendo-Switch/releases
    https://github.com/Manurocker95/TIL_NX/releases/
    https://github.com/Manurocker95/Evolution-Saved-Me-NX/releases/

todone:
0.8:
    - Projects missing github links will now get one generated from the github api link to go to the github repo, this applies to user-added homebrew as well. 
    - Added titles to pages so you know what you are looking at.
    - Added CFW manager alpha
    - Payload injector page now indicates if injector is already downloaded
    - Title bar now displays app version
0.9:
    - Improved HBUpdaterGUI.py code layout
    - software lists are now populated within the page that uses them, this is more flexible and requires far less code
    - The buttons were getting crowded on the standard homebrew page so I've added a new landing page with big icons. Gives it a metro feel
    - HBUpdater will now check for updates, setting available in setting menu to disable it
    errorpage.py now handles errors and yes/no questions, code reduction in installerhelperpage.py
    - improved folder handling, moved all folder definitions to locations.py
    removed homebrewcore.py to simplify backend
    - added download - on - demand serial checker
    - nut, fluffy, serial checker, payload injector, etc download into a tools subfolder for better folder structure 
    - installerhelperpage's functions have been moved to toolhelper.py in modules, the giu code has been taken over by errorpage.py
0.10
    - added about page, separated from settings
    - stopped crash when initial json fails to download
    - app now works offline
    - app size now set in guisettings_user.json
    - homepage scales better
    - app now writes to .get package location for HBappstore compatibility
    - images are now cached based on author name rather than project name, saving on bandwidth and reducing disc reads  
    - double-click on list pages now executes the set "primary function" of the page (inject payload, install homebrew, restore backup, etc...)
    author images now cache properly in about page
    - install will no longer error if user has removed a file then tried to uninstall it
    - very basic SD card backup tool added
    - user repos now use the pattern system
    - repo jsons now download under the name of the project, this means homebrew that share the same url don't download twice, furthur reducing bandwidth and ratelimit incursion
    - added a session cache to the webhandler so if a repo was already downloaded this session it won't be redownloaded, this is especially useful for users adding multiple assests from the same repo (eg a repo with multiple .nros for different emulators)
    - app now uses the HBAppstore package management system instead of mine, this was a bit annoying to implement (it took longer than I'd like to admit)
1.0-1
Release
 - injector now remembers last payload
 - many folders now init only when their corresponding software is downloaded
1.1
 - Injector now uses pattern system for standardization reasons
 - Broke pattern-based asset finding out into a function
 - Fixed injector page listbox continuing under console
 - added blawar's modded memloader
 - cleaned up some messy copy-pasted app descriptions
 - tools like nut are now Popen() in a config folder so config files aren't at risk, this is for the future addition of proper version managing for nut and fluffy
 - Serial checker no longer needs download as it has been re-written as a single file
 - Fixed bug with adding forked repos
 - Search now updates with every charater typed
 - Users can now set the name of an added repo
 - Improved per-file-type-handling
 - Content
     + Added ComicNX
     + Added Apollo
     + Added hbmenu
     + Removed sdsetup-switch (for now) per authors recommendation












    
 

bites for official release:
Users already using fluffy or nut will likely already have the prerequsites needed to run this app.
Verified working with pypy


WINDOWS ONLY
https://gbatemp.net/threads/nsc_builder-nintendo-switch-cleaner-and-builder-game-updates-dlc-in-a-single-xci.522486/ 

https://github.com/nicoboss/nsZip/releases

https://github.com/CaitSith2/SwitchSDTool/releases

https://github.com/The-4n/reNXpack/releases/

https://github.com/Myster-Tee/NxFileViewer/releases

https://github.com/The-4n/hacPack/releases

https://github.com/Destiny1984/XCI-Cutter/releases

AGNOSTIC
https://github.com/AnalogMan151/splitNSP/releases
https://github.com/vgmoose/nro-asset-editor/releases


https://gbatemp.net/threads/download-all-cheats-from-max-cheats-bash-shell-script.528893/

NRO (SOME RELEASES MISSING DATA WILL NEED TO UPDATE CODE TO BE ABLE TO HANLDE REPOS WITHOUT ASSETS WITH AN ERROR WINDOW )
https://github.com/keeganatorr/openfodder-switch/releases

#maybe
#https://github.com/jakibaki/In-Home-Switching/releases
#https://f4ke.de/dev/switch/

#7zip
#https://github.com/WinterMute/chocolate-doom/releases/tag/chocolate-doom-3.0.0-switch

KIPS (FUTURE FEATURE)

https://github.com/jakibaki/sys-netcheat/releases
https://gbatemp.net/threads/ldn_mitm-play-local-wireless-supported-games-online.525512/
https://gbatemp.net/threads/sys-audioplayer-background-audio-player-for-the-nintendo-switch.536580/

Future
https://gbatemp.net/threads/switchguide-updater.522136/

huh
https://github.com/Povstalez/Kefir-Updater/releases





#useful code bits for later
winfo exists window: Returns 1 if there exists a window named window, 0 if no such window exists.
for child in frame2.winfo_children():
    child.configure(state='disable')


#Other ideas
Python homebrew to clear user's screenshot directory


Ideas for the future:
https://github.com/bodyXY/Ultimate-Material-Hactool-GUI
https://github.com/bodyXY/NES-ONLINE-Game-Injector

