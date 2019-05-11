import homebrewcore 
import webhandler
import json
version = 0.2

#variable to hold repo list
repolist = []
#variable to track the current selected repo
currepo = 0
repolistlen = None

guilog = "guilog_user.json"
guilog_default = "guilog_default.json"
if not homebrewcore.exists(guilog):
	print("Gui json not found, initializing")
	shutil.copy(guilog_default,guilog)

repolog = "user_repos.json"
if not homebrewcore.exists(repolog):
	print("Gui json not found, initializing")

	newentry = 	{ "created_with" : version }

	with open(repolog, 'w') as outfile:
	    json.dump(newentry, outfile,indent=4)

newrepotempvariable = {}

hbdict = []
softwarechunknumber = 0 #variable to track where we are in the list of homebrew
dictlen = 0 

tagversionnumber = 0 #variable to track currently selected tag number
taglen=0 #variable to track number of items in version listbox 

ijdict = []
payloadchunknumber = 0
ijdictlen = 0

payloadinjector = []



def setDict(dicty):
	global hbdict
	global dictlen
	hbdict = dicty
	# print(json.dumps(hbdict, indent=8))
	dictlen = len(hbdict)

def setIJDict(dicty):
	global ijdict
	global ijdictlen
	ijdict = dicty
	# print(json.dumps(ijdict, indent=8))
	ijdictlen = len(ijdict)

def setPayloadInjector(dicty):
	global payloadinjector
	payloadinjector = dicty





def updateguilog(newentry):
	#open log
	print("updating gui log with {}".format(newentry))
	with open(guilog, 'r') as jfile:  
		originaljfile = json.load(jfile)

	#update value
	originaljfile.update(newentry)

	#write updated log
	with open(guilog, 'w') as jfile:
		json.dump(originaljfile, jfile, indent=4,)

def checkguitag(software, key):
	try:
		with open(guilog, 'r') as json_file:  
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
