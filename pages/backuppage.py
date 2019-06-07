from modules.format import * 
import modules.guicore as guicore
import modules.HBUpdater as HBUpdater
import modules.locations as locations
import modules.customwidgets as cw
import pages.pagetemplate as pt

import os

#archive handling
from zipfile import ZipFile
from datetime import datetime

import tkinter as tk
from tkinter.constants import *

details_guide_text = """


To make a backup:
    1. Select your SD card
    2. Click "Make backup"

To restore a backup:
    - WARNING
    - This cannot be undone
    - Any files in the target directory that also exist in the backup will be overwritten
    1. Select your SD card
    2. Select the backup you wish to restore
    3. Click "Restore"
    4. Confirm that you wish to restore backup.

Clicking the trash can will delete the currently highlighted backup.
""" 

backup_prefix = "backup_"

class backupPage(pt.page):
    def __init__(self, parent, controller,page_name, back_command):
        pt.page.__init__(self,parent=parent, 
            controller=controller,
            back_command=back_command,
            page_title="SD BACKUP MANAGER",
            primary_button_text="RESTORE",
            primary_button_command=self.restore,
            page_name=page_name
            )

        self.bind("<<ShowFrame>>", self.on_show_frame)

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
        self.listbox_list = []

        self.backupstable = cw.themedtable(self.list_frame,columns,tablecolumnwidth)
        self.backupstable.place(relx=0.0, rely=0.0, relheight=1, relwidth=1,)

        for column in columns:
            self.backupstable.listboxes[column].bind("<MouseWheel>", self.OnMouseWheel)
            self.listbox_list.append(self.backupstable.listboxes[column])

        #set listboxes to easy names
        self.software_listbox = self.backupstable.listboxes["BACKUP"]
        self.software_listbox.bind('<<ListboxSelect>>',self.CurSelet)
        self.datecolumn = self.backupstable.listboxes["DATE"]

        self.console = cw.consolebox(self.content_frame)
        self.console.place(relx=0,rely=.7,relwidth=1, relheight=.3)
        self.printtoconsolebox("Select SD card to make or restore backups")

 
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

        #Details guide for usage details and warnings
        self.details_guide = cw.ScrolledText(self.main_right_column,borderwidth=0,highlightthickness=0,background=light_color,foreground=guidetextcolor,wrap=WORD,font=details_guide_font)
        self.details_guide.place(relwidth=1,relheight=1,height=-(3*(navbuttonheight+separatorwidth)+separatorwidth))
        

        self.setguidetext(details_guide_text)

    def printtoboth(self,stringtoprint):
        self.console.print(stringtoprint)
        print(stringtoprint)

    def printtoconsolebox(self,stringtoprint):
        self.console.print(stringtoprint)

    def updatetable(self,searchterm):            
        try:
            for listbox in self.listbox_list:
                listbox.configure(state=NORMAL)

            self.cleartable()

            files_in_backups = subfiles(locations.backupfolder)
            backups = []

            itt = 0
            while itt < len(files_in_backups["location"]):
                filename = files_in_backups["filename"][itt]
                location = files_in_backups["location"][itt]
                if os.path.isfile(location):
                    if filename.endswith(".zip"):
                        backups.append(filename.strip("\\"))
                itt += 1

            for backup in backups:
                self.backupstable.listboxes["BACKUP"].insert(END, backup)
                self.backupstable.listboxes["DATE"].insert(END,parse_date(backup))

            for listbox in self.listbox_list:
                listbox.configure(state=DISABLED) 

            self.backupstable.listboxes["BACKUP"].configure(state=NORMAL)
        except Exception as e:
            pass
            # print("updatetable error - {}".format(e))


    def delete(self):
        if self.software_listbox.size() == 0:
            self.printtoboth("\nNothing to delete")
            return


        filename = self.backupstable.listboxes["BACKUP"].get(self.currentselection)
        zip_file = os.path.join(locations.backupfolder, filename)

        self.controller.show_frame("errorPage")
        self.controller.frames["errorPage"].getanswer(self.page_name,"Are you sure you would like to delete this backup?\n\n{}".format(zip_file),lambda: self.deletebackup(zip_file))

        self.refreshPage()


    def deletebackup(self,filetodelete):
        os.remove(filetodelete)
        self.printtoboth("\nDeleted backup {}\n".format(filetodelete))

    def backup(self):
        if not HBUpdater.checksdset():
            self.setSDpath()
        if not HBUpdater.checksdset():
            self.printtoboth("\nSD path not set, can't make backup\n")
            return

        if not HBUpdater.checktrackingfile():
            self.controller.show_frame("errorPage")
            self.controller.frames["errorPage"].getanswer(self.page_name,"Could not find tracking file, are you sure you would like to proceed with your backup?\n",self.makebackup)
        else:
            self.makebackup()

    def makebackup(self):
        files = subfiles(HBUpdater.getSDpath())
        ziptime = date_str()
        newzipname = "{}{}.zip".format(backup_prefix,ziptime)
        newzip = os.path.join(locations.backupfolder,newzipname)

        with ZipFile(newzip, 'x') as backup:
            itt = 0
            while itt < len(files["location"]):
                filename = files["filename"][itt]
                backup.write(files["location"][itt],filename)
                print("Archived - {}".format(filename))
                itt += 1
            self.printtoconsolebox("\nArchived {} files\n".format(itt))

        self.printtoboth("Backup {} complete".format(newzipname))
        self.updatetable(None)

    def restore(self):
        if self.software_listbox.size() == 0:
            self.printtoboth("\nNothing to restore\n")
            return

        if not HBUpdater.checksdset():
            self.setSDpath()
        if not HBUpdater.checksdset():
            self.printtoboth("\nSD path not set, can't restore backup\n")
            return

        self.controller.show_frame("errorPage")
        self.controller.frames["errorPage"].getanswer(self.page_name,"Are you sure you want to restore this backup?\n\nFILES IN THE TARGET DIRECTORY SHARING THE SAME NAME AS AN ITEM IN THE BACKUP WILL BE OVERWRITTEN.\n\nTarget Directory - {}".format(HBUpdater.getSDpath()),self.restorebackup)

    def restorebackup(self):
        chosensdpath = HBUpdater.getSDpath()

        zip_file = os.path.join(locations.backupfolder, self.backupstable.listboxes["BACKUP"].get(self.currentselection))

        with ZipFile(zip_file, 'r') as zipObj:
            zipObj.extractall(chosensdpath)
            namelist = zipObj.namelist()
            print("files copied: \n {}".format(namelist))
            self.printtoboth("Copied {} files".format(len(namelist)))
            self.printtoboth("\nSucessfully restored backup {} to SD\n".format(zip_file))
            



    def on_show_frame(self,event):
        self.refreshPage()
    def pageup(self):
        if self.currentselection <  self.software_listbox.size()-1:
            self.currentselection += 1
            self.refreshPage()
    def pagedown(self):
        if self.currentselection > 0:
            self.currentselection -= 1
            self.refreshPage()
    def refreshPage(self):
        self.updatetable(None)
        if self.currentselection > self.software_listbox.size():
            self.currentselection = self.software_listbox.size()-1


        for listbox in self.listbox_list:
            listbox.selection_clear(0, self.backupstable.listboxes["BACKUP"].size()-1)
            listbox.selection_set(self.currentselection)
            listbox.see(self.currentselection)
            listbox.activate(self.currentselection)

def date_str():
    #returns the today string year, month, day, second
    return '{}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S"))

def subfiles(path):
    filelist = {
        "location" : [],
        "filename" : [],
    }

    for root, dirs, files in os.walk(path):
        for name in files:
            filename = os.path.join(root, name)

            filelist["location"].append(filename)

            filename = remove_prefix(filename,path)

            filelist["filename"].append(filename)
    return filelist

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text  # or whatever

def parse_date(date):
    try:
        date = remove_prefix(date, backup_prefix)
        date = date.strip(".zip")
        dates = date.split("-")
        ddmmyyyy = "{}/{}/{}".format(dates[1],dates[2],dates[0])
        return ddmmyyyy
    except Exception as e:
        self.printtoboth("dateparsing error - {}".format(e))
        return "unknown"





