# HBUpdater
![](img/main.png)

![License](https://img.shields.io/badge/License-GPLv3-blue.svg) [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/HBUpdater/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/HBUpdater.svg)]()

# About
HBUpdater is a one-stop-shop for managing and updating your Nintendo Switch Homebrew.

# Backend
Currently the [backend](https://github.com/LyfeOnEdge/HBUpdater_API) runs every 30 minutes to keep the repos file up to date. The repo json can be found here: [repos](https://github.com/LyfeOnEdge/HBUpdater_API/releases)

# Notes
  - Downloads packages directly from github
  - Easily install lots of popular Homebrew
  - RCM injector (payloads downloaded from github)
  - Tracks which homebrew and what versions you have installed, compatible with the Homebrew Appstore 
  - Content includes tools, emulators, media viewers, games, and more
  - No longer visit 17.53 different places to make sure you have the latest version of everything

# HBUpdater
## View update notes and install old/legacy versions
![View update notes and install old/legacy versions](img/detail.png)

## Built-in RCM injector
![Built-in RCM injector (Uses fusee-launcher)](img/injector.png)

# Requirements:
    Works on: Mac, Window, Linux
    Python 3.6 or greater

# How to use:
##### Windows:
  - Extract HBUpdater.zip
  - Install [python](https://www.python.org/downloads/release/python-373/)
  	- If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
  - In a command prompt type ```pip install pillow pyusb``` to install dependencies
  - Double-click startHBUpdater.bat

##### Macintosh:
- Extract HBUpdater.zip
- Mac users may already have a compatible version of python installed, try double-clicking HBUpdater.py
--If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work, install [python](https://www.python.org/downloads/release/python-373/)

##### Linux:
- Extract HBUpdater.zip
- Navigate to the directory in a terminal
- Type "python HBUpdaterGUI.py"
  - If you are missing dependencies do the following:
  - sudo apt-get install python3 python3-pip python3-tk python3-pil.imagetk
- If you don't know how to do this you should probably be using Windows.
- For access to USB functions you must run python with elevated privledges (sudo)

##### Want to contribute? Have ideas? Questions? Great!
You can find me here: 
**[4TU/Switchbru](https://discord.gg/uAfu6yM)**
