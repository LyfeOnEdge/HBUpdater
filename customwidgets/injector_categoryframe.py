from .categoryframe import categoryFrame
from .storeappsquare import storeAppSquare

class injector_categoryFrame(categoryFrame):
    def __init__(self,parent,controller,framework, repos):
        self.last_packages = []
        self.local_packages_handler = controller.local_packages_handler
        categoryFrame.__init__(self, parent,controller,framework,repos)
        framework.add_on_refresh_callback(lambda: self.rebuild())

    #instantiates button, adds it to list
    def makeButton(self,frame, framework, repo):
        button = storeAppSquare(frame, self.controller, framework, self, repo,self.show_payload_injector, self.local_packages_handler)
        self.buttons.append(button)

    def show_payload_injector(self, repo):
        self.controller.frames["injectorPage"].show(repo)