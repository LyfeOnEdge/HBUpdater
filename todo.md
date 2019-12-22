Todo:
Less bold

Releases listbox - display if asset could be found. otherwise grey out download button and listbox entry

splash on installed_category_frame when nothing present.

Exclude option for readmes etc.

Hekete ini editor

Alert when files collide


System-specific:
    - Linux
        + favicon
        + fix text sizing issues



Modules:
    - Appstore:
        + change download path for zips, delete after download / load in to ram instead
     
    
2.0:
Major Revision
2.1:
fixed error when no path selected when sd dialog shows
fixed fail-to-install due to an issue where `with open()` on a zip would allow the file to be deleted within the `with` on linux but not windows, thanks cptWhiskey.
2.2:
Moved to new repo.json layout
2.3:
fixed bug displaying injector banner, less bold
reduced package image pop-in, and fixed images missing on screen load due to insufficient padding
Added settings system, settings page, added on-the fly tile size adjustment
Updater failing to get update file no longer causes crash
Falls back on old repo json when new one unavailable
Added multiple maximization settings (Normal/Fullscreen/Maximized)
Added setting to keep window topmost
Fixed searchbar and dropdown padding in main page