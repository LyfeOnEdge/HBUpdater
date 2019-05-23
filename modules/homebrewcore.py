import os, sys

def get_path(filename):
	return os.path.join(sys.path[0], filename)

def exists(filename):
	return os.path.isfile(filename)

def joinpaths(prefix,suffix):
	return os.path.join(prefix,suffix)

def direxist(foldername):
    return os.path.isdir(foldername)

#folders thet need to be initialized on app start
downloadsfolder = get_path("downloads")
cachefolder = get_path("cache")
payloadsfolder = get_path("payloads")
jsoncachefolder = joinpaths(cachefolder,"json")
imagecachefolder = joinpaths(cachefolder,"images")
folderstoinitialize = [downloadsfolder, cachefolder, payloadsfolder, jsoncachefolder, imagecachefolder]
#initailize folders if they don't exist
for folder in folderstoinitialize:
	if not os.path.isdir(folder):
		print("initializing folder {}".format(folder))
		os.mkdir(folder)

assetfolder = get_path("assets")
if not os.path.isdir(assetfolder):
	print("error, asset folder not found")

#folders and files for tracking installed apps on the sd
trackingfolder = "hbupdater"
trackingfile = "hbupdater.json"

def checkphoto(dir, photo):
	for s in os.listdir(dir):
		if os.path.splitext(s)[0] == photo and os.path.isfile(os.path.join(dir, s)):
			return s

	return "Not found"
