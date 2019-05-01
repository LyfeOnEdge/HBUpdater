import homebrewcore
import webhandler
import json


version = 0.1 #guicore version 0.1


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

def addrepo(url,description,subfolder,genre):
	apiurl = webhandler.parse_standard_github_to_api(url)
	if apiurl == None:
		print("error parsing link")
		return
	print(apiurl)
	repo = apiurl.rsplit("/",2)[1]
	author = apiurl.rsplit("/",3)[1]



	newentry = {
					repo : {
						"software" : repo,
						"githuburl" : url,
						"githubapi" : apiurl,
						"author" : author,
						"description" : description,
						"group" : genre,
						"install_subfolder" : subfolder,
					}
			}

	# print(json.dumps(newentry,indent=4))

	updateguirepos(newentry)


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


def updaterepolog(newentry):
	#open log
	print("updating repo file with {}".format(newentry))
	with open(repolog, 'r') as jfile:  
		originaljfile = json.load(jfile)

	#update value
	originaljfile.update(newentry)


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

