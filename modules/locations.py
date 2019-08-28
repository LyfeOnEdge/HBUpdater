import os, sys, json
#Folder and file definitions for easy access
wd = sys.path[0]

folders_to_init = []
#Folder to hold app downloads
downloadsfolder =  os.path.join(wd, "downloads")
folders_to_init.append(downloadsfolder)
#Folder to hold cache folders
cachefolder =  os.path.join(wd, "cache")
folders_to_init.append(cachefolder)
#Folder to cache repo jsons
jsoncachefolder = os.path.join(cachefolder,"json")
folders_to_init.append(jsoncachefolder)
#Folder to cache author images
imagecachefolder = os.path.join(cachefolder,"images")
folders_to_init.append(imagecachefolder)
#Folder for software tools like serial checker, etc
toolsfolder = os.path.join(wd, "tools")
folders_to_init.append(toolsfolder)

configfolder = os.path.join(toolsfolder, "config")
folders_to_init.append(configfolder)

#Folder for downloaded Blawar nut client
nutfolder = os.path.join(toolsfolder, "nut")
#Folder for downloaded fluffy
fluffyfolder = os.path.join(toolsfolder, "fluffy")
#Folder for downloaded serail checker
ssncfolder = os.path.join(toolsfolder, "ssnc")
#Folder for downloaded fuess-primary
injectorfolder = os.path.join(toolsfolder, "fusee")
#Folder for downloaded payloads
payloadsfolder =  os.path.join(wd, "payloads")
#Folder for backups
backupsfolder = os.path.join(wd, "backups")

for folder in folders_to_init:
	if not os.path.isdir(folder):
		print("initializing folder {}".format(folder))
		os.mkdir(folder)

ssncserials = os.path.join(jsoncachefolder,"serials.json")
etagfile = os.path.join(jsoncachefolder, "etags.json")

updateapi = "https://api.github.com/repos/LyfeOnEdge/HBUpdater/releases"




def openJson(file):
    with open(file, encoding="utf-8") as f:
        return json.load(f)

repo_file = os.path.join(wd, "repos.json")

repos = openJson(repo_file)

homebrewlist = repos["homebrew"]
emulist = repos["emulators"]
customfirmwarelist = repos["cfw"]
gameslist = repos["games"]
nxpythonlist = repos["python"]
nutserverdict = repos["nut"]
fluffydict = repos["fluffy"]
payloadlist = repos["payloads"]
payloadinjector = repos["fusee"]