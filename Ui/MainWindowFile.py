import tkinter as tk
from Ui.ColorControlFile import ColorControl
import math
def RoundToSigN(x, sig=3):
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

class CreateUiElimants():
    """docstring for CreateUiElimants"""
    def __init__(self):
        print ("imported CreateUiElimants")
        self.CC = ColorControl() # this is the color control 

    def EventsToDay(self):
        print ("events ")

    def BuildDayEvents(self, Window, MainCanvas):
        LittleTempList = []
        
        # creates the back ground for day display
        T1 = MainCanvas.create_rectangle(0, 0, 350, Window.winfo_height(), fill=self.CC.LightBackGroundColor(), outline=self.CC.HighLightColor())
        LittleTempList.append(T1)
        # T2 = MainCanvas.create_line(175, 0, 175, ScreenData.height, fill=self.CC.HighLightColor())
        # LittleTempList.append(T2)
        HourSepration = RoundToSigN(Window.winfo_height() / 24)-0.1
        print (Window.winfo_height(), HourSepration)
        offset = 0
        for x in range(25):
            # creates a line for each our in the day at a reguler interval
            T3 = MainCanvas.create_line(10, offset, 340, offset, fill=self.CC.HighLightColor())
            LittleTempList.append(T3)

            # adds text to see what the hour is
            # todo [ ] add am and pm back 
            Hour = f"{x}"
            if x == 13 or x > 13:
                Hour = f"{x - 12}"
            T4 = MainCanvas.create_text(175, offset-7, text=Hour, fill=self.CC.HighLightColor())
            offset += HourSepration