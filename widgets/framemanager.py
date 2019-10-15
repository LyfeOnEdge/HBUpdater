#Heavily customized class to manage frames in the outermost layer
import tkinter as tk

#Frame handler, raises and pages in z layer,
#also
class frameManager(tk.Tk):
    def __init__(self, 
                pages, #List of pages to put in outermost z-layer
                geometry, #Startup size
                async_threader, #object to easily deal with a few async function
                image_sharer, #Simple tool to have one base location to lookup images
                update_status = None #Whether or not the app needs an update
                ): 
        tk.Tk.__init__(self)
        self.update_status = update_status
        self.async_threader = async_threader
        self.image_sharer = image_sharer
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
            print("No pages found")


    def show_frame(self, page_name):
        #Show frame for the given page name
        frame = self.frames[page_name]
        frame.event_generate("<<ShowFrame>>")
        frame.tkraise()

if __name__ == "__main__":
    app = App()
    app.mainloop()