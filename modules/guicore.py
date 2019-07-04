import modules.HBUpdater as HBUpdater
import os, sys, json, shutil
version = 1.0

#Folder and file definitions for easy access
wd = sys.path[0]
#Folder for local assets
assetfolder =  os.path.join(wd, "assets")

#local
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

def getpilstatus():
	global pilstatus
	return pilstatus

def setpilstatus(status):
	global pilstatus
	pilstatus = status

def setguisetting(newentry, silent = False):
	#open log
	if not silent:
		print("\n updating gui log with {}".format(json.dumps(newentry,indent=4)))
	with open(guisettings, 'r') as jfile:  
		originaljfile = json.load(jfile)

	#update value
	originaljfile = dict(originaljfile, **newentry)

	#write updated log
	with open(guisettings, 'w') as jfile:
		json.dump(originaljfile, jfile, indent=4,)

def checkguisetting(key, value):
	try:
		with open(guisettings, 'r') as json_file:  
			jfile = json.load(json_file)

		try:
			info = jfile[key][value]
		except:
			info = None
	except:
		info = None

	return info



def updateguirepos(newentry):
	#open log
	print("updating repo file with {}".format(json.dumps(newentry,indent=4)))
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

def getreposbygroup(category):
	repos = []
	try:
		with open(repolog, 'r') as json_file:  
			jfile = json.load(json_file)
			for repo in jfile:
				if repo["category"] == category:
					repos.append(repo)
		return repos
	except:
		return None

def getreposbygroupfromlist(category, listy):
	repos = []
	for repo in listy:
		if repo["category"] == category:
			repos.append(repo)
		return repos

def getrepolist():
	try:
		with open(repolog, 'r') as json_file:  
			return json.load(json_file)
	except:
		return None

def makerepolist():
	repolist=[]
	jsonrepolist = getrepolist()
	if not jsonrepolist == None:
		for repo in jsonrepolist:
			if not repo == "created_with":
				repochunk = jsonrepolist[repo]
				repolist.append(repochunk)
	return repolist
		# print("User Repo Data: {}".format(json.dumps(guicore.repolist,indent=4)))
