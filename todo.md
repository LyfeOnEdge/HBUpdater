Todo:
Less bold

Releases listbox - display if asset could be found. otherwise grey out download button and listbox entry

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
