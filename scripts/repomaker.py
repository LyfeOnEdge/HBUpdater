import repos
import webhandler
import requests
import getpass
import json, shutil, os, sys
REPOFILENAME = "repos.json"
OLDREPOFILENAME = "repos_old.json"
OAUTHFILE = "oauth"

new_repo = os.path.join(sys.path[0], REPOFILENAME)
old_repo = os.path.join(sys.path[0], OLDREPOFILENAME)

if not os.path.isdir("downloads"):
    os.mkdir("downloads")

# def get_authorization():
#     username = input('Github username: ')
#     password = getpass.getpass('Github password: ')
#     note = input('Note (optional): ')

#     url = 'https://api.github.com/authorizations'
#     payload = {}
#     if note:
#         payload['note'] = note
#     res = requests.post(
#         url,
#         auth = (username, password),
#         data = json.dumps(payload),
#         )
#     #
#     # Parse Response
#     #
#     j = json.loads(res.text)
#     if res.status_code >= 400:
#         msg = j.get('message', 'UNDEFINED ERROR (no error description from server)')
#         print('ERROR: %s' % msg)
#         return
#     token = j['token']
#     print ('New token: %s' % token)
#     return token

def make_repo():
    new_dict = {
        "homebrew" : repos.homebrewlist,
        "emulators" : repos.emulist,
        "games" : repos.gameslist,
        "media" : repos.medialist,
        "python" : repos.nxpythonlist,
        "cfw" : repos.customfirmwarelist,
        "payloads" : repos.payloadlist,
    }

    for genre in new_dict.keys():
        for software_item in new_dict[genre]:
            updatefile = webhandler.getJson(software_item["name"], software_item["githubapi"])
            if not updatefile:
                sys.exit("ERROR BUILDING REPO FILE: Failed to get json for {}".format(software_item["name"]))
            with open(updatefile, encoding = "utf-8") as update_file_object:
                json_data = json.load(update_file_object)
            software_item["github_content"] = json_data
            software_item["downloads"] = get_downloads(software_item, json_data)

    old_dict = None
    if os.path.isfile(new_repo):
        with open(new_repo) as old:
            old_dict = json.load(old)

    #if the repo has changed
    if new_dict == old_dict:
        print("No data has changed.")
    else:
        print("Content has changed, updating repo {}".format(REPOFILENAME))

        #Make 1-instance backup
        if os.path.isfile(new_repo):
            shutil.move(new_repo, old_repo)

        #Print the new data
        print(json.dumps(new_dict, indent=4))

        with open(REPOFILENAME, 'w+') as outfile:
            json.dump(new_dict, outfile, indent=4)

def get_downloads(software_item, json_data):
    ttl_dls = 0
    try:
        for release in json_data:
            asset = findassetchunk(software_item["pattern"], release["assets"])
            if asset:
                ttl_dls += asset["download_count"]
    except:
        print("Error getting downloads for {}".format(software_item["name"]))
    return ttl_dls

#matching the pattern or none found
def findassetchunk(pattern, assets):
    if not pattern:
        return

    if not assets:
        return

    for asset in assets:
        asseturl = asset["browser_download_url"]
        assetname = asseturl.rsplit("/",1)[1].lower()
        assetwithoutfiletype = assetname.split(".")[0]
        for firstpartpattern in pattern[0]:
            if firstpartpattern.lower() in assetwithoutfiletype.lower():
                if assetname.endswith(pattern[1].lower()):
                    return asset




if __name__ == '__main__':
    with open(OAUTHFILE) as f:
        oauth_token = f.read()

    if oauth_token:
        webhandler.start(['Authorization', 'token %s' % oauth_token])
        make_repo()
    else:
        print("No token")
