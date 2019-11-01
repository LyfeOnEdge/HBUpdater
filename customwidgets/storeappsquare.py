from PIL import Image, ImageTk
import tkinter as tk
from widgets import ThemedFrame, button, tooltip, ThemedLabel
from appstore import getPackageIcon
from modules.locations import notfoundimage
import style
import platform 

class storeAppSquare(ThemedFrame):
    def __init__(self, parent, controller, framework, category_frame, repo, callback, status_handler):
        self.controller = controller
        self.parent = parent
        self.framework = framework
        self.category_frame = category_frame
        self.repo = repo
        self.name = repo["name"]
        self.callback = callback
        self.status_handler = status_handler
        self.active = True
        self.image_sharer = self.controller.image_sharer
        self.imageset = False
        self.base_x = None #Stores the base x location to build the button from for dynamic building
        self.base_y = None #Stores the base y location to build the button from for dynamic building
        self.canvas = None
        self.placed = False
        ThemedFrame.__init__(self, parent, background = style.w)

        self.buttonobj = button(self,image_object=None,callback=lambda: self.callback(repo),background = style.color_2)
        self.buttonobj.place(relheight=1,relwidth=1)
        
        #Placeholders used by the category frame when building the button, fixes the disappearing text issue
        self.buttontitlelabel = None #Placeholder used for the button title
        self.buttonauthorlabel = None #Placeholder for the button author
        self.buttonversionlabel = None #Placeholder for the current cersion
        self.buttonseparator = None #Placeholder for underline in each button
        self.buttonstatuslabel = None #Placeholder for download / version status

    def set_image(self):
        repo = self.repo
        try:
            package = repo["package"]
        except:
            package = None

        #Checks a shared dict to see if this package already has an image loaded, returns none if not
        self.button_image = self.image_sharer.get_image(package)

        if not self.button_image:
            try:
                image_file = getPackageIcon(package) or notfoundimage
                button_image = Image.open(image_file)

                #Resizes and saves image if it's the wrong size for faster loads in the future
                if not button_image.size[0] == [style.thumbnailwidth, style.thumbnailheight]:
                    button_image = button_image.resize((style.thumbnailwidth, style.thumbnailheight), Image.ANTIALIAS)

                self.button_image = ImageTk.PhotoImage(button_image)
                if not image_file == notfoundimage:
                    self.image_sharer.set_image(package, self.button_image)

            except Exception as e:
                print(e)
                self.button_image = self.category_frame.notfoundimage
                self.image_sharer.set_image(package, self.button_image)

        self.buttonobj.setimage(self.button_image)
        self.imageset = True

    def set_xy_canvas(self, base_x, base_y, canvas):
        self.base_x = base_x
        self.base_y = base_y
        self.canvas = canvas

    def get_xy(self):
        return((self.base_x, self.base_y))

    def build_button(self):
        if not self.placed:            
            if self.base_y and self.base_x and self.canvas:
                self.placed = True
                repo = self.repo

                label_y = self.base_y + style.thumbnailheight - style.buttontextheight + 40

                def place_button():
                    self.place(x=self.base_x, y = self.base_y, height = style.thumbnailheight + 2 * style.offset, width = style.thumbnailwidth)
                    # ttp = "{}\nAuthor: {}\nDownloads: {}".format(repo["description"], repo["author"], repo["downloads"])
                    # self.button_ttp = tooltip(self.buttonobj,ttp)
                
                def place_buttontitlelabel():
                    if not self.buttontitlelabel:
                        self.buttontitlelabel = ThemedLabel(self.canvas,self.repo["name"],anchor="e",label_font=style.mediumboldtext,foreground=style.w,background=style.color_2)
                    self.buttontitlelabel.place(x = self.base_x, y =  label_y - 1.5 * style.buttontextheight, width = style.thumbnailwidth)

                def place_buttonauthorlabel():
                    if not self.buttonauthorlabel:
                        self.buttonauthorlabel = ThemedLabel(self.canvas,self.repo["author"],anchor="e",label_font=style.smallboldtext,foreground=style.lg,background=style.color_2)
                    self.buttonauthorlabel.place(x = self.base_x, y = label_y, width = style.thumbnailwidth)

                def place_buttonstatuslabel():
                    if not self.buttonstatuslabel:
                        self.buttonstatuslabel = ThemedLabel(self.canvas,"",anchor="w",label_font=style.smallboldtext,foreground=style.lg,background=style.color_2)
                    self.buttonstatuslabel.place(x = self.base_x, y = label_y - 1.5 * style.buttontextheight + 4)

                    status = None
                    package = self.repo["package"]
                    if self.status_handler.packages:
                        if package in self.status_handler.packages:
                            installed_version = self.status_handler.get_package_version(package)

                            if self.status_handler.clean_version(installed_version, package) == self.status_handler.clean_version(installed_version, package):
                                status = "UPTODATE"
                            elif self.status_handler.clean_version(installed_version, package) < self.status_handler.clean_version(installed_version, package):
                                status = "NEEDSUPDATE"
                        else:
                            status = "NOTINSTALLED"
                    else:
                        status = "NOTINSTALLED"

                    self.buttonstatuslabel.configure(image=self.category_frame.status_map[status])

                def place_buttonversionlabel():
                    if not self.buttonversionlabel:
                        self.buttonversionlabel = ThemedLabel(self.canvas,self.repo["github_content"][0]["tag_name"],anchor="w",label_font=style.smallboldtext,foreground=style.lg,background=style.color_2)
                    self.buttonversionlabel.place(x = self.base_x, y = label_y)

                def place_buttonseparator():
                    if not self.buttonseparator:
                        self.buttonseparator = tk.Label(self.canvas, background=style.lg, borderwidth= 0)
                    self.buttonseparator.place(x = self.base_x, y = label_y + 2 * style.offset + style.buttontextheight, height = 1, width = style.thumbnailwidth)

                place_button()
                place_buttonauthorlabel()
                place_buttontitlelabel()
                place_buttonstatuslabel()
                place_buttonversionlabel()
                place_buttonseparator()

                if not self.imageset:
                    self.set_image()

                self.items = [
                    self,
                    self.buttonobj,
                    self.buttontitlelabel,
                    self.buttonauthorlabel,
                    self.buttonversionlabel,
                    self.buttonseparator,
                    self.buttonstatuslabel
                ]

                for item in self.items:
                    try:
                        if platform.system() == 'Windows' or platform.system() == "Darwin":
                            item.bind("<MouseWheel>", self.canvas.on_mouse_wheel)
                        elif platform.system() == "Linux":
                            item.bind("<Button-4>", self.canvas.on_mouse_wheel)
                            item.bind("<Button-5>", self.canvas.on_mouse_wheel)
                    except Exception as e:
                        print(e)