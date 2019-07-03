#LyfeOnEdge's super simple etag handler.
import os, sys, shutil, json
import urllib.request
import modules.locations as locations


#Header for checking if etag is updated
etag_header = "If-None-Match"
#Must set to acess github appi
useragent = 'Mozilla/5.0'

#Feed this the url of a api item that suppots etags and the corresponding file to update
#If there is an update it will update the file, if not it will return the file
#This tool is useful for avoiding api overuse and minimizing bandwidth
def accessETaggedFile(url, file):
    global etag_header
    global useragent

    req = urllib.request.Request(url)
    req.add_header('User-Agent', useragent)

    etag = getEtag(file)

    if etag:
        req.add_header(etag_header, "{}".format(etag))

    try:
        with urllib.request.urlopen(req) as response, open(file, 'wb+') as out_file:
            shutil.copyfileobj(response, out_file)
            headers = response.info()
            newetag = headers["ETag"]
            setEtag(file,newetag)
        print("file {} - Updated".format(file))
    except urllib.error.URLError as e:
        if e.reason == "Not Modified": #304 error, what we want to see if nothing has been updated
            print("file {} - {}".format(file, e.reason))
        else:  
            print("etag download error - {} - {}\n\n".format(file, e.reason))
            return None

    return(file)

#tag is the file path associated with the etag
#etag is tag obtained from last request
def setEtag(tag, etag):
    if not os.path.isfile(locations.etagfile):
        print("No ETag file, initializing")
        with open(locations.etagfile, 'w+', encoding="utf-8") as jfile: 
            newfile = {"created_with" : "lyfe_get"}
            json.dump(newfile, jfile, indent=4,)

    #open log
    newentry = {tag : etag}
    with open(locations.etagfile, 'r', encoding="utf-8") as jfile:  
        originaljfile = json.load(jfile)

    #update value
    originaljfile.update(newentry)

    #write updated log
    with open(locations.etagfile, 'w', encoding="utf-8") as jfile:
        json.dump(originaljfile, jfile, indent=4,)

#tag is path of previously downloaded file, returns file's associated etag or none if not found
def getEtag(tag):
    try:
        with open(locations.etagfile, 'r', encoding="utf-8") as json_file:  
            jfile = json.load(json_file)

        try:
            etag = jfile[tag]
        except:
            etag = None
    except:
        etag = None

    return etag