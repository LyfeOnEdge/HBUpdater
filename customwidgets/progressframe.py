import tkinter as tk
from style import *
from widgets import button, progBar
from PIL import Image, ImageTk
import style

class progressFrame(tk.Frame):
    def __init__(self, frame):
        tk.Frame.__init__(self,frame,background=color_1)
        self.framework = frame
        self.progress = None
        self.progress_text = tk.StringVar()
        self.title = tk.StringVar()
        self.placed = False
        self.value = 0
        self.display_value = 0

        self.progresstitle = tk.Label(self,
            background = color_1,
            highlightthickness=0,
            anchor="center",
            font=hugeboldtext,
            foreground= w,
            textvariable = self.title,
            ).place(relwidth = 1, relheight = 0.25, width = -2*offset, rely = 0.25, y = - (2 * progressbarheight + 2 * offset))

        self.progbartext = tk.Label(self,
            background = color_1,
            highlightthickness=0,
            anchor="center",
            font=largeboldtext,
            foreground= lg,
            textvariable = self.progress_text,
            ).place(relwidth = 1, height = progressbarheight, width = -2*offset, rely = 0.5, y = - (2 * progressbarheight + 2 * offset))

        self.progbar = progBar(self)
        self.progbar.Place(relwidth = 1, height = progressbarheight, width = -2*offset, rely = 0.5, y = - progressbarheight / 2)

        self.back_image = ImageTk.PhotoImage(Image.open("assets/return.png").resize((style.buttonsize, style.buttonsize), Image.ANTIALIAS))
        self.backbutton = button(self, image_object=self.back_image, callback=self.hide, background=style.color_1)
        self.backbutton.place(rely=1,relx=1,x = -(style.buttonsize + style.offset), y = -(style.buttonsize + style.offset))


    def set_title(self, title):
        self.title.set(title)

    def update(self, update_text, update_percent_int):
        if not update_percent_int or update_percent_int == 100:
            self.hide()
            self.progress_text.set("")
            self.value = 0
            self.update_loop()
        else:
            self.show()
            self.progress_text.set(update_text + " ~ {}%".format(update_percent_int))
            self.value = update_percent_int
            self.update_loop()

    def update_loop(self):
        if self.value:
            if self.display_value < self.value:
                self.display_value += 1
                self.progbar.setValue(self.display_value)
                self.framework.schedule_callback(self.update_loop, 100)
            else:
                self.display_value = self.value
                self.progbar.setValue(self.value)
        else:
            self.progbar.setValue(0)

    def show(self):
        self.place(relwidth = 1, relheight = 1)
        self.placed = True

    def hide(self):
        self.place_forget()
        self.placed = False
        self.clear()

    def clear(self):
        self.progress_text.set("")
        self.set_title("")
        self.progbar.setValue(0)

    def Place(self):
        self.show()