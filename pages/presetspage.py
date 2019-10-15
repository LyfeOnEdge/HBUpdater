import os, json
from widgets import ThemedFrame, ThemedListbox, ThemedLabel, searchBox, button, themedScrollingText
import style

#modified searchbox that calls a function to update the json printout
class entrybox(searchBox):
    def __init__(self, frame, placeholder = ""):
        searchBox.__init__(self, frame, placeholder=placeholder, command = None, command_on_keystroke = frame.update_json)

class presetsPage(ThemedFrame):
    def __init__(self, parent, controller):
        self.controller = controller
        self.appstore_handler = controller.appstore_handler
        self.repo_parser = controller.repo_parser


        self.preset_json = None #Holds the value of the json, makes it easy to "reset"
        self.unsaved_preset_json = None


        ThemedFrame.__init__(self,parent)

        self.unincluded_packages_listbox = ThemedListbox(self,foreground=style.b)
        self.included_packages_listbox = ThemedListbox(self, foreground=style.b):

        self.author_name = entrybox(self, placeholder = "Preset Author")
        self.preset_name = entrybox(self, placeholder = "Preset Package Name")
        self.preset_package_version = entrybox(self, placeholder = "Preset Package Version (Optional)")

        self.output_json = themedScrollingText(self)


        save config button
        reset config button
        back button

    def show(self):
        self.place(relwidth=1,relheight=1)

    def hide(self):
        self.place_forget()

    #preset is the path to a json 
    def load(self, preset):
        try:
            with open(preset) as preset_file:
                preset_object = json.load(preset_file)

            self.author_name.set_text(preset_object.get("author"))
            self.preset_package_name.set_text(preset_object.get("preset_package_name"))
            self.preset_package_version.set_text(preset_object.get("preset_package_version"))

        except:
            #Inform user via gui
            print("Error loading preset json ")


        self.show()

    #Gets the page ready to make a new repo
    def new(self):
        self.show()


    def add_package_to_included(package):
        pass
        #remove from unincluded
        #add to included

    def add_packages_to_included(packagelist):
        for package in packagelist:
            add_package_to_included(package)




#Todo:
#Make clicking a listbox item move the item to the other listbox 
    #returns a dict representing the json value of preset package
    def make_json_object(self):
        json_object = {
            "author" : self.author_name.get_text(),
            "preset_package_name" : self.preset_name.get_text(),
            "preset_package_version" : self.preset_package_version.get_text()
        }
        return json_object






#Frame for the main appstore to show list of presets, clicking a preset leads to presets page
class presetsFrame(ThemedFrame):

    presets_listbox

    for each icon display 3 "cards" overlayed at an angle


