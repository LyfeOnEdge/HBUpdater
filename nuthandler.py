import webhandler, homebrewcore, HBUpdater, locations, guicore
from zipfile import ZipFile
import sys, os, json, subprocess,imp
import threading



nutfolder = homebrewcore.get_path("nut")
if not os.path.isdir(nutfolder):
    os.mkdir(nutfolder)
    print("initializing nut folder")


def checkifnutdownloaded():
    if guicore.checkguitag("nut", "version") == "not installed" or guicore.checkguitag("nut", "version") == "none":
        return True
    return False

def checkifmoduleinstalled(module):
    try:
        imp.find_module(module)
        return True
    except ImportError:
        print("module {} not installed".format(module))
        return False


def installpipmodule(module):
    try:
        print("installing {} via pip".format(module))
        print(subprocess.call([sys.executable, "-m", "pip", "install", module]))
        return(True)
    except:
        print("Error installing module")
        return(False)


def downloadnutandinstalldependencies():
    nutjson = webhandler.getJson("nut", locations.nutserverdict["githubapi"])
    with open(nutjson) as json_file: #jsonfile is path, json_file is file obj
        jfile = json.load(json_file)
        if jfile == [] or jfile == None:
            print("Error: empty json nut file")
            return

        zipurl = jfile[0]["zipball_url"]
        version = jfile[0]["tag_name"]
        if zipurl == None:
            print("zip file url invalid, can't download nut assets")

        nutzip = webhandler.download(zipurl)
        nutzip = homebrewcore.joinpaths(homebrewcore.downloadsfolder, nutzip)

        with ZipFile(nutzip, 'r') as zipObj:
            zipObj.extractall(nutfolder)
            print("Sucessfully extracted {} to nut folder\n".format(nutzip))

            extractedfiles = zipObj.namelist()

            serverfile = None
            for possibleserverfile in extractedfiles:
                if possibleserverfile == extractedfiles[0] + "server.py":
                    serverfile = possibleserverfile
            if serverfile == None:
                print("Could not find server file in extracted files")
                return 

            serverfile = homebrewcore.joinpaths(nutfolder, serverfile)

        newentry = {
            "nut" : {
                "version": version,
                "location": serverfile,
            }
        }
        guicore.updateguilog(newentry)

    print("checking nut dependencies")


    threads = []
    for dependency in locations.nutserverdict["dependencies"]:
        if not checkifmoduleinstalled(dependency):
            modulethread = threading.Thread(target=installpipmodule, args=(dependency,))
            threads.append(modulethread)

    # Start all threads
    if not threads == []:
        for thread in threads:
            thread.start()
        # Wait for all of them to finish
        for thread in threads:
            thread.join()


def startnut():
    if checkifnutdownloaded():
        print("Nut server not installed, downloading")
        downloadnutandinstalldependencies()
        

    script_path = guicore.checkguitag("nut", "location")
    print("starting nut server")
    subprocess.Popen([sys.executable,script_path])