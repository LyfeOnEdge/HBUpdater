# HBUpdater
![](img/main.png)

![License](https://img.shields.io/badge/License-GPLv3-blue.svg) [![Releases](https://img.shields.io/github/downloads/LyfeOnEdge/HBUpdater/total.svg)]() [![LatestVer](https://img.shields.io/github/release-pre/LyfeOnEdge/HBUpdater.svg)]()

# About
HBUpdater is a one-stop-shop for managing and updating your Nintendo Switch Homebrew.

# Features
  - Downloads packages directly from github
  - Easily install lots of popular Homebrew
  - RCM injector (payloads downloaded from github)
  - Tracks which homebrew and what versions you have installed, compatible with the Homebrew Appstore 
  - Content includes tools, emulators, media viewers, games, and more
  - No longer visit 17.53 different places to make sure you have the latest version of everything

## View update notes and install old/legacy versions
![View update notes and install old/legacy versions](img/detail.png)

## Built-in RCM injector
![Built-in RCM injector (Uses fusee-launcher)](img/injector.png)

## Demo
(Goes to youtube)
[![Alt text](https://img.youtube.com/vi/NESayHlzOwU/0.jpg)](https://www.youtube.com/watch?v=NESayHlzOwU)

# Requirements:
    Works on: macOS, Windows, Linux
    Python 3.6 or greater

# How to use:
##### Windows:
  - Extract HBUpdater.zip
  - Install [python](https://www.python.org/downloads/release/python-373/)
    - If you do a custom installation remember to install tcl/tk, add python to the path, and include pip
  - In a command prompt type ```pip install -r requirements``` to install dependencies
  - Double-click startHBUpdater.bat

##### Macintosh:
- Extract HBUpdater.zip
- Mac users may already have a compatible version of python installed, try double-clicking HBUpdater.py
--If the file opens in a text reader, close the reader and right-click the file and open it with pylauncher
- If this still doesn't work, install [python](https://www.python.org/downloads/release/python-373/)

##### Linux:
- Extract HBUpdater.zip
- Navigate to the directory in a terminal
- Type `python HBUpdaterGUI.py`
  - If you are missing dependencies do the following:
  - `sudo apt install python3 python3-pip python3-tk python3-pil.imagetk`
- If you don't know how to do this you should probably be using Windows.
- For access to USB functions you must run python with elevated privledges (sudo)

## TroubleShooting:
##### Mac:
- Error:
  - ```ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1056)```
- Solution:
  - Macintosh HD > Applications > Python3.6 folder (or whatever version of python you're using) > double click on "Install Certificates.command" file

# How it works:

###NOTICE: I WILL BE MOVING TO A BETTER REPO SYSTEM IN THE FUTURE, DETAILS SOON(tm).

## The big picture
[**repo collection**](#repo-collection)

[**repo stitiching**](#repo-stitching)

[**repo distribution**](#repo-distribution)
  
[**repo parsing**](#repo-parsing)
  
[**package management**](#package-management)

Short and sweet:
The repository (AKA HBUpdater_packages):
A package repository broken out into package.json files with info that can't or shouldn't be gleaned from the github api, these lay out author, package name, releases api link, etc.
This repository can be found here: `https://github.com/LyfeOnEdge/HBUpdater_packages`.

The backend (AKA HBUpdater_API):
A script periodically (every 30 minutes) queries the github api with an auth token to grab updated api files for each package at `https://api.github.com/repos/__organization__/__repo__`, it then bundles the api files, checks them agains a previous version, and if anything has changed releases this bundle at: `https://github.com/LyfeOnEdge/HBUpdater_API/releases`

The frontend (AKA HBUpdater):
Any tool that interacts with the api should be able to grab a github release. The api file is grabbed from `https://api.github.com/repos/LyfeOnEdge/HBUpdater_API/releases`, the latest release is found, downloaded, and parsed into categories by an intermediate tool.

## repo collection
  Package entries are found here at [HBUpdater_packages](https://github.com/LyfeOnEdge/HBUpdater_packages). 

## repo stitching
  The repo builder is the repomaker_server.py script located in the source of LyfeOnEdge/HBUpdater_API. It accesses the github api using a github token. The purpose of the token is twofold, it allows the repo builder to exceed the normal 60 api requests / hour as well as make releases in its *own* repo. This means the "releases" section of the LyfeOnEdge/HBUpdater_API repo source on github acts as an etagged "server" for the repo json.
  The repo builder goes through each entry in the repo and grabs the api json, it then adds the loaded api json to the info grabbed from the repository.

## repo distribution
  When each entry has had an updated json object appended the whole object is organized into a json object and dumped. If any content in the json has changed it gets pushed as a new release to github, with the tag name incrementing by one.

  The receiving app (LyfeOnEdge/HBUpdaterGUI) grabs the repo file by getting the github api releases json at https://api.github.com/repos/LyfeOnEdge/HBUpdater_API/releases, which contains a link to the latest release of the HBUpdater_API repo.

## repo parsing
  The receiving app (LyfeOnEdge/HBUpdaterGUI) parses the json into mapped lists based on category. Each category is displayed on a page in the app.

## package management
  HBUpdater uses a heavily modified python rewrite of vgmoose's [libget](https://github.com/vgmoose/libget)
  It should be compatible with vgmooses [Homebrew Appstore](https://github.com/vgmoose/hb-appstore), except packages not also offered by the appstore will not show up in vgmoose's appstore.

##### Want to contribute? Have ideas? Questions? Great!
You can find me here: 
**[4TU/Switchbru](https://discord.gg/uAfu6yM)**