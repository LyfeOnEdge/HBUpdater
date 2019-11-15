#LyfeOnEdge 2019
#GPL3
import threading
from .asyncthread import asyncThread
#super basic thread manager
#Only start threads you have no intention of retrieving data from with this
#force_high_priority will force high-priority threads to start on the next timer update even if the limit has been reached
class asyncThreader():
    def __init__(self, max_threads = 16, force_high_priority = True, force_medium_priority = True):
        self.force_high_priority = force_high_priority
        self.force_medium_priority = force_medium_priority
        self.max_threads = max_threads

        self.high_priority_threads = []
        self.medium_priority_threads = []
        self.low_priority_threads = []
        self.unique_thread = {}
        self.running_threads = []

        self.watchdog = None
        self.stopwatchdog = None
        self.watchdogrunning = None
        
        self.update_running_threads()

        self.priority_map = {
                            "high" : self.high_priority_threads,
                            "hi" : self.high_priority_threads,
                            "h" : self.high_priority_threads,
                            "medium" : self.medium_priority_threads,
                            "med" : self.medium_priority_threads,
                            "m" : self.medium_priority_threads,
                            "low" : self.low_priority_threads,
                            "l" : self.low_priority_threads,
                            }

    def do_async(self, func, arglist = [], priority = "low"):
        t = asyncThread(func, arglist)
        #If there is room for another thread do it now, else prioritize it
        if len(self.running_threads) < self.max_threads:
            t.begin()
            self.running_threads.append(t)
        else:
            self.priority_map[priority].append(t)

    def join(self):
        if self.running_threads:
            for t in self.running_threads:
                t.join()
            self.running_threads = []

    def clear_dead_threads(self):
        if self.running_threads:
            for t in self.running_threads:
                if not t.isAlive():
                    t.handled = True
            self.running_threads = [t for t in self.running_threads if not t.handled]

    #Not to be called by user
    def update_running_threads(self):
        self.watchdogrunning = True
        self.clear_dead_threads()
        #Do high, then medium, then low-priority tasks, only do the next if the previous que was empty or finished
        if self.start_threads_and_move_to_running(self.high_priority_threads, force = self.force_high_priority):
            if self.start_threads_and_move_to_running(self.medium_priority_threads, force = self.force_medium_priority):
                self.start_threads_and_move_to_running(self.low_priority_threads)

        if not self.stopwatchdog:
            #Schedule Self
            self.watchdog = threading.Timer(0.05, self.update_running_threads)
            self.watchdog.start()
        else:
            self.stopwatchdog = False
            self.watchdogrunning = False

    #Returns true if there are no remaining threads in the passed list, else we are maxed out
    def start_threads_and_move_to_running(self, threads, force=False):
        #Returns trus if thread started
        def do_start_and_move_to_running():
            if threads:
                t = threads.pop(0)
                t.begin()
                self.running_threads.append(t)
                return True

        if not force:
            while len(self.running_threads) < self.max_threads:
                result = do_start_and_move_to_running()
                if not result:
                    break
            if len(self.running_threads) < self.max_threads:
                return True
        else:
            #Do until all threads in list are started
            while do_start_and_move_to_running():
                pass
            return True

    def exit(self):
        self.join()
        print("Stopping watchdog")
        self.stopwatchdog = True
        while self.watchdogrunning:
            pass
        print("Watchdog stopped")