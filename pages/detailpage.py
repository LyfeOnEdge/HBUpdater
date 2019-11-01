import os
import tkinter as tk
import tkinter.filedialog
import modules.locations as locations
from widgets import ThemedFrame, ThemedLabel, ThemedListbox, activeFrame, scrolledText, button, tooltip, ScrolledThemedListBox
from customwidgets import progressFrame
import style
from appstore import getScreenImage
from webhandler import opentab
from .yesnopage import yesnoPage

from PIL import Image, ImageTk

class detailPage(activeFrame):
    def __init__(self, parent, controller):
        activeFrame.__init__(self,parent,controller)
        self.controller = controller
        self.appstore_handler = controller.appstore_handler
        self.repo_parser = controller.repo_parser
        self.selected_version = None
        self.version_index = None
        self.repo = None
        self.package = None

        self.bind("<Configure>", self.on_configure)

        self.column = ThemedFrame(self, background = style.color_1)
        self.column.place(relx = 1, rely = 0, width = style.sidecolumnwidth, relheight = 1, x = - style.sidecolumnwidth)

        self.column_body = ThemedFrame(self.column, background = style.color_1)
        self.column_body.place(relwidth=1, relheight=1)

        self.column_title = ThemedLabel(self.column_body,"",anchor="w",label_font=style.mediumboldtext, foreground = style.w, background = style.color_1)
        self.column_title.place(x = style.offset, width = - style.offset, rely = 0, relwidth = 1, height = style.detailspagemultiplier)

        self.column_author = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_author.place(x = style.offset, width = - style.offset, y = style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_version = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_version.place(x = style.offset, width = - style.offset, y = 1.333 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_license = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_license.place(x = style.offset, width = - style.offset, y = 1.666 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_package = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_package.place(x = style.offset, width = - style.offset, y = 2.000 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_downloads = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_downloads.place(x = style.offset, width = - style.offset, y = 2.333 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_updated = ThemedLabel(self.column_body,"",anchor="w",label_font=style.smalltext, foreground = style.w, background = style.color_1)
        self.column_updated.place(x = style.offset, width = - style.offset, y = 2.666 * style.detailspagemultiplier, relwidth = 1, height = 0.333 * style.detailspagemultiplier)

        self.column_separator_top = ThemedLabel(self.column_body, "", background=style.lg)
        self.column_separator_top.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - 3 * style.offset - style.buttonsize - 1 - 0.5 * style.buttonsize, width = - 2 * style.offset, height = 1)

        self.tags_menu_label = ThemedLabel(self.column_body,"Releases:",anchor="w",label_font=style.smallboldtext, foreground = style.w, background = style.color_1)
        self.tags_menu_label.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - 2 * style.offset - style.buttonsize - 1 - 0.5 * style.buttonsize, width = - 2 * style.offset, height = 0.5 * style.buttonsize)

        self.TAGS_LIST = ["You shouldn't be seeing this"]
        self.selected_tag_name = tk.StringVar()
        self.selected_tag_name.set(None)
        self.tags_dropdown = tk.OptionMenu(self.column_body ,self.selected_tag_name, *self.TAGS_LIST)
        self.tags_dropdown.configure(foreground = style.w)
        self.tags_dropdown.configure(background = style.color_2)
        self.tags_dropdown.configure(highlightthickness = 0)
        self.tags_dropdown.configure(borderwidth = 0)
        self.tags_dropdown.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - 2 * style.offset - style.buttonsize - 1, width = - 2 * style.offset, height = style.buttonsize)

        self.column_separator_bot = ThemedLabel(self.column_body, "", background=style.lg)
        self.column_separator_bot.place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset) - style.offset - 1, width = - 2 * style.offset, height = 1)

        self.column_open_url_button = button(self.column_body, 
            callback = self.trigger_open_tab, 
            text_string = "VISIT PAGE", 
            font=style.mediumboldtext, 
            background=style.color_2,
            ).place(rely=1,relwidth = 1, x = + style.offset, y = - 3 * (style.buttonsize + style.offset), width = - 2 * style.offset, height = style.buttonsize)

        self.column_install_button = button(self.column_body, 
            callback = self.trigger_install, 
            text_string = "INSTALL", 
            font=style.mediumboldtext, 
            background=style.color_2
            )
        self.column_install_button.place(rely=1,relwidth = 1, x = + style.offset, y = - 2 * (style.buttonsize + style.offset), width = - 2 * style.offset, height = style.buttonsize)

        self.column_uninstall_button = button(self.column_body, 
            callback = self.trigger_uninstall, 
            text_string = "UNINSTALL", 
            font=style.mediumboldtext, 
            background=style.color_2
            )

        self.back_image = ImageTk.PhotoImage(Image.open(locations.backimage).resize((style.buttonsize, style.buttonsize), Image.ANTIALIAS))

        self.column_backbutton = button(self.column_body, image_object=self.back_image, callback=self.leave, background=style.color_1)
        self.column_backbutton.place(rely=1,relx=1,x = -(style.buttonsize + style.offset), y = -(style.buttonsize + style.offset))
        # self.column_backbutton_ttp = tooltip(self.column_backbutton,"Back to list")

        self.content_frame = ThemedFrame(self, background = style.color_2)
        self.content_frame.place(x = 0, width = -style.sidecolumnwidth, rely = 0, relheight = 1, relwidth = 1)

        self.content_frame_header = ThemedFrame(self.content_frame, background = style.color_2)
        self.content_frame_header.place(x = style.offset, width = - 2 * style.offset, rely = 0, relwidth = 1, height = style.detailspagemultiplier)

        self.content_frame_body = ThemedFrame(self.content_frame, background = style.color_2)
        self.content_frame_body.place(x = style.offset, width = - 2 * style.offset, y = style.detailspagemultiplier,relwidth = 1, height = -style.detailspagemultiplier, relheight=1)

        self.content_banner_image_frame = ThemedFrame(self.content_frame, background=style.color_2)
        self.content_banner_image_frame.place(x=0, y = + style.detailspagemultiplier, relwidth=1, height = - style.detailspagemultiplier, relheight = 0.4)

        self.content_banner_image = ThemedLabel(self.content_banner_image_frame,"",background = style.color_2,foreground=style.w,anchor="center",wraplength = None)
        self.content_banner_image.place(x=0, y = 0, relwidth=1, relheight = 1)

        self.content_frame_details = scrolledText(self.content_frame_body, wrap = 'word', font = style.smalltext, background = style.lg)
        self.content_frame_details.place(rely=0.4, relx=0,relwidth=1,relheight=0.25,x=+style.offset, width = - 2 * (style.offset), height=-style.offset)

        self.content_frame_patch_notes_label = ThemedLabel(self.content_frame_body,"Release notes:",anchor="w",label_font=style.mediumboldtext, foreground = style.b, background = style.color_2)
        self.content_frame_patch_notes_label.place(relx = 0.5, width = self.content_frame_patch_notes_label.winfo_reqwidth(), rely = 0.65, y = + style.offset, x = - 0.5 * self.content_frame_patch_notes_label.winfo_reqwidth(), height = 0.33*style.detailspagemultiplier)

        self.content_frame_version_details = scrolledText(self.content_frame_body, wrap = 'word', font = style.smalltext, background = style.lg)
        self.content_frame_version_details.place(rely=0.65, y = + style.offset + 0.33*style.detailspagemultiplier, relx=0,relwidth=1,relheight=0.35, height = -(2 * style.offset + 0.33*style.detailspagemultiplier), x=+style.offset, width = - 2 * (style.offset))

        #Displays app name
        self.header_label = ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.giantboldtext, background = style.color_2, foreground=style.b)
        self.header_label.place(rely=0, y=0, relheight=0.65)

        #Displays app name
        self.header_author = ThemedLabel(self.content_frame_header,"",anchor="w",label_font=style.smalltext, background = style.color_2, foreground=style.color_1)
        self.header_author.place(rely=0.65, y=0, relheight=0.35)

        self.progress_bar = progressFrame(self)

        self.yesnoPage = yesnoPage(self)

    def update_option_menu(self, options):
        menu = self.tags_dropdown['menu']
        menu.delete(0, 'end')
        for string in options:
            menu.add_command(label=string, 
                             command=lambda value=string: self.on_menu_update(value))
        self.on_menu_update(options[0])

    def on_menu_update(self, option):
        self.selected_tag_name.set(option)
        self.select_version(option)

    def update_page(self,repo):
        self.selected_version = None
        self.repo = repo

        try:
            package = repo["package"]
        except:
            package = repo["software"]

        self.package = package

        self.controller.async_threader.do_async(self.update_banner)

        github_content = repo["github_content"]

        version = github_content[0]["tag_name"]

        self.column_title.set("Title: {}".format(repo["name"]))

        self.column_author.set("Author: {}".format(repo["author"]))
        self.column_version.set("Latest Version: {}".format(github_content[0]["tag_name"]))
        try:
            self.column_license.set("License: {}".format(repo["license"]))
        except:
            self.column_license.set("License: N/A")


        self.column_package.set("Package: {}".format(package))
        self.column_downloads.set("Downloads: {}".format(repo["downloads"]))
        self.column_updated.set("Updated: {}".format(github_content[0]["created_at"]))

        self.content_frame_details.configure(state="normal")
        self.content_frame_details.delete('1.0', "end")

        #Makes newlines in details print correctly. Hacky but :shrug:
        details = repo["description"].replace("\\n", """
"""
            )
        self.content_frame_details.insert("1.0", details)
        self.content_frame_details.configure(state="disabled")


        self.header_label.set(repo["name"])
        self.header_author.set(repo["author"])

        #Hides or places the uninstalll button if not installed or installed respectively
        #get_package_entry returns none if no package is found or if the sd path is not set
        if self.appstore_handler.get_package_entry(package):
            self.column_uninstall_button.place(rely=1,relwidth = 1, x = + style.offset, y = - 1 * (style.buttonsize + style.offset), width = - (3 * style.offset + style.buttonsize), height = style.buttonsize)
            if self.column_install_button:
                if self.appstore_handler.clean_version(self.appstore_handler.get_package_version(package), package) > self.appstore_handler.clean_version(self.appstore_handler.get_package_version(version), package):
                    self.column_install_button.settext("UPDATE")
                else:
                    self.column_install_button.settext("REINSTALL")
        else:
            self.column_uninstall_button.place_forget()
            if self.column_install_button:
                self.column_install_button.settext("INSTALL")

        tags = []
        for release in self.repo["github_content"]:
            tags.append(release["tag_name"])
        self.update_option_menu(tags)

    def select_version(self, option):
        try:
            self.selected_version = option
            self.version_index = self.controller.appstore_handler.get_tag_index(self.repo["github_content"], self.selected_version)
            self.update_release_notes()
        except Exception as e:
            # print(e)
            pass

    def on_configure(self, event=None):
        if self.repo:
            self.update_banner()

    def update_banner(self):
        self.bannerimage = getScreenImage(self.package)
        if self.bannerimage:
            self.do_update_banner(self.bannerimage)
        else:
            self.do_update_banner(locations.notfoundimage)

    def do_update_banner(self,image_path):
        maxheight = self.content_banner_image_frame.winfo_height()
        maxwidth = self.content_banner_image_frame.winfo_width()
        if maxwidth > 0 and maxheight > 0:
            art_image = Image.open(image_path)
            wpercent = (maxwidth/float(art_image.size[0]))
            hsize = int((float(art_image.size[1])*float(wpercent)))
            w_img = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
            if w_img.size[0] > maxheight:
                hpercent = (maxheight/float(art_image.size[1]))
                wsize = int((float(art_image.size[0])*float(hpercent)))
                art_image = art_image.resize((maxwidth,hsize), Image.ANTIALIAS)
            else:
                art_image = w_img

            art_image = ImageTk.PhotoImage(art_image)

            self.content_banner_image.configure(image=art_image)
            self.content_banner_image.image = art_image

    def update_release_notes(self):
        notes = self.repo["github_content"][self.version_index]["body"]

        self.content_frame_version_details.configure(state="normal")
        self.content_frame_version_details.delete('1.0', "end")

        #Makes newlines in details print correctly. Hacky but :shrug:
        notes = notes.replace("\\n", """
"""
            )
        self.content_frame_version_details.insert("1.0", notes)
        self.content_frame_version_details.configure(state="disabled")

    def show(self, repo):
        self.do_update_banner(locations.notfoundimage)
        self.controller.async_threader.do_async(self.update_page, [repo], priority = "medium")
        self.tkraise()
        for child in self.winfo_children():
            child.bind("<Escape>", self.leave)

    def leave(self):
        self.controller.show_frame("appstorePage")
        for child in self.winfo_children():
            child.unbind("<Escape>")

    def reload_function(self):
            self.controller.frames["appstorePage"].reload_category_frames()
            self.reload()

    def trigger_install(self):
        index = 0
        if not self.appstore_handler.check_path():
            self.set_sd()
        if self.appstore_handler.check_path():
            if self.appstore_handler.check_if_get_init():
                if self.repo:
                    self.controller.async_threader.do_async(self.appstore_handler.install_package, [self.repo, self.version_index, self.progress_bar.update, self.reload_function, self.progress_bar.set_title], priority = "high")
            else:
                self.yesnoPage.getanswer("The homebrew appstore has not been initiated here yet, would you like to initiate it?", self.init_get_then_continue)

    def init_get_then_continue(self):
        self.appstore_handler.init_get()
        self.trigger_install()

    def trigger_uninstall(self):
        if self.repo:
            self.controller.async_threader.do_async(self.appstore_handler.uninstall_package, [self.repo], priority = "high")
            self.controller.frames["appstorePage"].reload_category_frames()
            self.schedule_callback(self.reload(), 100)

    def reload(self):
        self.controller.async_threader.do_async(self.update_page, [self.repo])

    def trigger_open_tab(self):
        if self.repo:
            try:
                url = self.repo["projectpage"]
                opentab(url)
            except:
                print("Failed to open tab for url {}".format(url))

    def set_sd(self):
        chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
        self.appstore_handler.set_path(chosensdpath)
        self.reload()