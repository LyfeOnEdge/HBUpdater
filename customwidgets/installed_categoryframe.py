from .categoryframe import categoryFrame

class installed_categoryFrame(categoryFrame):
    def __init__(self,parent,controller,framework, repos):
        self.last_packages = []
        categoryFrame.__init__(self, parent,controller,framework, repos)
        framework.add_on_refresh_callback(lambda: self.rebuild())
        
    def makeButtonList(self):
        self.packages = []

        if self.appstore_handler.packages:
            if not self.appstore_handler.packages == self.last_packages:
                print("Remaking")
                for package in self.appstore_handler.packages:
                    for repo in self.repos:
                        if repo["name"] == package:
                            self.packages.append(repo)
                            break
                self.last_packages = self.appstore_handler.packages

                self.buttons = []
                for repo in self.packages:
                    self.makeButton(self.canvas_frame, self.framework, repo)
                self.original_button_order = self.buttons[:]
        else:
            self.buttons = []

        self.buildFrame()

    def rebuild(self):
        self.clear()
        self.update_button_sizes()
        self.makeButtonList()
        self.update_displayed_buttons()