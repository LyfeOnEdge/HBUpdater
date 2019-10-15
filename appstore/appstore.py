#Some basic scripts for installing appstore zips given the package name
#Loosely based on vgmoose's libget here: https://github.com/vgmoose/libget
#Copyright LyfeOnEdge 2019
#Licensed under GPL3

import sys, os, shutil, json
from zipfile import ZipFile
from .appstore_web import getPackage

#Standard path to find the appstore at
PACKAGES_DIR = "switch/appstore/.get/packages"
#Name of package info file
PACKAGE_INFO = "info.json"
#Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"
#The prefix used to designate each line in the manifest
MANIFEST_PREFIX = "U: "

#python object to hold appstore entrys data
class appstore_handler(object):
    def __init__(self):
        self.base_install_path = None
        self.packages = None

    def warn_path_not_set(self):
        print("Warning: appstore path not set")

    #Check if the appstore packages folder has been inited
    def check_if_get_init(self):
        if not self.check_path(): return self.warn_path_not_set()
        #Append package name to packages directory
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        try:
            return os.path.isdir(packagesdir)
        except:
            pass

    def init_get(self):
        if not self.check_path(): return self.warn_path_not_set()
        if not self.check_if_get_init():
            packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
            os.makedirs(packagesdir)
        else:
            print("Appstore packages dir already inited")
            return

    #Set this to a root of an sd card or in a dir to test
    def set_path(self, path):
        self.base_install_path = path
        print("Set SD Root path to %s" % path)
        self.packages = None
        self.get_packages()

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
    def install_package(self, repo_entry, progress_function = None, reload_function = None, title_function = None, silent = False):
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
            package = repo_entry["name"]
        except:
            print("Error - package name not found in repo data")
            do_progress_function("Error - package name not found in repo data", 15)
            print("Not continuing with install")
            return

        do_progress_function("Package data passed", 20)

        try:
            version = repo_entry["version"]
        except:
            print("Error - package version not found in repo data")
            do_progress_function("Error - package name not found in repo data", 25)
            print("Not continuing with install")
            return

        title = "Installing %s" % package
        if version:
            title +=  " - %s" % version

        do_title_function(title)

        if not self.check_if_get_init():
            print("Get folder not initiated.")
            print("Not continuing with install")
            do_progress_function("Get folder not initiated, not continuing with install.", 25)
            return

        do_progress_function("Get folder found", 30)

        #Uninstall if already installed
        if package in self.get_packages(silent=True):
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
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        if not os.path.isdir(packagesdir):
            os.makedirs(packagesdir)
        #Append package folder to packages directory
        packagedir = os.path.join(packagesdir, package)
        if not os.path.isdir(packagedir):
            os.mkdir(packagedir)

        do_progress_function("Downloading package %s" % package, 60)

        #Download the package from the switchbru site
        appstore_zip = getPackage(package)
        if not appstore_zip:
            print("Failed to download zip for package {}".format(package))
            return

        do_progress_function("Extracting...", 70)

        with ZipFile(appstore_zip) as zipObj:
            namelist = zipObj.namelist()
            #Easy check to see if info and manifest files are in the zip
            if not PACKAGE_MANIFEST in namelist:
                print("Failed to find package manifest in zip... Stopping install, no files have been changed on the SD card")
                return
            if not PACKAGE_INFO in namelist:
                print("Failed to find package info in zip... Stopping install, no files have been changed on the SD card")
                return

            #Extract everything but the manifest and the info file
            extract_manifest = [] 
            for filename in zipObj.namelist():
                if filename == PACKAGE_MANIFEST or filename == PACKAGE_INFO:
                    pass
                else:
                    zipObj.extract(filename, path = self.base_install_path)
                    extract_manifest.append(filename)

            print("Extracted: {}".format(json.dumps(extract_manifest, indent = 4)))

            do_progress_function("Extract complete", 80)
                
            #Extract manifest
            zipObj.extract(PACKAGE_MANIFEST, path = packagedir)
            print("Wrote package manifest.")
            do_progress_function("Wrote package manifest", 90)

            #Extract info file
            zipObj.extract(PACKAGE_INFO, path = packagedir)
            print("Wrote package info.")
            do_progress_function("Wrote package info", 100)

        print("Installed {} version {}".format(repo_entry["title"], version))

        #Refreshes the current packages
        if reload_function:
            reload_function()
        self.reload()

    #Uninstalls a package given a chunk from the repo
    def uninstall_package(self, repo_entry):
        if not self.check_path(): return self.warn_path_not_set()
        if not repo_entry:
            print("No repo entry data passed to appstore handler.")
            print("Not continuing with uninstall")
            return
        if not self.check_if_get_init():
            print("Appstore get folder not initiated.")
            print("Not continuing with uninstall")
            return

        package = repo_entry["name"]
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
        pacdir = os.path.join(PACKAGES_DIR, package)
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
        pacdir = os.path.join(PACKAGES_DIR, package)
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
        pacdir = os.path.join(PACKAGES_DIR, package)
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
        packagedir = os.path.join(self.base_install_path, PACKAGES_DIR)

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

    def edit_info(self, package, key, value):
        if not self.check_path(): return self.warn_path_not_set()
        packagedir = os.path.join(self.base_install_path, PACKAGES_DIR)
        packagesdir = os.path.join(self.base_install_path, PACKAGES_DIR)
        packagedir = os.path.join(packagesdir, package)
        pkg = os.path.join(packagedir, PACKAGE_INFO)

        try:
            with open(pkg, encoding="utf-8") as infojson:
                info = json.load(infojson)
        except Exception as e:
            print("Failed to open info data for {} - {}".format(package, e))
            return

        info[key] = value

        with open(pkg, "w", encoding ="utf-8") as infojson:
            json.dump(info, infojson)

        print(json.dumps(info, indent = 4))


    def clean_version(self, ver, name):
        ver = ver.lower().strip("v")
        if name:
            ver = ver.replace(name.lower(), "") 
        ver = ver.split(" ")[0].replace("switch", "").strip("-")
        return ver