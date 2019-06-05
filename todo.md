THIS IS MY PERSONAL TODO LIST
NONE OF THESE IDEAS, PIECES OF SOFTWARE, OR TODOS ARE SET IN STONE, THEY MAY NEVER MAKE THEIR WAY INTO HBUPDATER

Difficulty / Time:
[EASY]
[MEDIUM]
[HRNNN]

mustdo:
test pattern - based homebrew checking

todo:
    fix search bar to update every character

Priority:
    High:
        settings:
            window default launch size [EASY] 
            ftp tool [HARD]
        bugs:
        features:
            improve repo management and addition [MEDIUM]
            github 304 rate limiting avoidance [HARD]
        Add pattern-based file finding in HBUpdater install function

    Medium:
        features:
            Home page features:
                SD card:
                    backup and restore sd contents easily
                    Browse installed items in single screen
                    sd card no longer forgets current one if invald one is chosen

    Low:
        file structure:
            clean up imports
            make entrybox a subclass of searchbox
        HBUpdater updater
            use github api (duh)
            use yes/no screen when new update is available (diable screen in settings)
    Code clean-up:
    move cfw install code to core



    Aesthetic:
        borderless window, settings on top bar with quick-access
        fix linux icon
        implement gross light theme

Prerelease checklist 
Try:
    Nut
    Fluffy
    Injector
    inject
    Serial Checker
    Install
    Uninstall



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
    https://github.com/rsn8887/uae4all2/releases
    https://github.com/ELY3M/Lighting-up-LED-on-right-joycon-for-Nintendo-Switch/releases
    https://github.com/Manurocker95/TIL_NX/releases/
    https://github.com/Manurocker95/Evolution-Saved-Me-NX/releases/

todone:
0.8:
    Projects missing github links will now get one generated from the github api link to go to the github repo, this applies to user-added homebrew as well. 
    Added titles to pages so you know what you are looking at.
    Added CFW manager alpha
    Payload injector page now indicates if injector is already downloaded
    Title bar now displays app version
0.9:
    Improved HBUpdaterGUI.py code layout
    software lists are now populated within the page that uses them, this is more flexible and requires far less code
    The buttons were getting crowded on the standard homebrew page so I've added a new landing page with big icons. Gives it a metro feel
    HBUpdater will now check for updates, setting available in setting menu to disable it
    errorpage.py now handles errors and yes/no questions, code reduction in installerhelperpage.py
    improved folder handling, moved all folder definitions to locations.py
    removed homebrewcore.py to simplify backend
    download - on - demand serial checker
    nut, fluffy, serial checker, payload injector, etc download into a tools subfolder for better folder structure 
    installerhelperpage's functions have been moved to toolhelper.py in modules, the giu code has been taken over by errorpage.py
0.10
    stopped crash when initial json fails to download
    app now works offline
    app size now set in guisettings_user.json
    homepage scales better






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