# github_updater
A python module / git submodule for python applications to grab their updates from github releases

Define the updater's settings in the **same folder** as the module *folder* not in the module folder
The settings file must be called "update_settings.json" and in the form:
{
    "UPDATENAME": "REPO_NAME",
    "UPDATEURL": "https://api.github.com/repos/__AUTHOR__/__REPO__/releases",
    "ASSETPATTERN": [
        [
            "__CONSISTENT_RELEASE_PATTERN__"
        ],
        "CONSISTENT_RELEASE_FILE_TYPE__"
    ]
}