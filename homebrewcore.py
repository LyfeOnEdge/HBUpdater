import os, sys

def get_path(filename):
	return os.path.join(sys.path[0], filename)

def exists(filename):
	return os.path.isfile(filename)

def joinpaths(prefix,suffix):
	return os.path.join(prefix,suffix)

def direxist(foldername):
    return os.path.isdir(foldername)

#if downloads folder hasn't been made create it
downloadsfolder = get_path("downloads")
if not os.path.isdir(downloadsfolder):
	os.mkdir(downloadsfolder)

cachefolder = get_path("cache")
if not os.path.isdir(cachefolder):
	os.mkdir(cachefolder)

assetfolder = get_path("assets")
if not os.path.isdir(assetfolder):
	print("error, asset folder not found")


jsoncachefolder = joinpaths(cachefolder,"json")
if not os.path.isdir(jsoncachefolder):
	os.mkdir(jsoncachefolder)

imagecachefolder = joinpaths(cachefolder,"images")
if not os.path.isdir(imagecachefolder):
	os.mkdir(imagecachefolder)

trackingfolder = "hbupdater"
trackingfile = "hbupdater.json"

def checkphoto(dir, photo):
	for s in os.listdir(dir):
		if os.path.splitext(s)[0] == photo and os.path.isfile(os.path.join(dir, s)):
			return s

	return "Not found"



# #not used yet, will be useful for grabbing a few things
# def extractTar(tarfilename, target):
# 	if (tarfilename.endswith("tar.gz")):
# 	    tar = tarfilename.open(fname, "r:gz")
# 	    tar.extractall(path = target)
# 	    tar.close()
# 	elif (fname.endswith("tar")):
# 	    tar = tarfilename.open(fname, "r:")
# 	    tar.extractall(path = target)
# 	    tar.close()