import threading

class asyncThread(threading.Thread):
    def __init__(self, func, arglist):
        threading.Thread.__init__(self, target=func, args=arglist)
        self.handled = False

    def begin(self):
        self.start()