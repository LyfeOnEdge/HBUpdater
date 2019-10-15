#Some basic scripts for grabbing icon and screenshot for packages using the appstore site.
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import sys, os

import urllib.request 
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)

APPSTORE_URL = "https://www.switchbru.com/appstore/{}"
IMAGE_BASE_URL = APPSTORE_URL.format("packages/{}/{}")
APPSTORE_PACKAGE_URL = "https://www.switchbru.com/appstore/zips/{}.zip"

DOWNLOADSFOLDER = "downloads"

CACHEFOLDER = "cache"
ICON  = "icon.png"
SCREEN = "screen.png"

lib_path = os.path.dirname(os.path.realpath(__file__))
#To blacklist icons
#create a file in the same folder as this on
#Call it icon_blacklist.txt
#Put the package name you'd like to blacklist on it's own line 
blacklist = os.path.join(lib_path, "icon_blacklist.txt")
ICONBLACKLIST = []
if os.path.isdir(blacklist):
    with open(blacklist) as blacklistfile:
        ICONBLACKLIST = blacklistfile.read()
        print("Loaded icon blacklist {}".format(ICONBLACKLIST))

SCREENBUFFER = {}
ICONBUFFER = {}

def download(url,file,silent = False):
    try:
        urllib.request.urlretrieve(url,file)
        return file
    except Exception as e:
        if not silent:
            print("failed to download file - {} from url - {}, reason: {}".format(file, url, e)) 
        return None

#Gets (downloads or grabs from cache) an image of a given type (icon or screenshot) for a given package
def getImage(package, image_type, force = False):
    path = os.path.join(os.path.join(sys.path[0], CACHEFOLDER), package.replace(":",""))
    if not os.path.isdir(path):
        os.mkdir(path)

    image_file = os.path.join(path, image_type)

    if os.path.isfile(image_file) and not force:
        return(image_file)
    else:
        return download(IMAGE_BASE_URL.format(package, image_type), image_file, silent = True)

def getPackageIcon(package, force = False):
    if not package in ICONBLACKLIST:
        if package in ICONBUFFER.keys():
            return ICONBUFFER[package]
        icon = getImage(package, ICON, force = force)
        ICONBUFFER.update({package : icon})
        return icon

def getScreenImage(package, force = False):
    if package in SCREENBUFFER.keys():
        return SCREENBUFFER[package]
    screen = getImage(package, SCREEN, force = force)
    SCREENBUFFER.update({package : screen})
    return screen

#Downloads the current zip of a package
def getPackage(package):
    try:
        downloadsfolder = os.path.join(sys.path[0], DOWNLOADSFOLDER)
        packageURL = APPSTORE_PACKAGE_URL.format(package)
        packagefile = os.path.join(downloadsfolder, "{}.zip".format(package))
        return download(packageURL, packagefile)
    except Exception as e:
        print("Error getting package zip for {} - {}".format(package, e))

def test(package):
    getScreenImage(package)
    getPackageIcon(package)
    getPackage(package)

if __name__ == "__main__":
    #Test with the appstore
    test("appstore")