from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.webhandler as webhandler
import modules.customwidgets as cw
import pages.pagetemplate as pt
import json

import os

import tkinter as tk
from tkinter.constants import *

details_guide_text = """
This page shows your custom github repos.
"""


assetguidetext = """Begin by chosing the asset you wish to manage from the list. Click "SELECT", and the pattern boxes will be filled out.

If the asset's file name doesn't change between release versions simply selecting the
asset should be enough since the auto-filled pattern and extension will always match.

If not, HBUpdater uses a pattern-based system to select the correct asset between releases.
The first box should contain a consistent pattern to to find the asset by.
The second box should contain the file's extension (eg .nro, .zip, .py, etc)
For example:
    If a repo offers 
        homebrew-switch_v231_0938.nro, 
        homebrew-psp_v231_0938.tuv,
        homebrew-xbx_v231_0938.xyz
    You would select the switch asset, remove the version number (_v231_0938) and specify the file type.
    You would be left with 'homebrew-switch' in the first box and '.nro' in the second.
"""

softwarename_placeholder = "Repo Name"
new_url_placeholder = "Repo URL in format: https://www.github.com/author/repo"
new_subfolder_placeholder = "SD subfolder (blank for root)"
new_genre_placeholder = "Genre"
new_description_placeholder = "(Optional) Repo Description"


class addrepoPage(pt.page):
    def __init__(self, parent, controller,page_name,back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            page_title="YOUR REPOS",
            page_name=page_name,
            primary_button_command=self.on_new_button,
            primary_button_text="NEW",
            genre_function=self.get_category,
            noimage=True,
            nodetail=True,
            # version_function=self.get_store_installed_version
            )
        self.bind("<<ShowFrame>>", self.on_show_frame)

        self.repoVar = {}
        self.return_frame = "homePage"
        self.maintable.place_forget()
        self.infobox.place_forget()
        self.details_frame.place_forget()
        self.details_right_column.place_forget()

        self.trashimage = tk.PhotoImage(file=os.path.join(guicore.assetfolder, "trash.png")).subsample(2)


        self.list_buttons_frame.etc_button.setcommand(lambda: self.controller.frames["errorPage"].getanswer(self.page_name,"Are you sure you want to delete this repo?",self.delete))
        self.list_buttons_frame.etc_button.setimage(self.trashimage)

        buttonlist = [
            {
            "image" : self.returnimage,
            "callback" : lambda: self.controller.show_frame(self.return_frame),
            "tooltip" : "Back to home screen",
            },
        ]
        self.setbuttons(buttonlist)
        

        #usage guide
        self.details_guide = cw.ScrolledText(self.main_right_column,borderwidth=0,highlightthickness=0,background=light_color,foreground=guidetextcolor,wrap=WORD,font=details_guide_font)
        self.details_guide.place(relwidth=1,relheight=1,height=-(2*(navbuttonheight+separatorwidth)+separatorwidth))
        
        self.setguidetext(details_guide_text)

        #Make a list of user repos, populate it from the github json, set it as software list 
        repolist = guicore.makerepolist()
        repolist = self.populatesoftwarelist(repolist)
        self.setlist(repolist)

        #generate table with column labels from list, status column name can be set in declaration
        columns = ["REPO", "CATEGORY", "SUBFOLDER"]

        self.list_frame = cw.ThemedFrame(self.content_frame,frame_highlightthickness=0)
        self.list_frame.place(relx=0,rely=0,y=searchboxheight, relheight=1, height=-(searchboxheight),relwidth=1)

        self.listbox_list = []
        self.maintable = cw.themedtable(self.list_frame, columns, 100)
        self.maintable.place(relheight=1,relwidth=1)
        #bind listboxes to move with mouse scroll
        for column in columns:
            self.maintable.listboxes[column].bind("<MouseWheel>", self.OnMouseWheel)
            # self.listbox_list.append(self.maintable.listboxes[column])

        #set listboxes to easy names
        for listbox in self.maintable.listboxes:
            self.listbox_list.append(self.maintable.listboxes[listbox])

        # self.listboxlist = self.maintable.listboxes
        self.genre_listbox = self.maintable.listboxes["CATEGORY"]

        self.software_listbox = self.maintable.listboxes["REPO"]
        self.software_listbox.bind('<<ListboxSelect>>',self.CurSelet)

        self.latest_listbox = cw.ThemedListbox(self)
        self.status_listbox = self.maintable.listboxes["SUBFOLDER"]


