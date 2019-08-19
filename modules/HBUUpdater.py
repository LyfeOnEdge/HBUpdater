# This script grabs the latest version of HBU from github
import os, sys, platform, json, shutil
import modules.locations as locations
import modules.webhandler as webhandler
from zipfile import ZipFile
import urllib

hbu_pattern = [["HBUpdater"], ".zip"]

print("HBUpdaterUpdater, Using Python {}.{}".format(sys.version_info[0],sys.version_info[1]))

#Download a file at a url, returns file path
def download(fileURL):
    try:
        downloadedfile, headers = urllib.request.urlretrieve(fileURL)
        print(headers)
        filename = headers["Content-Disposition"].split("filename=",1)[1]
        downloadlocation = os.path.join(locations.downloadsfolder,filename)
        shutil.move(downloadedfile, downloadlocation)
        print("downloaded {} from url {}".format(filename, fileURL))
        return downloadlocation
    except Exception as e: 
        print(e)
        return None

def openJson(file):
    with open(file) as f:
        return json.load(f)

def get_members(zip):
    parts = []
    # get all the path prefixes
    for name in zip.namelist():
        # only check files (not directories)
        if not name.endswith('/'):
            # keep list of path elements (minus filename)
            parts.append(name.split('/')[:-1])
    # now find the common path prefix (if any)
    prefix = os.path.commonprefix(parts)
    if prefix:
        # re-join the path elements
        prefix = '/'.join(prefix) + '/'
    # get the length of the common prefix
    offset = len(prefix)
    # now re-set the filenames
    for zipinfo in zip.infolist():
        name = zipinfo.filename
        # only check files (not directories)
        if len(name) > offset:
            # remove the common prefix
            zipinfo.filename = name[offset:]
            yield zipinfo


def handleZIP(file, extract_dir):
    with ZipFile(file, 'r') as zipObj:
        zipObj.extractall(extract_dir, get_members(zipObj))

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
    return downloadlink

def update():
    try:
        update_url = locations.updateapi
    except:
        update_url = None
    if not update_url:
        sys.exit("Could not find update api url")

    update_file = webhandler.getJson("HBUpdater", locations.updateapi)
    if not update_file: sys.exit("Failed to download update json")

    update_data = openJson(update_file)[0]
    if not update_data: sys.exit("No update data")

    print("Downloading HBUpdater {}".format(update_data["tag_name"]))

    assets = update_data["assets"]

    download_url = findasset(hbu_pattern, assets)

    if not download_url: sys.exit("Failed to find download link in json")

    update_zip = download(download_url)

    handleZIP(update_zip, sys.path[0])

    sys.exit("Update complete!")

# if __name__ == "__main__":
#     update()