from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.customwidgets as cw
import pages.pagetemplate as pt

import os

import tkinter as tk
from tkinter.constants import *

details_guide_text = """
""" 

class backupPage(pt.page):
    def __init__(self, parent, controller,page_name, back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            page_title="SD BACKUP MANAGER",
            primary_button_text="RESTORE",
            page_name=page_name
            )

        self.maintable.place_forget()
        self.infobox.place_forget()
        self.details_frame.place_forget()
        self.details_right_column.place_forget()



        self.sdimage = tk.PhotoImage(file=os.path.join(locations.assetfolder,"sd.png")).zoom(2).subsample(4)  
        self.trashimage = tk.PhotoImage(file=os.path.join(locations.assetfolder, "trash.png")).subsample(2)


        self.list_buttons_frame.etc_button.setcommand(self.delete)
        self.list_buttons_frame.etc_button.setimage(self.trashimage)

        #Button to uninstall selected software
        self.backupbutton = cw.navbutton(self.main_right_column,command_name=self.backup,image_object= None,text_string="MAKE BACKUP")
        self.backupbutton.place(relx=0, rely=1, y=-3*(navbuttonheight+separatorwidth), height=navbuttonheight, x=+separatorwidth,relwidth=1, width=-(2*separatorwidth))

        columns = ["BACKUP","DATE",]

        self.backupstable = cw.themedtable(self.list_frame,columns,tablecolumnwidth)
        self.backupstable.place(relx=0.0, rely=0.0, relheight=1, relwidth=1,)



        buttonlist = [
            {
            "image" : self.returnimage,
            "callback" : back_command,
            "tooltip" : "Back to home screen",
            },

            {
            "image" : self.sdimage,
            "callback" : self.setSDpath,
            "tooltip" : "Select SD card",
            },

        ]

        self.setbuttons(buttonlist)

        self.setguidetext(details_guide_text)


    def delete(self):
        print("delete button pushed")

    def backup(self):
        if not HBUpdater.setpathset:
            self.setSDpath()