#Page frame for adding new repo
        self.addreposcreen = cw.ThemedFrame(self.outer_frame,background_color=light_color)
        self.addreposcreen.place(x=0,y=0,relwidth=1,relheight=1)

        self.softwarename_box = cw.entrybox(self.addreposcreen, placeholder=softwarename_placeholder,)
        self.softwarename_box.place(relx=0.00,relwidth=.333,y=separatorwidth,height=entryheight,width=-2*separatorwidth,x=+separatorwidth)

        self.new_urlbox = cw.entrybox(self.addreposcreen, placeholder=new_url_placeholder, )
        self.new_urlbox.place(relx=0.334, y = separatorwidth, relwidth=.666, height=entryheight, width=-separatorwidth)

        self.new_descriptionbox = cw.entrybox(self.addreposcreen, placeholder=new_description_placeholder)
        self.new_descriptionbox.place(relx=0, y = 2*(entryheight+2*separatorwidth), relwidth=1, height=entryheight, width=-2*separatorwidth,x=+separatorwidth)

        self.download_github_button = cw.navbutton(self.addreposcreen,command_name = lambda: self.download_json_then_list_assets(), text_string="NEXT")
        self.download_github_button.place(relx=0,rely=0,y=3*(entryheight+2*separatorwidth),x=+separatorwidth,height=entryheight,width=3*entryheight)

        #What subfolder do you want the asset to install to?
        "Select install subfolder (omit leading /)\nKeep in mind some .zips already contain\nthe necessary subfolders and should be\n unzipped to the SD root"
        subfolders = [
        "atmosphere",
        "ReiNX",
        "switch",
        "switch/PyNX",
        "sxos",
        ]
        self.subfolder_dropdown = cw.cbox(self.addreposcreen, subfolders, "subfolder (blank for root)")
        self.subfolder_dropdown.place(relx=0.00,relwidth=.333,y=(entryheight+2.5*separatorwidth),height=entryheight,width=-2*separatorwidth,x=+separatorwidth)


        #Which description do you want your app to have
        """Select homebrew genre (optional)"""
        genres = [
        "app",
        "emu",
        "experimental",
        "game",
        "homebrew",
        "interpreter",
        "mod",
        "other",
        "patch",
        "save manager",
        "script",
        "tool",
        "video player",
        "shoutouts to simpleflips",
        "twitch.tv/simpleflips"
        ]
        self.genres_dropdown = cw.cbox(self.addreposcreen, genres, "genre (up to you)")
        self.genres_dropdown.place(relx=0.334,relwidth=.333,y=(entryheight+2.5*separatorwidth),height=entryheight,width=-separatorwidth)


        #Which page does the repo appear on?
        """Select page to display repo on"""
        categories = [
        "homebrew",
        "emulator",
        "game",
        "python",
        "cfw"
        ]
        self.category_dropdown = cw.cbox(self.addreposcreen, categories, "display page")
        self.category_dropdown.place(relx=0.667,relwidth=.333,y=(entryheight+2.5*separatorwidth),height=entryheight,width=-separatorwidth)
        self.category_dropdown.disabletext()
        # self.category_dropdown.set_text(categories[0])

        self.assetsframe = cw.ThemedFrame(self.addreposcreen,background_color=light_color)   

        self.titleframe = cw.ThemedFrame(self.assetsframe,background_color=light_color)
        self.titleframe.place(relx=0.25, rely=0, x=-5*entryheight, y=0, width = 10*entryheight, height=entryheight)
        self.title = tk.Label(self.titleframe,foreground=w,background=light_color,text="Repo Assets",font=giantboldtext)
        self.title.place(x=0,y=0,relwidth=1,relheight=1)

        self.assetslistbox = cw.ScrolledListBox(self.assetsframe)
        self.assetslistbox.place(x=0,relwidth=0.5,relheight=1,y=+entryheight+separatorwidth, height = -2*(entryheight+separatorwidth))
        self.assetslistbox.bind('<<ListboxSelect>>',self.AssetSelect)    

        # self.assetsguide = cw.ThemedLabel(self.assetsframe, "^Select github asset you wish to manage with this repo. \n This relies on the repo's developer releasing the app with a consistent format.",)
        # self.assetsguide.place(x=0,rely=1,y=-(2*navbuttonheight+separatorwidth), relwidth=1,height=navbuttonheight)
        self.select_asset_button = cw.navbutton(self.assetsframe, text_string="SELECT", command_name=lambda: self.selectasset())
        self.select_asset_button.place(rely=1,y=-(entryheight), relx=0.25,x=-(1.5*navbuttonheight),height=entryheight,width=3*navbuttonheight)

        #Not placed until needed
        self.asset_pattern_frame = cw.ThemedFrame(self.assetsframe,background_color=light_color)
        self.asset_pattern_frame.place(relx=0.5, x=+separatorwidth, y=0, relheight=1, relwidth=0.5, width=-separatorwidth)

        self.asset_guide = cw.ScrolledText(self.asset_pattern_frame,borderwidth=0,highlightthickness=0,background=light_color,foreground=guidetextcolor,wrap=WORD,font=details_guide_font)
        self.asset_guide.place(relx=0, rely=0, relheight=1, height=-entryheight,relwidth=1)
        self.asset_guide.insert(END,assetguidetext)
        self.asset_guide.configure(state=DISABLED)


        self.asset_pattern_firstpart_box = cw.entrybox(self.asset_pattern_frame,placeholder="pattern (filename)",justification='right')
        self.asset_pattern_firstpart_box.place(relx=0,rely=1,y=-entryheight,height=entryheight,relwidth=0.5)

        self.asset_pattern_lastpart_box = cw.entrybox(self.asset_pattern_frame,placeholder=".extension")
        self.asset_pattern_lastpart_box.place(relx=0.5,x=+separatorwidth,rely=1,y=-entryheight, height=entryheight, relwidth=0.5,width=-separatorwidth)

        self.returnbuttonframe = cw.ThemedFrame(self.addreposcreen)
        self.returnbuttonframe.place(relx=1,rely=1,x=-(separatorwidth+navbuttonheight), y=-(separatorwidth+entryheight),height=entryheight, width=navbuttonheight)
        self.returntoreposcreenbutton = cw.navbutton(self.returnbuttonframe,image_object=self.returnimage,command_name=lambda: self.showmainreposcreen())
        self.returntoreposcreenbutton.place(relwidth=1,relheight=1)

        self.addrepobuttonframe = cw.ThemedFrame(self.addreposcreen,background_color=light_color)
        self.addrepobuttonframe.place(relx=0.5, rely=1, x=-5*entryheight, y=-(entryheight+separatorwidth), width = 10*entryheight, height=entryheight)
        self.addrepobutton = cw.navbutton(self.addrepobuttonframe, text_string="ADD REPO", command_name=lambda: self.addrepo())
        self.addrepobutton.place(x=0,y=0,relwidth=1,relheight=1)

        self.content_frame.tkraise()

    def show_assets_frame(self):
        self.assetsframe.place(x=+separatorwidth,y=4*(entryheight+2*separatorwidth),relwidth=1, width=-2*separatorwidth,height=-5*(entryheight+2*separatorwidth),relheight=1)
        self.selected_asset = None

    def hide_assets_frame(self):
        self.assetsframe.place_forget()

    #Update page whenever it is raised
    def on_show_frame(self,event):
        listbox = self.software_listbox
        listbox.selection_set(0)
        listbox.activate(0)
        listbox.see(0)

        self.refreshwindow()
        self.populaterepobox()
    
    #Function to properly raise page so the back command works
    def raiseRepo(self, return_screen, category):
        self.return_frame = return_screen
        self.category_dropdown.set_text(category)
        

    #Functions to hide and show the info box when entering and leaving the add-repo screen
    def hideinfobox(self):
        self.rightcolumn.place_forget()

    def showinfobox(self):
        self.rightcolumn.place(relx=1, x=-infoframewidth, rely=0.0, relheight=1, width=infoframewidth)

    def get_category(self,chunk):
        return chunk["category"]

    #Redefinition of updateinfobox to nullify it
    def updateinfobox(self):
        self.updatelistboxcursor()

    #Populates listbox then calls setrepostrings()
    def populaterepobox(self):
        self.latest_listbox.configure(state=NORMAL)
        self.genre_listbox.configure(state=NORMAL)
        self.status_listbox.configure(state=NORMAL)

        for listbox in self.listbox_list:
            listbox.delete(0,END)
        if not self.softwarelist == None:
            for repo in self.softwarelist:
                    softwarename = repo["software"]
                    author = repo["author"]
                    group = repo["group"]
                    subfolder = repo["install_subfolder"]
                    if subfolder == None or subfolder == "":
                        subfolder = "root"
                    self.software_listbox.insert(END, softwarename)

                    self.latest_listbox.insert(END,author)

                    self.genre_listbox.insert(END,group)
                    self.status_listbox.insert(END,subfolder)
            self.latest_listbox.configure(state=DISABLED)
            self.genre_listbox.configure(state=DISABLED)
            self.status_listbox.configure(state=DISABLED)


    def AssetSelect(self, event):
        try:
            widget = event.widget
            selection=widget.curselection()
            picked = widget.get(selection[0])
            self.selected_asset = picked
        except:
            pass

    #get current selection from list box on selection, update repo strings
    def CurSelet(self, event):
        widget = event.widget
        selection=widget.curselection()
        picked = widget.get(selection[0])
        self.currentselection = widget.get(0, END).index(picked)

    def reload(self):
        self.on_reload()

    def on_reload(self, event = None):
        self.populaterepobox()
        
    def delete(self):
        self.removerepo()

    def on_new_button(self):
        self.hideinfobox()
        self.addreposcreen.tkraise()
        
