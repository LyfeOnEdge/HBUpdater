#file handling
import os, sys, shutil
from zipfile import ZipFile
import json

#stop script if running without a frontend
if __name__ == '__main__':
    sys.exit("This script was not meant to run without a frontend. Exiting...")

version = "1.1"
print("HBUpdater version {}".format(version))

#My modules
from modules.format import *
import modules.locations as locations
import modules.webhandler as webhandler
import modules.appstore as appstore

chosensdpath = None
sdpathset = False

##SD handling (or technically any path)
#update global "chosensdpath"
def setSDpath(sdpath):
    global chosensdpath
    global sdpathset

    if not(str(sdpath) == ""):
        chosensdpath = sdpath
        print("SD path set to: {}".format(str(chosensdpath)))
        sdpathset = True
    else:
        print("invalid path chosen")
        sdpathset = False

    print("sdpathset - {}".format(sdpathset))
    return sdpathset

#Get the SD path
def getSDpath():
    global chosensdpath
    if checkSDset():
        return chosensdpath

#Check if the SD card has been set
def checkSDset():
    global sdpathset
    return sdpathset

def parse_api_to_standard_github(url):
    remove = [
    "api.",
    "/releases",
    "/repos",
    "/latest",
    ]
    try:
        for item in remove:
            url = url.replace(item,"")
        return(url)
    except:
        return None


#The installer uses a "software chunk" to install
#Here is an example based on the Homebrew appstore
# {
#     "software" : "Homebrew Store",
#     "store_equivalent" : "appstore",
#     "githubapi" : "https://api.github.com/repos/vgmoose/hb-appstore/releases", 
#     "author" : "vgmoose", 
#     "projectpage": "https://github.com/vgmoose/hb-appstore/releases",
#     "description" : "A graphical frontend to the get package manager for downloading and managing homebrew on video game consoles, such as the Nintendo Switch and Wii U. This is a replacement to the older Wii U Homebrew App Store.",
#     "group" : TOOL,
#     "install_subfolder": "switch/appstore",
#     "pattern" : [['appstore'],".nro"],
#     "license" : GPL3
#  },


def installitem(sc, suboption):
    global sdpathset
    global chosensdpath

    if not sdpathset: return
    if not chosensdpath: return

    name = sc["software"]
    print("Installing {}".format(name))

    #parse api link to a github project releases link
    url = parse_api_to_standard_github(sc["githubapi"])
    url = url.strip("/") + "/releases"

    #Create empty appstore entry and populate it
    entry = appstore.appstore_entry()
    entry["title"] = name
    entry["author"] = sc["author"]
    entry["category"] = sc["group"]
    entry["license"] = None
    entry["description"] = sc["description"]
    entry["url"] = url
    package = sc["store_equivalent"]
 
    #open the repo file
    with open(sc["githubjson"], encoding="utf-8") as repo_file: 
        repo = json.load(repo_file)    

    ver = repo[suboption]["tag_name"]

    entry["details"] = repo[suboption]["body"]

    assets = repo[suboption]["assets"]
    if assets == None:
        print("Could not find asset data for selected software")
        return


    if sc["pattern"] == None:
        print("no asset pattern specified for repo")
        return

    #Find the correct asset in the list of assets pulled from the repo json
    downloadlink = findasset(sc["pattern"], assets)

    if not downloadlink:
        return

    downloadedfile = webhandler.download(downloadlink)

    #If download failed return
    if downloadedfile == None:
        print("Asset download failed, not installing")
        return

    print("Download successful, proceeding...")

    filestoremove = appstore.get_package_manifest(chosensdpath, package)
    if filestoremove:
        if 'str' in str(type(filestoremove)):
            file = os.path.join(chosensdpath,filestoremove)
            if os.path.isfile(file):  
                os.remove(file)
                print("removed {}".format(file))
        else:
            #Go through the previous ziplist in reverse, this way folders get cleaned up
            for path in reversed(filestoremove):
                file = os.path.join(chosensdpath,path) 
                if os.path.isfile(file):  
                    os.remove(file)
                    print("removed {}".format(file))
                elif os.path.isdir(file):
                    if not os.listdir(file):
                        os.rmdir(file)
                        print("removed empty directory {}".format(file))

    #Move software to sd card
    #Handles data differently depending on file type
    installlocation = installfiletosd(downloadedfile, sc["install_subfolder"])

    #Convert github version to store version
    entry["version"] = appstore.parse_version_to_store_equivalent(ver, package)
    appstore.create_store_entry(chosensdpath,entry,installlocation,package)



