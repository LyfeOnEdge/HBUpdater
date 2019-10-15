#A tool to minimize unnecessary copies of the same image object with multiple icons sharing the same image
class icon_dict():
    def __init__(self):
        self.images = {}

    def get_image(self, keyword):
        if keyword in self.images.keys():
            return self.images[keyword]

    def set_image(self, keyword, tk_image_object):
        self.images[keyword] = tk_image_object