#Repo System (Need to move a lot of this to its own module):
    def selectasset(self):
        csel = self.selected_asset
        if csel:
            self.fillassets(csel)

    def fillassets(self, string):
        parts = string.rsplit(".",1)
        self.asset_pattern_firstpart_box.set_text(parts[0])
        self.asset_pattern_lastpart_box.set_text("."+parts[1])


    def addrepo(self):
        print("adding repo")
        
        #Get strings
        fp = self.asset_pattern_firstpart_box.get()
        lp = self.asset_pattern_lastpart_box.get()
        #Check they are populated
        if not fp or not lp:
            print("No asset selected, not adding")
            return
        self.repoVar["pattern"] = [[fp],lp]

        self.repoVar["software"] = self.softwarename_box.get()
        self.repoVar["group"] = self.genres_dropdown.get() or "used-added"
        self.repoVar["category"] = self.category_dropdown.get() or "homebrew"
        self.repoVar["install_subfolder"] = self.subfolder_dropdown.get() or None
        self.repoVar["store_equivalent"] = self.repoVar["software"]
        self.repoVar["description"] = self.new_descriptionbox.get() or "added by user"

        newentry = {
                        self.repoVar["software"] : self.repoVar
                    }

        self.softwarelist.append(self.repoVar)
        guicore.updateguirepos(newentry)
        self.repoVar = {}
        print("repo successfully added")
        self.reload()
        self.controller.set_repos(self.softwarelist)
        self.clearpage()
        self.showmainreposcreen()

    def removerepo(self):
        selectiontoremove = self.softwarelist[self.currentselection]["software"]
        print("removing repo {}".format(selectiontoremove))
        guicore.removeitemfromrepo(selectiontoremove)

        #Remove item from current list
        del self.softwarelist[self.currentselection]
        self.controller.set_repos(self.softwarelist)
        self.currentselection = 0
        self.reload()
  

    def download_json_then_list_assets(self):
        url = self.new_urlbox.get().strip("/")
        if url == "" or url == None:
            print("No url to parse")
            return
        desc = self.new_descriptionbox.get()
        subfolder = self.subfolder_dropdown.get()
        genre = self.genres_dropdown.get()

        if desc == None or desc == "":
            desc = "Added by user, you can edit this description in the repos menu."
        if genre == None or genre == "":
            genre = "user repo"

        self.repoVar = webhandler.getrepochunkfromurl(url,desc)

        with open(self.repoVar["githubjson"]) as json_file: #jsonfile is path, json_file is file obj
            jfile = json.load(json_file)

            if jfile == [] or jfile == None:

                self.controller.raiseError("""No api data, it looks like the repository you are trying to add\nhas no official releases, talk to the repo author and ask them to\nrelease it in order to use it with HBUpdater.""",self.page_name)

                print()
                return

            if len(jfile[0]["assets"]) == 0:
                print("No assets")
                return

            self.assetslistbox.delete(0,END)
            for asset in jfile[0]["assets"]:
                self.assetslistbox.insert(END,asset["name"])

            self.show_assets_frame()


    def clearpage(self):
        self.new_urlbox.clear()
        self.new_descriptionbox.clear()
        self.subfolder_dropdown.clear()
        self.genres_dropdown.clear()
        self.category_dropdown.clear()
        self.hide_assets_frame()
        self.assetslistbox.delete(0,END)
        self.asset_pattern_firstpart_box.clear()
        self.asset_pattern_lastpart_box.clear()
        self.softwarename_box.clear()



    def showmainreposcreen(self):
        self.content_frame.tkraise()
        self.showinfobox()
        self.on_show_frame(None)

