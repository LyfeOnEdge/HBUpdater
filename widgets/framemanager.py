#Heavily customized class to manage frames in the outermost layer
import tkinter as tk
#Frame handler, raises and pages in z layer,
#also handles making core components like package handlers,
#parsers, and other library-driven functions available to subsystems
class frameManager(tk.Tk):
    def __init__(self,
                pages, #List of pages to put in outermost z-layer
                args,
                geometry
                ):  #Passed args to be accessed globally

        tk.Tk.__init__(self)
        self.args = args
        self.version = None
        self.geometry("{}x{}".format(geometry["width"],geometry["height"]))
        # self.resizable(False, False)

        # the container is where we'll stack a bunch of frames
        # on top of each other, then the one we want visible
        # will be raised above the others
        container = tk.Frame(self, borderwidth = 0, highlightthickness = 0)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Add pages as frames to dict, with keyword being the name of the frame
        self.frames = {}
        if pages:
            for F in (pages):
                frame = F(parent=container, controller=self)
                page_name = F.__name__
                self.frames[page_name] = frame

                #place the frame to fill the whole window, stack them all in the same place
                frame.grid(row=0, column=0, sticky="nsew")
        else:
            print("No pages to initialize.")

    def show_frame(self, page_name):
        #Show frame for the given page name
        frame = self.frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()
        print("raised - {}".format(page_name))

    def set_version(self, version_string):
        self.version = version_string

if __name__ == "__main__":
    app = App()
    app.mainloop()