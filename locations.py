import os, sys
#Folder and file definitions for easy access
update_url = None

wd = sys.path[0]

folders_to_init = []
#Folder to hold cache folders
cachefolder =  os.path.join(wd, "cache")
#Folder to cache repo jsons
jsoncachefolder = os.path.join(cachefolder,"json")
#Folder to cache author images
imagecachefolder = os.path.join(cachefolder,"images")
#Download folder
downloadsfolder = os.path.join(wd, "downloads")
#Folder for preset bundle jsons
presetsfolder = os.path.join(wd, "presets")

assetsfolder = os.path.join(wd, "assets")

folders_to_init = [cachefolder, jsoncachefolder, imagecachefolder, downloadsfolder, presetsfolder]
for folder in folders_to_init:
	if not os.path.isdir(folder):
		print("initializing folder {}".format(folder))
		os.mkdir(folder)

etagfile = os.path.join(jsoncachefolder, "etags.json")

notfoundimage = os.path.join(os.path.join(wd, "assets"), "notfound.png")
backimage = os.path.join(os.path.join(wd, "assets"), "return.png")

aboutfile = os.path.join(wd, "about.txt")
readme = os.path.join(wd, "readme.md")