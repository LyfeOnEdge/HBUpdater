import modules.webhandler as webhandler
import modules.HBUpdater as HBUpdater
import os, json, shutil
version = 0.2

#variable to hold repo list
repolist = []
#variable to track the current selected repo
currepo = 0
repolistlen = None

guisettings = "guisettings_user.json"
guisettings_default = "guisettings_default.json"
if not os.path.isfile(guisettings):
	print("Gui json not found, initializing")
	shutil.copy(guisettings_default,guisettings)

repolog = "user_repos.json"
if not os.path.isfile(repolog):
	print("Repo json not found, initializing")

	newentry = 	{ "created_with" : version }

	with open(repolog, 'w') as outfile:
	    json.dump(newentry, outfile,indent=4)

pilstatus = None

guiwidth = 

def getpilstatus():
	global pilstatus
	return pilstatus

def setpilstatus(status):
	global pilstatus
	pilstatus = status

def setguisetting(newentry):
	#open log
	print("\n updating gui log with {}".format(json.dumps(newentry,indent=4)))
	with open(guisettings, 'r') as jfile:  
		originaljfile = json.load(jfile)

	#update value
	originaljfile.update(newentry)

	#write updated log
	with open(guisettings, 'w') as jfile:
		json.dump(originaljfile, jfile, indent=4,)

def checkguisetting(software, key):
	try:
		with open(guisettings, 'r') as json_file:  
			jfile = json.load(json_file)

		try:
			info = jfile[software][key]
		except:
			info = None
	except:
		info = None

	return info

def getrepochunkfromurl(url,description,subfolder,genre):
	apiurl = webhandler.parse_standard_github_to_api(url)
	if apiurl == None:
		print("error parsing link")
		return
	print(apiurl)
	repo = apiurl.rsplit("/",2)[1]
	author = apiurl.rsplit("/",3)[1]

	jsonfile = webhandler.getJson(repo, apiurl)

	#make new entry
	chunk = {
			"software" : repo,
			"githuburl" : url,
			"githubapi" : apiurl,
			"githubjson" : jsonfile,
			"github_asset" : None,
			"author" : author,
			"projectpage" : None,
			"description" : description,
			"group" : genre,
			"install_subfolder" : subfolder,
			"zip_items" : None,
			"githubjson" : jsonfile,
			"photopath" : None,
			}
		
	# print(json.dumps(newentry,indent=4))

	return chunk


def updateguirepos(newentry):
	#open log
	print("updating repo file with {}".format(newentry))
	with open(repolog, 'r') as jfile:  
		originaljfile = json.load(jfile)

	#update value
	originaljfile.update(newentry)

	#write updated log
	with open(repolog, 'w+') as jfile:
		json.dump(originaljfile, jfile, indent=4,)

def removeitemfromrepo(software):
    with open(repolog, 'r') as json_file:  
        originaljfile = json.load(json_file)
        del originaljfile[software]
        print("removed {} from repo file".format(software))

    #write updated log
    with open(repolog, 'w+') as jfile:
        json.dump(originaljfile, jfile, indent=4,)

def checkrepotag(software, key):
	try:
		with open(repolog, 'r') as json_file:  
			jfile = json.load(json_file)
		try:
			info = jfile[software][key]
		except:
			info = None
	except:
		info = None

	return info

def getrepoinfo(software):
	try:
		with open(repolog, 'r') as json_file:  
			jfile = json.load(json_file)
		try:
			info = jfile[software]
		except:
			info = None
	except:
		info = None

	return info

def getrepolist():
	try:
		with open(repolog, 'r') as json_file:  
			return json.load(json_file)
	except:
		return None

def makerepodict():
	global repolist
	repolist=[]
	jsonrepolist = getrepolist()
	if not jsonrepolist == None:
		for repo in jsonrepolist:
			if not repo == "created_with":
				repochunk = jsonrepolist[repo]
				repolist.append(repochunk)
	return repolist
		# print("User Repo Data: {}".format(json.dumps(guicore.repolist,indent=4)))
