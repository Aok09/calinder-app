from screeninfo import get_monitors
import tkinter as tk

from Ui.ColorControlFile import ColorControl
from Ui.MainWindowFile import CreateUiElimants as Eliment

import time
class MainWindow(tk.Tk):
    """docstring for MainWindow"""
    def __init__(self):
        super().__init__() # this is what tels the class to use tk
        self.CC = ColorControl() # this is the color control 
        self.Monitor = get_monitors()[0] # gets the second monitor

        self.TBDOTTAR = [] # or TheBigDictOfThingsThatAreRenderd :)
        # creates the window and places it on the second screen
        self.geometry(f"+{self.Monitor.x}+{self.Monitor.y}")
        self.state("zoomed")
        
        # crates the canvas
        self.CalinderCanvas = tk.Canvas(self, bg=self.CC.DarkBackGroundColor())
        self.CalinderCanvas.pack(fill="both", expand=True)

        self.after(10, self.OnStart)
        self.mainloop()

    def OnStart(self):
        DayEventsBGC = Eliment().BuildDayEvents(self, self.CalinderCanvas) # creates the side bar to view the the events of today
        self.TBDOTTAR.append(DayEventsBGC)

MainWindow()