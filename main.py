from screeninfo import get_monitors
import tkinter as tk
from datetime import date
import time

from Ui.ColorControlFile import ColorControl
from Ui.MainWindowFile import CreateUiElimants
from Ui.FontControlFile import FontControl
from Ui.MouseEventHandlerFile import MouseEventHandler

class MainWindow(tk.Tk):
    """docstring for MainWindow"""
    def __init__(self):

        super().__init__() # this is what tels the class to use tk

        self.CC = ColorControl() # this is the color control 
        self.MEH = MouseEventHandler()
        self.ElemntBuilder = CreateUiElimants()

        self.Monitor = get_monitors()[0] # gets the second monitor
        self.WorkingDate = [int(date.today().year), int(date.today().month), int(date.today().day)]
        print (f"year: {date.today().year}")
        print (f"month: {date.today().month}")
        print (f"day: {date.today().day}")
        self.RenderdOnScreen = {}
        self.ToBeRenderdOnScreen = []
        # creates the window and places it on the second screen
        self.geometry(f"+{self.Monitor.x}+{self.Monitor.y}")
        self.state("zoomed")
        
        # crates the canvas
        self.CalinderCanvas = tk.Canvas(self, bg=self.CC.DarkBackGroundColor())
        self.CalinderCanvas.pack(fill="both", expand=True)

        self.bind("<Button-1>", self.OnClick)
        self.bind("<Motion>", self.MouseMoved)
        self.bind("<MouseWheel>", self.ScrollWheel)

        self.after(1, self.OnStart)
        self.mainloop()

    def OnStart(self):
        print ("run start")

        
        EventsToday = self.ElemntBuilder.BuildDayEvents(self, self.CalinderCanvas) # creates the side bar to view the the events of today
        self.RenderdOnScreen["EventsOfToday"] = EventsToday


        CalinderGrid = self.ElemntBuilder.BuildMonthDayGrid(self, self.CalinderCanvas, self.WorkingDate) 
        self.RenderdOnScreen["CalinderGrid"] = CalinderGrid


        # places the hand on todays events display
        self.after(1, self.PlaceingTheLargeHandLoop)
        
        # places the the clock and titles
        self.after(1, self.UpdateClockAndTitle)


    def PlaceingTheLargeHandLoop(self):
        self.after(60000, self.PlaceingTheLargeHandLoop)
        WhereHand = self.ElemntBuilder.PlaceLargeHand(self, self.CalinderCanvas)
        self.RenderdOnScreen["TheLargeHand"] = [WhereHand]

    def UpdateClockAndTitle(self):
        self.ElemntBuilder.CreateCorrectTittles(self, self.CalinderCanvas, self.WorkingDate)
        TimeTillUpdate = ((1-(time.time()%1))*1000)+70
        self.after(int(TimeTillUpdate), self.UpdateClockAndTitle)

    def MouseMoved(self, event):
        # return
        HoveringOver = self.MEH.WhereIsMouse(event, self.RenderdOnScreen)

    def OnClick(self, event):
        ClickingOn = self.MEH.WhereIsMouse(event, self.RenderdOnScreen)
    
    def ScrollWheel(self, event):
        ScrollingOn = self.MEH.WhereIsMouse(event, self.RenderdOnScreen)
        print(ScrollingOn)
        
        # if scrolling on the main calinder view
        if ScrollingOn["WhatIsOn"][0] == True:
            print (event)
            UporDown = 1 if event.delta == 120 else -1
            self.WorkingDate[1] = int(self.WorkingDate[1]) + UporDown 
            CalinderGrid = self.ElemntBuilder.BuildMonthDayGrid(self, self.CalinderCanvas, self.WorkingDate) 
            self.ElemntBuilder.CreateCorrectTittles(self, self.CalinderCanvas, self.WorkingDate)

            self.RenderdOnScreen["CalinderGrid"] = CalinderGrid

MainWindow()