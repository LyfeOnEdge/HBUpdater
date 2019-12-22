import os, json
from widgets import ThemedFrame, ThemedListbox, ThemedLabel, searchBox, button, themedScrollingText, scrollingTkListbox
from HBUpdater import repo_parser, store_handler
from customwidgets import progressFrame
import style
import tkinter as tk
import tkinter.filedialog
from locations import presetsfolder, assetsfolder
from .yesnopage import yesnoPage
from .usermessagepage import usermessagePage
from PIL import Image, ImageTk
from asyncthreader import threader

warning_label = """APPLYING A BUNDLE IS A ONE-WAY PROCESS.
To remove packages you will have go to the `Installed` tab and remove them individually.
Deselect any packages you don't wish to install or update.
Would you like to apply this package?"""

#modified searchbox that calls a function to update the json printout
class entrybox(searchBox):
	def __init__(self, frame, placeholder = "", callback = None):
		searchBox.__init__(self, frame, placeholder=placeholder, command = callback, command_on_keystroke = True, entry_font = style.smalltext, placeholder_font = style.smallerboldtext, placeholder_color = style.b)

class presetsPage(ThemedFrame):
	def __init__(self, parent, controller):
		self.controller = controller
		self.appstore_handler = store_handler
		self.repo_parser = repo_parser
		self.current_file_path = None
		self.originaljson = None
		self.currentjson = None
		self.ok_to_load = True
		self.json_name = None
		self.changes = None
		self.progress_string = None
		self.gui_title = None
		self.errors = []

		ThemedFrame.__init__(self,parent, background = style.color_2)
		self.bind("<<ShowFrame>>", self.update_apply_frame)

		#LEFT COLUMN________________________________
		self.presets_listbox_label = ThemedLabel(self, label_text ="Bundles:", background = style.color_2, foreground = style.lg, label_font = style.largeboldtext)
		self.presets_listbox_label.place(relx = 0.0, relwidth = 0.5, height = style.buttonsize - 2 * style.offset, x = + style.offset, width = - 2 * style.offset)

		image_file = os.path.join(assetsfolder, "trash.png")
		button_image = Image.open(image_file)
		buttonsize = style.buttonsize - 4 * style.offset
		#Resizes and saves image if it's the wrong size for faster loads in the future
		if not button_image.size[0] == [buttonsize, buttonsize]:
			button_image = button_image.resize((buttonsize, buttonsize), Image.ANTIALIAS)
		self.trash_image = ImageTk.PhotoImage(button_image)

		self.delete_preset_button = button(self, callback = self.delete, image_object = self.trash_image, background = style.color_1)
		self.delete_preset_button.place(relx = 0.5, x = -(style.buttonsize - 2 * style.offset), y = + style.offset, width = style.buttonsize - 3 * style.offset, height = style.buttonsize - 3 * style.offset)

		self.presets_listbox = scrollingTkListbox(self, borderwidth = 0, highlightthickness = 0, background = style.w, foreground = style.b, exportselection = False)
		self.presets_listbox.place(relx = 0.0, relwidth = 0.5, relheight = 1, y = style.buttonsize - style.offset, x = + style.offset, width = - 2 * style.offset, height = - (2.5 * style.buttonsize + 2 * style.offset))

		self.new_preset_entry = entrybox(self, placeholder = "New bundle name (No extension)", callback = self.update_json)
		self.new_preset_entry.place(relx=0.0, x = + style.offset, relwidth = 0.5, height = 0.5 * style.buttonsize, rely = 1, y = - (2 * style.offset + 1.5 * style.buttonsize), width = - (3* style.offset + 0.5 * style.buttonsize))

		self.new_preset_button = button(self, callback = self.new, text_string = "+", background = style.color_1)
		self.new_preset_button.place(relx = 0.5, x = - (style.offset + 0.5 * style.buttonsize), width = 0.5 * style.buttonsize, height = 0.5 * style.buttonsize, rely = 1, y = - (2 * style.offset + 1.5 * style.buttonsize))

		self.loadbutton = button(self, callback=self.load,text_string="Load",background=style.color_1)
		self.loadbutton.place(relx=0.0, x = + style.offset, relwidth = 0.5, height = style.buttonsize, rely = 1, y = - (style.offset + style.buttonsize), width = - 2 * style.offset)

		self.divider = ThemedFrame(self, background = style.lg)
		self.divider.place(relx = 0.5, width = 2, relheight = 1, height = - 2 * style.offset, y = + style.offset, x = - 1)

		self.column_select_frame = ThemedFrame(self, background = style.color_2)
		self.column_select_frame.place(relx = 0.5, x = + style.offset, width = - 2 * style.offset, relwidth = 0.5, height = style.buttonsize, y = + style.offset)

		self.editor_button = button(self.column_select_frame, callback=lambda: self.show_frame("editor"),text_string="Edit",background=style.color_1, borderwidth = 1)
		self.editor_button.place(relheight = 1, relwidth = 0.33, relx = 0, width = - 0.5 * style.offset)

		self.applier_button = button(self.column_select_frame, callback=lambda: self.show_frame("applier"),text_string="Apply",background=style.color_1, borderwidth = 1)
		self.applier_button.place(relheight = 1, relwidth = 0.34, relx = 0.33, x = + 0.5 * style.offset, width = -style.offset)

		self.build_button = button(self.column_select_frame, callback=lambda: self.show_frame("builder"),text_string="Build",background=style.color_1, borderwidth = 1)
		self.build_button.place(relheight = 1, relwidth = 0.33, relx = 0.67, x = + 0.5 * style.offset, width = - 0.5 * style.offset)

		self.buttonmap = {
			"editor" : self.editor_button,
			"applier" : self.applier_button,
			"builder" : self.build_button
		}

		self.button_divider = ThemedFrame(self, background = style.lg)
		self.button_divider.place(relx = 0.5, x = + style.offset, width = - 2 * style.offset, relwidth = 0.5, height = 1, y = style.buttonsize + 2 * style.offset)

		self.content_frame = ThemedFrame(self, background = style.color_2)
		self.content_frame.place(relx = 0.5, relwidth = 0.5, width = - 2 * style.offset, x = + style.offset, relheight = 1, y = style.buttonsize + 3 * style.offset + 1, height = - (style.buttonsize + 4 * style.offset + 1))

		#EDITOR COLUMN________________________________
		self.editor_frame = ThemedFrame(self.content_frame, background = style.color_2)

		self.preset_name = entrybox(self.editor_frame, placeholder = "Bundle Name", callback = self.update_json)
		self.preset_name.place(height = 0.5 * style.buttonsize, relwidth = 1)

		self.author_name = entrybox(self.editor_frame, placeholder = "Bundle Author", callback = self.update_json)
		self.author_name.place(y = 1 * (style.offset + 0.5 * style.buttonsize), height = 0.5 * style.buttonsize, relwidth = 1)

		self.preset_package_version = entrybox(self.editor_frame, placeholder = "Bundle Package Version", callback = self.update_json)
		self.preset_package_version.place(y = 2 * (style.offset + 0.5 * style.buttonsize), height = 0.5 * style.buttonsize, relwidth = 1)

		self.packages_listbox_and_json_output_preview_frame = ThemedFrame(self.editor_frame, background = style.color_2)
		self.packages_listbox_and_json_output_preview_frame.place(y = 3 * (style.offset + 0.5 * style.buttonsize), relheight = 1, height =  - (2 * style.buttonsize + 7 * style.offset), relwidth = 1)

		self.packages_listbox_label = ThemedLabel(self.packages_listbox_and_json_output_preview_frame, label_text ="Packages:", background = style.color_2, foreground = style.lg, label_font = style.mediumboldtext)
		self.packages_listbox_label.place(relwidth = 1, height = style.buttonsize - 2 * style.offset)

		self.packages_listbox = scrollingTkListbox(self.packages_listbox_and_json_output_preview_frame, borderwidth = 0, highlightthickness = 0, background = style.w, foreground = style.b, exportselection = False, selectmode='multiple')
		self.packages_listbox.place(y = style.buttonsize - 2 * style.offset, relwidth = 1, relheight = 0.5, height = - (style.offset + style.buttonsize - 2 * style.offset))
		self.packages_listbox.bind('<<ListboxSelect>>', self.update_json)

		self.output_divider = ThemedFrame(self.packages_listbox_and_json_output_preview_frame, background = style.lg)
		self.output_divider.place(relwidth = 1, height = 1, rely = 0.5)

		self.output_json_label = ThemedLabel(self.packages_listbox_and_json_output_preview_frame, label_text ="Output:", background = style.color_2, foreground = style.lg, label_font = style.mediumboldtext)
		self.output_json_label.place(rely = 0.5, y = + style.offset + 1, relwidth = 1, height = style.buttonsize - 2 * style.offset)

		self.output_json = themedScrollingText(self.packages_listbox_and_json_output_preview_frame, font = style.smalltext)
		self.output_json.place(relwidth = 1, rely = 0.5, relheight = 0.5, height = - (style.buttonsize + style.offset), y = style.buttonsize)

		self.savebutton = button(self.editor_frame, callback=self.save,text_string="Save",background=style.color_1)
		self.savebutton.place(relwidth = 1, height = style.buttonsize, rely = 1, y = - (style.buttonsize))

		#APPLIER COLUMN_______________________________
		self.applier_frame = ThemedFrame(self.content_frame, background = style.color_2)

		self.applier_bundle_label = ThemedLabel(self.applier_frame, label_text ="BUNDLE: ", anchor="w", background = style.color_2, foreground = style.lg, label_font = style.smallboldtext)
		self.applier_bundle_label.place(height = 0.5 * style.buttonsize - style.offset)

		self.applier_selected_bundle_label = ThemedLabel(self.applier_frame, label_text ="test", anchor="e", background = style.color_2, foreground = style.w, label_font = style.smallboldtext)
		self.applier_selected_bundle_label.place(x = self.applier_bundle_label.winfo_reqwidth(), height = 0.5 * style.buttonsize - 1 * style.offset)
	
		self.applier_sd_label = ThemedLabel(self.applier_frame, label_text ="SD: ", anchor="w", background = style.color_2, foreground = style.lg, label_font = style.smallboldtext)
		self.applier_sd_label.place(y = 0.5 * style.buttonsize, height = 0.5 * style.buttonsize - 1 * style.offset)

		self.applier_selected_sd_label = ThemedLabel(self.applier_frame, label_text ="test", anchor="e", background = style.color_2, foreground = style.w, label_font = style.smallboldtext)
		self.applier_selected_sd_label.place(y = 0.5 * style.buttonsize, x = self.applier_sd_label.winfo_reqwidth(), height = 0.5 * style.buttonsize - 1 * style.offset)    

		self.applier_header_divider = ThemedFrame(self.applier_frame, background = style.lg)
		self.applier_header_divider.place(y = 1 * style.buttonsize, relwidth = 1, height = 1)

		self.applier_listboxes_frame = ThemedFrame(self.applier_frame, background = style.color_2)
		self.applier_listboxes_frame.place(y = 1 * style.buttonsize + 1 * style.offset + 1, relheight = 1, height = - (2 * style.buttonsize + 1 + style.offset), relwidth = 1)

		self.applier_to_be_installed_frame = ThemedFrame(self.applier_listboxes_frame, background = style.color_2)
		self.applier_to_be_installed_frame.place(relwidth = 1, relheight = 0.33, height = - style.offset)
		self.applier_to_be_installed_label = ThemedLabel(self.applier_to_be_installed_frame, label_text ="To be installed:", background = style.color_2, foreground = style.lg, label_font = style.smallboldtext)
		self.applier_to_be_installed_label.place(relwidth = 1, height = 0.5 * style.buttonsize - style.offset)
		self.applier_to_be_installed_listbox = scrollingTkListbox(self.applier_to_be_installed_frame, borderwidth = 0, highlightthickness = 0, background = style.w, foreground = style.b, exportselection = False, selectmode='multiple')
		self.applier_to_be_installed_listbox.place(y = 0.5 * style.buttonsize - 1 * style.offset, relwidth = 1, relheight = 1, height = - (0.5 * style.buttonsize - 3 * style.offset))
		# self.applier_to_be_installed_listbox.bind('<<ListboxSelect>>', self.update_json)

		self.applier_to_be_updated_frame = ThemedFrame(self.applier_listboxes_frame, background = style.color_2)
		self.applier_to_be_updated_frame.place(relwidth = 1, relheight = 0.34, rely = 0.33, height = - style.offset)
		self.applier_to_be_updated_label = ThemedLabel(self.applier_to_be_updated_frame, label_text ="To be updated:", background = style.color_2, foreground = style.lg, label_font = style.smallboldtext)
		self.applier_to_be_updated_label.place(relwidth = 1, height = 0.5 * style.buttonsize - style.offset)
		self.applier_to_be_updated_listbox = scrollingTkListbox(self.applier_to_be_updated_frame, borderwidth = 0, highlightthickness = 0, background = style.w, foreground = style.b, exportselection = False, selectmode='multiple')
		self.applier_to_be_updated_listbox.place(y = 0.5 * style.buttonsize - 1 * style.offset, relwidth = 1, relheight = 1, height = - (0.5 * style.buttonsize - 3 * style.offset))
		# self.applier_to_be_installed_listbox.bind('<<ListboxSelect>>', self.update_json)

		self.applier_to_be_unchanged_frame = ThemedFrame(self.applier_listboxes_frame, background = style.color_2)
		self.applier_to_be_unchanged_frame.place(relwidth = 1, relheight = 0.33, rely = 0.67, height = - style.offset)
		self.applier_to_be_unchanged_label = ThemedLabel(self.applier_to_be_unchanged_frame, label_text ="Unchanged:", background = style.color_2, foreground = style.lg, label_font = style.smallboldtext)
		self.applier_to_be_unchanged_label.place(relwidth = 1, height = 0.5 * style.buttonsize - style.offset)
		self.applier_to_be_unchanged_listbox = scrollingTkListbox(self.applier_to_be_unchanged_frame, borderwidth = 0, highlightthickness = 0, background = style.w, foreground = style.b, exportselection = False, selectmode='multiple')
		self.applier_to_be_unchanged_listbox.place(y = 0.5 * style.buttonsize - 1 * style.offset, relwidth = 1, relheight = 1, height = - (0.5 * style.buttonsize - 3 * style.offset))
		# self.applier_to_be_installed_listbox.bind('<<ListboxSelect>>', self.update_json)

		self.applier_apply_button = button(self.applier_frame, callback=self.apply,text_string="Apply",background=style.color_1)
		self.applier_apply_button.place(relwidth = 1, height = style.buttonsize, rely = 1, y = - (style.buttonsize))

		#BUILDER COLUMN_______________________________
		self.builder_frame = ThemedFrame(self.content_frame, background = style.color_2)


		for package in self.repo_parser.all:
			self.packages_listbox.insert("end", package["package"])

		self.frames = [
			{
			"frame" : self.editor_frame,
			"text" : "editor",
			},
			{
			"frame" : self.applier_frame,
			"text" : "applier"
			},
			{
			"frame" : self.builder_frame,
			"text" : "builder"
			}
		]

		self.content_frames = {}
		def make_frames_and_add(frame_list):
			for f in frame_list:
				page_name = f["text"]
				frame = f["frame"]
				self.content_frames[page_name] = frame
				frame.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)

		make_frames_and_add(self.frames)

		self.show_frame("editor")

		self.yesno = yesnoPage(self)
		self.usermessage = usermessagePage(self)
		self.progress_bar = progressFrame(self)
		self.update_json()
		self.reload_presets()
		self.update_sd_path()

	def show_frame(self, page_name):
		#Show a frame for the given page name
		frame = self.content_frames[page_name]
		frame.event_generate("<<ShowFrame>>")
		frame.tkraise()

		for button in self.buttonmap.keys():
			self.buttonmap[button].configure(background = style.color_1)
		self.buttonmap[page_name].select()


	def reload_presets(self):
		self.presets_listbox.delete(0, "end")
		files = []
		for file in os.listdir(presetsfolder):
			if file.endswith(".json"):
				files.append(file)
		for file in files:
			self.presets_listbox.insert("end", file)

	#preset is the path to a json 
	def load(self):
		#If new json is empty and hasn't been edited.
		if self.update_json() == self.currentjson or self.currentjson == None:
			self.ok_to_load = True
		if not self.ok_to_load:
			self.yesno.getanswer("You have unsaved changes, would you like to discard them and load a new preset?", self.do_load)
		else:
			self.do_load()
		self.ok_to_load = False

	def do_load(self, json_name = None):
		if json_name:
			self.json_name = json_name
		else:
			self.json_name = self.presets_listbox.get("active")
		preset = os.path.join(presetsfolder, self.json_name)
		self.current_file_path = preset
		self.packages_listbox.selection_clear(0, "end")
		try:
			with open(preset) as preset_file:
				preset_object = json.load(preset_file)
				self.originaljson = preset_object
		except:
			#Inform user via gui
			print("Error loading preset json ")
		# try:
		self.currentjson = json.dumps(preset_object, indent = 4)
		self.author_name.set_text(preset_object.get("author"))
		self.preset_name.set_text(preset_object.get("title"))
		self.preset_package_version.set_text(preset_object.get("version"))
		for package in preset_object.get("packages"):
			self.packages_listbox.selection_set(self.packages_listbox.get(0, "end").index(package))
		self.applier_selected_bundle_label.set(preset_object.get("title"))
		# except Exception as e:
		#     print("Error setting entry fields - {}".format(e))
		self.update_json()
		self.update_apply_frame()

	def save(self):
		if self.current_file_path:
			print("Saving preset - {}".format(self.current_file_path))
			output = self.update_json()
			with open(self.current_file_path, "w+") as preset_file:
				preset_file.writelines(output)
			self.do_load()
		else:
			print("Select a file first")

	#Gets the page ready to make a new repo
	def new(self):
		new_file_name = self.new_preset_entry.get_text()
		self.json_name = new_file_name.strip() + ".json"
		if self.json_name:
			self.clear()
			self.current_file_path = os.path.join(presetsfolder, self.json_name)
			new_json = {
				"title": new_file_name.strip(),
				"author": "",
				"version": "",
				"packages": []
			}
			output = json.dumps(new_json, indent = 4)
			with open(self.current_file_path, "w+") as preset_file:
				preset_file.writelines(output)
			self.reload_presets()

		self.do_load(self.json_name)

	def clear(self):
		self.author_name.set_text("")
		self.preset_name.set_text("")
		self.preset_package_version.set_text("")
		self.packages_listbox.selection_clear(0, "end")
		self.new_preset_entry.set_text("")

	def update_json(self, event = None):
		j = {}
		j["title"] = self.preset_name.get_text()
		j["author"] = self.author_name.get_text()
		j["version"] = self.preset_package_version.get_text()
		selected = self.packages_listbox.curselection()
		j["packages"] = [self.packages_listbox.get(selection) for selection in selected if selected]

		j_text = json.dumps(j, indent = 4)
		self.output_json.set(j_text)
		return j_text

	def delete(self):
		self.yesno.getanswer("Delete preset - {}?".format(self.presets_listbox.get("active")), self.do_delete)

	def do_delete(self):
		try:
			os.remove(os.path.join(presetsfolder, self.presets_listbox.get("active")))
		except Exception as e:
			print("Failed to delete preset - {}\n   ~ {}".format(self.presets_listbox.get("active"), e))
		self.clear()
		self.reload_presets()
		self.current_file_path = None
		self.currentjson = None
		self.json_name = None
		self.update_json()

	def apply(self):
		if not self.appstore_handler.check_path():
			self.set_sd()
		if self.appstore_handler.check_path():
			self.yesno.getanswer(warning_label, self.do_apply, follow_up = True)

	def do_apply(self):
		selected_to_be_installed = self.applier_to_be_installed_listbox.curselection()
		to_be_installed = [self.applier_to_be_installed_listbox.get(selection) for selection in selected_to_be_installed if selected_to_be_installed]
		selected_to_be_updated = self.applier_to_be_updated_listbox.curselection()
		to_be_updated = [self.applier_to_be_updated_listbox.get(selection) for selection in selected_to_be_updated if selected_to_be_updated]
		to_be_unchanged = self.applier_to_be_unchanged_listbox.get(0, "end")

		outstring = ""
		outstring += "Applying bundle {}\n".format(self.originaljson["title"])

		changes = []
		if to_be_installed:
			for package in to_be_installed:
				changes.append(package)
			outstring += "The following packages will be INSTALLED: {}\n".format(json.dumps(to_be_installed, indent = 4))

		if to_be_updated:
			for package in to_be_updated:
				changes.append(package)
			outstring += "The following packages will be UPDATED: {}\n".format(json.dumps(to_be_updated, indent = 4))

		if to_be_unchanged:
			outstring += "The following packages will remain UNCHANGED: {}\n".format(json.dumps(to_be_unchanged, indent = 4))

		outstring += "Please confirm."

		if not changes:
			self.yesno.getanswer("No packages will be changed, please select packages you would like to add.", self.yesno.hide())
		else:
			self.changes = changes
			self.yesno.getanswer(outstring, lambda: self.do_do_apply(self.changes), follow_up = True)

	def do_do_apply(self, package_list):
		print("Applying bundle")
		packages = [self.repo_parser.get_package(package) for package in package_list]
		for package in package_list:
			threader.do_unique(self.appstore_handler.install_package_list, [packages, 0, self.progress_function, self.reset_title, self.title_function, False, self.error_function, self.complete_function])
		self.controller.frames["appstorePage"].reload_category_frames()

	def title_function(self, string):
		self.gui_title = string
		self.update_title()

	def progress_function(self, string, percent_complete):
		self.progress_string = "{} ~ {}%".format(string, percent_complete)
		self.update_title()

	def update_title(self):
		if self.gui_title and self.progress_string:
			self.controller.wm_title("{}: {}".format(self.gui_title, self.progress_string))
		else:
			self.reset_title()

	def error_function(self, erring_repo):
		self.errors.append(erring_repo)

	def clear_title(self):
		self.reset_title()
		self.progress_string = None
		self.gui_title = None

	def complete_function(self):
		self.usermessage.telluser("The following packages errored during install: {}".format(self.errors))
		self.errors = []

	def reset_title(self):
		self.controller.wm_title(self.controller.version)

	def check_if_installer_running(self):
		if not threader.is_unique_running():
			self.reset_title()

	def set_sd(self):
		chosensdpath = tkinter.filedialog.askdirectory(initialdir="/",  title='Please select your SD card')
		self.appstore_handler.set_path(chosensdpath)
		self.update_sd_path()
		self.update_apply_frame()

	def update_sd_path(self):
		chosensdpath = self.appstore_handler.check_path()
		if chosensdpath:
			#Get the basename
			basepath = os.path.basename(os.path.normpath(chosensdpath))
			#If we didn't find it, assume it's a root dir and just return the whole path
			if not basepath:
				basepath = chosensdpath
		else:
			basepath = "Not Set"
		self.applier_selected_sd_label.set(basepath)

	def update_apply_frame(self, event = None):
		if self.appstore_handler.check_path():
			packages = self.appstore_handler.get_packages(silent = True)
			if packages:
				to_be_installed = []
				to_be_updated = []
				unchanged = []
				if self.originaljson:
					for package in self.originaljson["packages"]:
						installed_version = self.appstore_handler.get_package_version(package)
						if not installed_version or installed_version == "not installed":
							to_be_installed.append(package)
							continue
						latest_version = self.appstore_handler.clean_version(self.repo_parser.get_latest_version(package), package)
						if not self.appstore_handler.clean_version(installed_version, package) == latest_version:
							to_be_updated.append(package)
							continue
						else:
							unchanged.append(package)
					self.clear_apply_listboxes()
					if to_be_installed:
						for package in to_be_installed:
							self.applier_to_be_installed_listbox.insert("end", package)
					if to_be_updated:
						for package in to_be_updated:
							self.applier_to_be_updated_listbox.insert("end", package)
					if unchanged:
						self.applier_to_be_unchanged_listbox.config(state = "normal")
						for package in unchanged:
							self.applier_to_be_unchanged_listbox.insert("end", package)
						self.applier_to_be_unchanged_listbox.config(state = "disable")
					self.applier_to_be_installed_listbox.selection_set(0, "end")
					self.applier_to_be_updated_listbox.selection_set(0, "end")

	def clear_apply_listboxes(self):
		for listbox in (self.applier_to_be_installed_listbox, self.applier_to_be_updated_listbox, self.applier_to_be_unchanged_listbox):
			listbox.config(state = "normal")
			listbox.delete(0, "end")
		self.applier_to_be_unchanged_listbox.config(state = "disabled")