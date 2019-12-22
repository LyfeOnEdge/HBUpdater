import platform
import tkinter as tk
from PIL import Image, ImageTk
from timeit import default_timer as timer
import style
from .storeappsquare import storeAppSquare
from widgets import ThemedLabel
from locations import notfoundimage
from asyncthreader import threader
from settings_tool import settings
from HBUpdater import store_handler

class categoryFrame(tk.Frame):
    def __init__(self,parent,controller,framework, repos):
        #list of repos to be displayed by this frame
        self.repos = repos
        self.parent = parent
        self.controller = controller #Frame manager
        self.framework = framework #**Scheduler
        self.appstore_handler = store_handler #Tool to get installed package data etc
        self.buttons = []   #List to hold buttons for this page
        self.original_button_order = []
        self.selected = False
        self.is_displaying = False #Debounce used for the display function to prevent multiple threads grabbing an updated image
        self.is_searching = True #Used to remember if we are currently searching
        self.currentsearch = False #Used to remember the current qued search term (helps with search lag)
        self.lastsearch = False #Used to remember the last term searched
        self.searchtimer = None
        self.sort_type = None
        self.thumbnailheight = None
        self.thumbnailwidth = None

        tk.Frame.__init__(self, parent, background = style.w, border = 0, highlightthickness = 0)

        #Shared images for the squares
        self.get_image = ImageTk.PhotoImage(Image.open("assets/GET.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.installed_image = ImageTk.PhotoImage(Image.open("assets/INSTALLED.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.update_image = ImageTk.PhotoImage(Image.open("assets/UPDATE.png").resize((style.statussize, style.statussize), Image.ANTIALIAS))
        self.notfoundimage = ImageTk.PhotoImage(Image.open(notfoundimage).resize((style.large_thumbnail_width, style.large_thumbnail_width - 10), Image.ANTIALIAS))

        self.status_map = {
            "UPTODATE" : self.installed_image,
            "NEEDSUPDATE" : self.update_image,
            "NOTINSTALLED" : self.get_image
        }

        #make canvas and scroll bar
        self.canvas = tk.Canvas(self, bg=style.color_2, relief=tk.constants.SUNKEN)
        self.canvas.config(
            width=100, #Parent frame width
            highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, troughcolor = style.color_1, bg = style.color_2)

        #Bind sidebar to canvas and vv
        self.scrollbar.config(command=self.on_scroll_bar)           
        self.canvas.config(yscrollcommand=self.scrollbar.set) 

        #pack the sidebar and canvas
        self.scrollbar.pack(side=tk.constants.RIGHT, fill=tk.constants.Y)                     
        self.canvas.pack(side=tk.constants.LEFT, expand=tk.constants.YES, fill=tk.constants.BOTH)

        #A frame to put in the canvas window
        self.canvas_frame = tk.Frame(self.canvas, background = style.color_2, border = 0, highlightthickness = 0)
        self.canvas_frame.on_mouse_wheel = self.on_mouse_wheel
        #Creates a "window" and places the canvas in it
        self.canvas.create_window(0,0, window=self.canvas_frame, anchor='nw')

        #Bind resize
        self.bind("<Configure>", self.configure)

        if platform.system() == 'Windows' or platform.system() == "Darwin":
            self.canvas_frame.bind("<MouseWheel>", self.on_mouse_wheel)
            self.bind("<MouseWheel>", self.on_mouse_wheel)
        elif platform.system() == "Linux":
            self.canvas_frame.bind("<Button-4>", self.on_mouse_wheel)
            self.canvas_frame.bind("<Button-5>", self.on_mouse_wheel)
            self.bind("<Button-4>", self.on_mouse_wheel)
            self.bind("<Button-5>", self.on_mouse_wheel)

        #Bind frame raise
        self.bind("<<ShowFrame>>", self.configure)

        self.set_sort_type("name-")

        #Build buttons from passed repo
        self.makeButtonList()
        self.rebuild()

        self.framework.add_on_refresh_callback(self.clear_then_update)

    def open_details(self, repo):
        self.controller.frames["detailPage"].show(repo)

    def select(self):
        self.selected = True
        self.rebuild()

    def deselect(self):
        self.selected = False

    def is_selected(self):
        return self.selected

    def rebuild(self):
        self.clear()
        self.update_button_sizes()
        self.buildFrame()
        self.update_displayed_buttons()

    def update_button_sizes(self):
        thumbnail_size_map = {
            "tiny" : (style.tiny_thumbnail_height, style.tiny_thumbnail_width),
            "small" : (style.small_thumbnail_height, style.small_thumbnail_width),
            "medium" : (style.medium_thumbnail_height, style.medium_thumbnail_width),
            "large" : (style.large_thumbnail_height, style.large_thumbnail_width),
            "huge" : (style.huge_thumbnail_height, style.huge_thumbnail_width)
        }

        thumbnail_size = settings.get_setting("thumbnail_size")
        thumbnail_size = thumbnail_size_map.get(thumbnail_size)

        if thumbnail_size:
            self.thumbnailheight = thumbnail_size[0]
            self.thumbnailwidth = thumbnail_size[1]

    def makeButtonList(self):
        self.buttons = []
        for repo in self.repos:
            self.makeButton(self.canvas_frame, self.framework, repo)

        self.original_button_order = self.buttons[:]

    #instantiates button, adds it to list
    def makeButton(self,frame, framework, repo):
        button = storeAppSquare(frame, self.controller, framework, self, repo,self.open_details, self.appstore_handler)
        self.buttons.append(button)

        #Tiles buttons
    def buildFrame(self): 
        #If frame is visible
        if self.selected:
            #if there is content to build with
            if self.buttons:
                self.buttons = self.original_button_order[:]
                reverse = False
                if self.sort_type:
                    sort_type = self.sort_type
                    if sort_type.endswith("-"):
                        sort_type = sort_type.strip("-")
                        reverse = True

                    self.buttons.sort(key=lambda x: x.repo[sort_type], reverse = reverse)

                # buildstart = timer()
                x_spacing = self.thumbnailwidth + 2 * style.offset
                y_spacing = self.thumbnailheight + 13 * style.offset
                #Set the width 
                scrollbar_width = self.scrollbar.winfo_width()
                if scrollbar_width == 1:
                    scrollbar_width = 16
                _framewidth = self.winfo_width() - scrollbar_width
                if _framewidth <= 0:
                    return
                self.canvas_frame.config(width=_framewidth)

                #Get integer number of tiles fittable in the window
                _maxperrow = _framewidth // x_spacing

                #If there's not enough room to build anything
                if not _maxperrow:
                    _maxperrow = 1

                empty_space = _framewidth - (_maxperrow * x_spacing)

                space_offset = empty_space / (_maxperrow + 1)

                _y = 0
                _x = 0

                for button in self.buttons:
                    if button.active:
                        base_y = _y * y_spacing + style.offset
                        base_x = _x * (x_spacing) + style.offset + (_x + 1) * (space_offset)
                        button.set_xy_canvas(base_x, base_y, self.canvas_frame)
                        _x += 1

                        if _x == _maxperrow:
                            _x = 0
                            _y += 1
                    else:
                        button.set_xy_canvas(None, None, None)

                #Update the size of the canvas and configure the scrollable area
                _canvasheight = (_y + 1) * (y_spacing)
                if _canvasheight < self.winfo_height():
                    _canvasheight = self.winfo_height()

                self.canvas_frame.config(height = _canvasheight,width= _framewidth)
                self.canvas.config(scrollregion=(0,0,_framewidth, _canvasheight))
                # buildend = timer()
                # print("build took {} seconds".format(buildend - buildstart))
            else:
                self.clear()

    def update_displayed_buttons(self):
        if not self.is_displaying:
            self.is_displaying = True
            #If frame is visible
            if self.selected:
                button_height = self.thumbnailheight + 13 * style.offset
                canvas_height = self.canvas_frame.winfo_height()
                if not canvas_height:
                    print("canvas height is zero")
                    return

                ratio = 1 / canvas_height

                viewable_buffer = (3 * button_height) * ratio

                #add a buffer to the range to search for buttons that need placing
                canvas_top = self.canvas.yview()[0] - viewable_buffer
                if canvas_top < 0:
                    canvas_top = 0

                canvas_bottom = self.canvas.yview()[1] + viewable_buffer
                if canvas_bottom > 1:
                    canvas_bottom = 1

                for button in self.buttons:
                    if not button.placed:
                        #If button has been designated to be placed on the canvas
                        if button.get_xy()[1]:
                            button_y_proportion = button.get_xy()[1] * ratio
                            if canvas_top < button_y_proportion and button_y_proportion < canvas_bottom:
                                threader.do_async(button.build_button, [], priority = "low")
            self.is_displaying = False

    def clear_then_update(self):
        self.clear()
        self.update_displayed_buttons()


    def search(self, searchterm):
        self.is_searching = True
        self.currentsearch = searchterm
        self.searchtimer = timer()
        self.controller.after(100, self.search_poll())

    def search_poll(self):
        if self.is_searching:
            #.4 second delay on search debouncer
            if (timer() - self.searchtimer) > (0.25):
                threader.do_async(self.do_search_query, [], priority = "low")
            else:
                self.controller.after(100, self.search_poll)

    def do_search_query(self):
        def doSearch(searchterm):
            search_categories = ["name", "package", "author", "description"]
            for button in self.buttons:
                button.active = False
                for category in search_categories:
                    compare_string = button.repo[category]
                    if compare_string:
                        if searchterm.lower() in compare_string.lower():
                            button.active = True
                            break

        if self.currentsearch:
            doSearch(self.currentsearch)
        else:
            for button in self.buttons:
                button.active = True

        self.is_searching = False
        self.lastsearch = self.currentsearch
        self.currentsearch = None

        self.rebuild()

        #Most efficiant way to un-place items on the canvas
    def clear(self):
        for child in self.canvas_frame.winfo_children():
            child.place_forget()
        for button in self.buttons:
            button.placed = False

    def configure(self, event):
        self.buildFrame()
        self.framework.refresh()

    def on_mouse_wheel(self, event):
        try:
            if platform.system() == 'Windows':
                self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            elif platform.system() == "Linux":
                if event.num == 5:
                    self.canvas.yview_scroll(1, "units")
                if event.num == 4:
                    self.canvas.yview_scroll(-1, "units")
            elif platform.system() == "Darwin":
                self.canvas.yview_scroll(event.delta, "units")

            self.update_displayed_buttons()
            return "break"
        except:
            pass

    def on_scroll_bar(self, move_type, move_units, __ = None):
        if move_type == "moveto":
            self.update_displayed_buttons()
            self.canvas.yview("moveto", move_units)

    def set_sort_type(self, sort_type):
        self.sort_type = sort_type