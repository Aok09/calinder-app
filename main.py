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
        self.ElemntBuilder = Eliment()
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
        print ("run start")
        self.ElemntBuilder.BuildDayEvents(self, self.CalinderCanvas) # creates the side bar to view the the events of today
        self.ElemntBuilder.BuildMonthDayGrid(self, self.CalinderCanvas) 

        # places the hand on todays events display
        self.after(1, self.PlaceingTheLargeHandLoop)
        
        # places the the clock and titles
        self.after(500, self.UpdateClockAndTitle)


    def PlaceingTheLargeHandLoop(self):
        self.after(60000, self.PlaceingTheLargeHandLoop)
        self.ElemntBuilder.PlaceLargeHand(self, self.CalinderCanvas)

    def UpdateClockAndTitle(self):
        self.ElemntBuilder.CreateCorrectTittles(self, self.CalinderCanvas)
        TimeTillUpdate = ((1-(time.time()%1))*1000)+70
        print (TimeTillUpdate)
        self.after(int(TimeTillUpdate), self.UpdateClockAndTitle)


MainWindow()