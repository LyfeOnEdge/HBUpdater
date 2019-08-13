#Some basic scripts for package managing appstore entries
#Copyright LyfeOnEdge 2019
#Licensed under GPL3
import os, json, shutil

#Standard path to find the appstore at
PACKAGES_DIR = "switch/appstore/.get/packages"
#Name of package info file
PACKAGE_INFO = "info.json"
#Name of pagkade manifest file
PACKAGE_MANIFEST = "manifest.install"
#The prefix used to designate each line in the manifest
MANIFEST_PREFIX = "U: "

version = "1.0"
print("appstore compat version {}".format(version))

#Default appstore entry struct
def appstore_entry():
    struct = {
        "title" : None, #TITLE (NOT ALWAYS PACKAGE NAME)
        "author" : None,
        "category" : None,
        "version" : None,
        "url" : None, # STANDARD GITHUB URL
        "license": None, 
        "description": None,
        "details" : None, 
        "changelog" : None,#LAST GITHUB UPDATE NOTES
    }
    return struct


#Check if the appstore packages folder has been inited
def check_if_get_init(basepath):
    if not basepath: return
    #Append package name to packages directory
    packagesdir = os.path.join(basepath, PACKAGES_DIR)
    try:
        if os.listdir(packagesdir):
            return True
    except:
        pass

#Get the contents of a package's info file as a dict
def get_package_info(basepath, package):
    if not basepath: return
    #Append package name to packages directory
    pacdir = os.path.join(PACKAGES_DIR, package)
    #Append base directory to packages directory
    packagedir = os.path.join(basepath, pacdir)
    #Append package loc to info file name
    pkg = os.path.join(packagedir, PACKAGE_INFO)

    try:
        with open(pkg, encoding="utf-8") as infojson:
            info = json.load(infojson)
        return info
    except FileNotFoundError:
        pass
    except:
        print("Failed to open repo data for {}".format(package))
        return None

#Get a package's json file value, returns none if it fails
def get_package_value(basepath, package, value):
    if not basepath: return
    #Get the package json data
    package_info = get_package_info(basepath, package)
    #If data was retrieved, return the value
    if package_info:
        # print(package_info[value])
        return package_info[value]


#Get the installed version of a package, return "not installed" if failed
def get_package_version(basepath, package):
    #Get the package json data
    ver = get_package_value(basepath, package, "version")
    return ver or "not installed"

#Returns a package's manifest as a list
def get_package_manifest(basepath, package):
    if not basepath: return
    #Append package name to packages directory
    pacdir = os.path.join(PACKAGES_DIR, package)
    #Append base directory to packages directory
    packagedir = os.path.join(basepath, pacdir)
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
            mf.append(os.path.join(basepath,fl))

    return mf

#Creates an HBAppstore entry for a given package and manifest
#Store_entry is a dict in the form defined at the top of the file
def create_store_entry(basepath, store_entry, manifest, package):
    if not basepath: return
    #Append base directory to packages directory
    packagesdir = os.path.join(basepath, PACKAGES_DIR)
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

    print("Created appstore entry for {} \n{}".format(package, json.dumps(store_entry,indent=4)))

#Removes a package entry by deleting the package 
#folder containing the manifest and info.json
def remove_store_entry(basepath, package):
    if not basepath: return
    #Append package name to packages directory
    pacdir = os.path.join(PACKAGES_DIR, package)
    #Append base directory to packages directory
    packagedir = os.path.join(basepath, pacdir)
    try:
        shutil.rmtree(packagedir, ignore_errors=True)
        print("Removed appstore entry")
    except Exception as e:
        print("Error removing store entry for {} - {}".format(package, e))

#Based on vgmoose's version checking script,
#makes github versions conform to appstore versions
def parse_version_to_store_equivalent(ver, name):
    ver = ver.lower().strip("v")
    if name:
        ver = ver.replace(name.lower(), "") 
    ver = ver.split(" ")[0].replace("switch", "").strip("-")
    return ver