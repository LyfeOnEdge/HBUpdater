#Copyright LyfeOnEdge 2019
#Licensed under GPL3
#stop script if running without a frontend
import sys, os, shutil, json
from zipfile import ZipFile
from webhandler import download

if __name__ == '__main__':
    sys.exit("This script was not meant to run without a frontend. Exiting...")

#Standard path to find get folder at
PACKAGES_DIR = ".get"
#Name of package info file
PACKAGE_INFO = "info.json"
#Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"
#The prefix used to designate each line in the manifest
MANIFEST_PREFIX = "U: "

DOWNLOADSFOLDER = "downloads"

#python object to hold appstore entrys data
class HBUpdater_handler(object):
    def __init__(self, mode):
        modemap = {
            "SWITCH" : "switch/appstore/.get/packages",
            "GENERIC" : PACKAGES_DIR,
        }
        self.packages_dir = modemap[mode] 
        self.base_install_path = None
        self.packages = None

    def warn_path_not_set(self):
        print("Warning: appstore path not set")

    #Check if the appstore packages folder has been inited
    def check_if_get_init(self):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        packagesdir = os.path.join(self.base_install_path, self.packages_dir)
        try:
            return os.path.isdir(packagesdir)
        except:
            pass

    def init_get(self):
        if not self.check_path(): return self.warn_path_not_set()
        if not self.check_if_get_init():
            packagesdir = os.path.join(self.base_install_path, self.packages_dir)
            os.makedirs(packagesdir)
        else:
            print("Appstore packages dir already inited")
            return

    #Set this to a root of an sd card or in a dir to test
    def set_path(self, path, silent = False):
        self.base_install_path = path
        if not path:
            path = ""
        print("Set SD Root path to %s" % path)
        self.packages = None
        self.get_packages(silent = silent)

    def reload(self):
        self.set_path(self.base_install_path)

    def check_path(self):
        return self.base_install_path



    #Installs an appstore package
    #Paramaters:
    #The repo_entry is a chunk from the appstore json that corresponds to a libget package

    #Optional Parameters:
    #Title function is a call to a gui to set a title for an install screen
    #Progress function is a call to the gui to 
    #The reload function will call a gui reload at the end of the install process
    #Note: don't try to be clever and use a for loop and lambda functions passed to reload_function to essentially chain installs together. It *will* crash.
    def install_package(self, repo_entry, version_index = 0, progress_function = None, reload_function = None, title_function = None, silent = False):
        def do_progress_function(text_string, progress_precent):
            if progress_function:
                try:
                    progress_function(text_string, progress_precent)
                except:
                    pass

        def do_title_function(title_string):
            if title_function:
                try:
                    title_function(title_string)
                except:
                    pass

        if not self.check_path(): return self.warn_path_not_set()

        do_progress_function("Paths set", 10)

        if not repo_entry:
            print("No repo entry data passed to appstore handler.")
            print("Not continuing with install")
            return
        try:
            package = repo_entry["package"]
        except:
            print("Error - package name not found in repo data")
            do_progress_function("Error - package name not found in repo data", 15)
            print("Not continuing with install")
            return

        do_progress_function("Package data passed", 20)

        try:
            version = repo_entry["github_content"][version_index]["tag_name"]
        except:
            print("Error - package version not found in repo data")
            do_progress_function("Error - package version not found in repo data", 25)
            print("Not continuing with install")
            return

        title = "Installing %s" % package
        title +=  " - %s" % version

        do_title_function(title)

        if not self.check_if_get_init():
            print("Get folder not initiated.")
            print("Not continuing with install")
            do_progress_function("Get folder not initiated, not continuing with install.", 25)
            return

        do_progress_function("Get folder found", 30)

        #Uninstall if already installed
        packages = self.get_packages(silent=True)
        if packages:
            if package in packages:
                print("Package already installed, removing for upgrade")
                if not self.uninstall_package(repo_entry):
                    #If uninstall fails
                    print("Uninstall failed.")
                    print("Not continuing with install")
                    do_progress_function("Uninstall failed, not continuing with install.", 35) 
                    return
                do_progress_function("Updating .", 35) 
            else:
                print("Package not previously installed, proceeding...")

        install_message = "Beginning install for package %s" % repo_entry["name"]

        print(install_message)

        do_progress_function(install_message, 50)

        #Append base directory to packages directory
        packagesdir = os.path.join(self.base_install_path, self.packages_dir)
        if not os.path.isdir(packagesdir):
            os.makedirs(packagesdir)
        #Append package folder to packages directory
        packagedir = os.path.join(packagesdir, package)
        if not os.path.isdir(packagedir):
            os.mkdir(packagedir)

        do_progress_function("Downloading package %s" % package, 60)

        #Download the package from github
        downloadedfile = self.getPackage(repo_entry, version_index)
        if not downloadedfile:
            print("Failed to download asset for package {}".format(package))
            do_progress_function("Failed to download asset for package {}".format(package), 70)
            return

        do_progress_function("Extracting...", 70)

        print("Download successful, proceeding...")

        #Move software to sd card
        #Handles data differently depending on file type
        installlocation = self.installfiletosd(downloadedfile, repo_entry["install_subfolder"])

        do_progress_function("Extract complete", 80)

        name = repo_entry["name"]
        print("Installing {}".format(name))

        #parse api link to a github project releases link
        url = parse_api_to_standard_github(repo_entry["release_api"])
        url = url.strip("/") + "/releases"

        #Create empty appstore entry and populate it
        entry = {}
        entry["title"] = name
        entry["author"] = repo_entry["author"]
        entry["category"] = repo_entry["category"]
        entry["license"] = repo_entry["license"]
        entry["description"] = repo_entry["description"]
        entry["url"] = url
        package = repo_entry["package"]
        #Convert github version to store version
        entry["version"] = self.clean_version(version, package)
        
                
        self.create_store_entry(entry,installlocation,package)

        do_progress_function("Wrote package manifest", 90)
        do_progress_function("Wrote package info", 100)

        print("Installed {} version {}".format(repo_entry["name"], version))

        #Refreshes the current packages
        if reload_function:
            reload_function()
        self.reload()

    def installfiletosd(self, filename,subfolder,remove_downloaded_file_after = True):
        def handleMove():
            try:
                if remove_downloaded_file_after:
                    shutil.move(file, sdlocation)
                else:
                    shutil.copy(file, sdlocation)
                print("Successfully copied {} to SD".format(filename))

                if subfolder:
                    return [os.path.join(subfolder,filename)]
                else:
                    return [filename]
            except Exception as e: 
                print("Failed to copy {} to SD ~{}".format(filename, e))
        def handleNRO():
            return handleMove()
        def handlePY():
            return handleMove()
        def handleBIN():
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
            if remove_downloaded_file_after:
                os.remove(file)
            return namelist

        def handle7Z():
            print(".7z archives are not supported yet")

        file = os.path.join("downloads", filename)

        if not subfolder == None:
            subdir = os.path.join(self.base_install_path,subfolder)
        else: 
            subdir = self.base_install_path

        sdlocation = os.path.join(subdir, filename)

        if not os.path.exists(subdir):
            os.makedirs(subdir)

        handlerMAP = {
            ".nro" : handleNRO,
            ".py" : handlePY,
            ".zip" : handleZIP,
            ".7z" : handle7Z,
            ".bin" : handleBIN,
        }

        for ending in handlerMAP:
            if filename.endswith(ending):
                return handlerMAP[ending]()   #<- We should return here

        print("file handling method not found")
        class TypeHandlerNotFound(Exception):
            pass
        raise TypeHandlerNotFound

    #Creates an HBAppstore entry for a given package and manifest
    #Store_entry is a dict in the form defined at the top of the file
    def create_store_entry(self, store_entry, manifest, package):
        basepath = self.base_install_path
        #Append base directory to packages directory
        packagesdir = os.path.join(basepath, self.packages_dir)
        #Append package folder to packages directory
        packagedir = os.path.join(packagesdir, package)
        #Append manifest filename to package folder
        manifest_file = os.path.join(packagedir, PACKAGE_MANIFEST)
        #Append info file filename to package folder
        info_file = os.path.join(packagedir,PACKAGE_INFO)

        #If the package dir hasn't been inited yet, make it
        if not os.path.isdir(packagedir):
            os.makedirs(packagedir)

        #Clean up the manifest lines, ensures line format
        #is consistent with 
        filemanifest = []
        if type(manifest) == str:
            path = manifest.replace("\\","/").strip("/")
            filemanifest.append(path)
        else:
            for file in manifest:
                file = str(file)
                path = file.replace("\\","/").strip("/")
                filemanifest.append(path)
        print(filemanifest)

        #Add the manifest prefix 
        prepped_manifest = []
        #Prep manifest lines with 'U:' marker and write
        with open(manifest_file, 'w+') as mf:
            for entry in filemanifest:
                newline = "{}{}\n".format(MANIFEST_PREFIX,entry)
                prepped_manifest.append(newline)
            mf.writelines(prepped_manifest)
            print("wrote manifest\n")

        #Write info file
        with open(info_file, 'w+') as inf:
            json.dump(store_entry, inf, indent=4,)

        print("Created log entry for {} \n{}".format(package, json.dumps(store_entry,indent=4)))

    #Uninstalls a package given a chunk from the repo
    def uninstall_package(self, repo_entry):
        if not self.check_path(): return self.warn_path_not_set()
        if not repo_entry:
            print("No repo entry data passed to appstore handler.")
            print("Not continuing with uninstall")
            return
        if not self.check_if_get_init():
            print(".get folder not initiated.")
            print("Not continuing with uninstall")
            return

        package = repo_entry["package"]
        if not self.get_package_entry(package):
            print("Could not find package in currently selected location.")
            print("Not continuing with uninstall")
            return

        print("Uninstalling {}".format(package))

        filestoremove = self.get_package_manifest(package)
        if 'str' in str(type(filestoremove)):
            file = os.path.join(self.base_install_path,filestoremove)
            if os.path.isfile(file):  
                os.remove(file)
                print("removed {}".format(file))
        else:
            #Go through the previous ziplist in reverse, this way folders get cleaned up
            for path in reversed(filestoremove):
                file = os.path.join(self.base_install_path,path) 
                if os.path.isfile(file):  
                    os.remove(file)
                    print("removed {}".format(file))
                elif os.path.isdir(file):
                    if not os.listdir(file):
                        os.rmdir(file)
                        print("removed empty directory {}".format(file))

            self.remove_store_entry(package)

        print("Uninstalled package {}".format(package))

        self.reload()
        return True


    #THIS DOES NOT UNINSTALL THE CONTENT
    #Removes a package entry by deleting the package 
    #folder containing the manifest and info.json
    def remove_store_entry(self, package):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        pacdir = os.path.join(self.packages_dir, package)
        #Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        try:
            shutil.rmtree(packagedir, ignore_errors=True)
            print("Removed appstore entry for {}".format(package))
        except Exception as e:
            print("Error removing store entry for {} - {}".format(package, e))

    #Get the contents of a package's info file as a dict
    #Returns none if it doesn't exist
    def get_package_entry(self, package):
        if not self.check_path(): return
        #Append package name to packages directory
        pacdir = os.path.join(self.packages_dir, package)
        #Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        #Append package loc to info file name
        pkg = os.path.join(packagedir, PACKAGE_INFO)

        try:
            with open(pkg, encoding="utf-8") as infojson:
                return json.load(infojson)
        except FileNotFoundError:
            pass
        except Exception as e:
            print("Failed to open repo_entry data for {} - {}".format(package, e))

    #Get a package's json file value, returns none if it fails
    def get_package_value(self, package, value):
        if not self.check_path(): return
        #Get the package json data
        package_info = self.get_package_entry(package)
        #If data was retrieved, return the value
        if package_info:
            # print(package_info[value])
            return package_info[value]

    #Get the installed version of a package, return "not installed" if failed
    def get_package_version(self, package):
        #Get the package json data
        ver = self.get_package_value(package, "version")
        return ver or "not installed"

    #Returns a package's manifest as a list
    def get_package_manifest(self, package):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        pacdir = os.path.join(self.packages_dir, package)
        #Append base directory to packages directory
        packagedir = os.path.join(self.base_install_path, pacdir)
        #Append package loc to manifest file name
        manifestfile = os.path.join(packagedir, PACKAGE_MANIFEST)
        print(manifestfile)
        if not os.path.isfile(manifestfile):
            print("couldn't find manifest")
            return

        mf = []
        #open the manifest, append the current base path to each line
        with open(manifestfile, "r") as maf:
            for fileline in maf:
                fl = fileline.replace(MANIFEST_PREFIX, "")
                fl = fl.strip().replace("\n", "")
                mf.append(os.path.join(self.base_install_path,fl))

        return mf

    def get_packages(self, silent = False):
        if not self.check_path(): return self.warn_path_not_set()
        packagedir = os.path.join(self.base_install_path, self.packages_dir)

        if os.path.isdir(packagedir):
            packages_dir_items = os.listdir(packagedir)

            packages = []
            #Go through items in packages dir
            for possible_package in packages_dir_items:
                #Find the path of the package
                pathed_package = os.path.join(packagedir, possible_package)
                package_json = os.path.join(pathed_package, PACKAGE_INFO)
                #check if the json exists (isfile will result in exception if it doesn't exist, it's unlikely to find a folder named info.json, either way exists() will have to be called)
                if os.path.exists(package_json):
                    packages.append(possible_package)
            self.packages = packages
            if not silent:
                print("Found packages -\n{}".format(json.dumps(packages, indent = 4)))
            return packages

    #Downloads the current zip of a package
    def getPackage(self, repo_entry, version_index):
        try:
            downloadsfolder = DOWNLOADSFOLDER
            if not os.path.isdir(DOWNLOADSFOLDER):
                os.mkdir(DOWNLOADSFOLDER)
            package = repo_entry["name"]
            packageURL = self.findasset(repo_entry["pattern"], repo_entry["github_content"][version_index]["assets"])
            if not packageURL:
                print("Failed to get package asset from list, can't getPackage")
                return
            packagefile = os.path.join(downloadsfolder, "{}.zip".format(package))
            return download(packageURL)
        except Exception as e:
            print("Error getting package zip for {} - {}".format(package, e))

    def clean_version(self, ver, name):
        ver = ver.lower().strip("v")
        if name:
            ver = ver.replace(name.lower(), "") 
        ver = ver.split(" ")[0].replace("switch", "").strip("-")
        return ver

    #matching the pattern or none found
    def findasset(self, pattern, assets, silent = False):
        if not pattern:
            print("No pattern specified")
            return

        if not assets:
            print("no assets specified")
            return

        downloadlink = None

        for asset in assets:
            asseturl = asset["browser_download_url"]
            assetname = asseturl.rsplit("/",1)[1].lower()
            assetwithoutfiletype = assetname.split(".")[0]
            for firstpartpattern in pattern[0]:
                if firstpartpattern.lower() in assetwithoutfiletype.lower():
                    if assetname.endswith(pattern[1].lower()):
                        if not silent:
                            print("found asset: {}".format(assetname))
                        downloadlink = asseturl
                        break
        if downloadlink == None:
            print("No asset data found for pattern {}, can't install\n".format(pattern))

        return downloadlink

    def get_tag_index(self, repo_entry, tag):
        index = 0
        for release in repo_entry:
            if release["tag_name"] == tag:
                return index
            else:
                index += 1
        return -1

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