def installfiletosd(filename,subfolder):
    global chosensdpath

    file = os.path.join(locations.downloadsfolder, filename)

    if not subfolder == None:
        subdir = os.path.join(chosensdpath,subfolder)
    else: 
        subdir = chosensdpath

    sdlocation = os.path.join(subdir, filename)

    if not os.path.exists(subdir):
        os.makedirs(subdir)


    def handleMove():
        try:
            shutil.move(file, sdlocation)
            print("Successfully copied {} to SD".format(filename))

            if subfolder:
                return [os.path.join(subfolder,filename)]
            else:
                return [filename]
        except: 
            print("Failed to copy {} to SD".format(filename) )
            return None
    def handleNRO():
        return handleMove()
    def handlePY():
        return handleMove()

    def handleZIP():
        with ZipFile(file, 'r') as zipObj:
            zipObj.extractall(subdir)
            print("Sucessfully extracted {} to SD".format(filename))
            sdlocation = zipObj.namelist()
            namelist = []
            for location in sdlocation:
                if subfolder:
                    namelist.append(os.path.join(subfolder,location))
                else:
                    namelist.append(location)
            print("files copied: \n {}".format(namelist))
            return namelist

    #Useless, 7z must be compiled
    # def handle7Z():
    #     import libarchive.public

    #     with libarchive.public.file_reader(file) as e:
    #         for entry in e:
    #             with open('/tmp/' + str(entry), 'wb') as f:
    #                 for block in entry.get_blocks():
    #                     f.write(block)
    #         return None


    handlerMAP = {
        ".nro" : handleNRO,
        ".py" : handlePY,
        ".zip" : handleZIP,
        # ".7z" : handle7Z,
    }

    for ending in handlerMAP:
        if filename.endswith(ending):
            return handlerMAP[ending]()   #<- We should return here

    print("file handling method not found")

    raise

def uninstallsoftware(package):
    global sdpathset
    global chosensdpath
    if not sdpathset:
        print("SD path not set, can't uninstall")
        return
    if not chosensdpath:
        print("SD path is invalid, can't uninstall")
    
    filestoremove = appstore.get_package_manifest(chosensdpath, package)
    if 'str' in str(type(filestoremove)):
        file = os.path.join(chosensdpath,filestoremove)
        if os.path.isfile(file):  
            os.remove(file)
            print("removed {}".format(file))
    else:
        #Go through the previous ziplist in reverse, this way folders get cleaned up
        for path in reversed(filestoremove):
            file = os.path.join(chosensdpath,path) 
            if os.path.isfile(file):  
                os.remove(file)
                print("removed {}".format(file))
            elif os.path.isdir(file):
                if not os.listdir(file):
                    os.rmdir(file)
                    print("removed empty directory {}".format(file))

        appstore.remove_store_entry(chosensdpath, package)

        print("removed {}".format(package))

#takes a pattern in form [[fp1, fp2, fp2], .extention] and an assets list 
#from a specific version from a repo object, returns the url of the asset
#matching the pattern or none found
def findasset(pattern, assets):
    if not pattern:
        print("No pattern specified")
        return

    if not assets:
        print("no repo json specified")
        return

    downloadlink = None

    for asset in assets:
        asseturl = asset["browser_download_url"]
        assetname = asseturl.rsplit("/",1)[1].lower()
        assetwithoutfiletype = assetname.split(".")[0]
        for firstpartpattern in pattern[0]:
            if firstpartpattern.lower() in assetwithoutfiletype.lower():
                if assetname.endswith(pattern[1].lower()):
                    print("found asset: {}".format(assetname))
                    downloadlink = asseturl
                    break
    if downloadlink == None:
        print("No asset data found for pattern {}, can't install\n".format(pattern))

    return downloadlink


#Check package version
#returns "not installed" if no data found or sd path not set
def get_app_status(package):
    global sdpathset
    if not sdpathset: return "not installed"
    global chosensdpath
    return appstore.get_package_version(chosensdpath, package)