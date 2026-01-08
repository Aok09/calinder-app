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
            LittleTempList.append(T4)

        return LittleTempList


    def BuildMonthDayGrid(self, Window, MainCanvas):
        # the main calinder grid is:
        # top left: 360 x 150 - to give space for the title/month or what ever
        # the bottem right: the window size -10 in both directions  
        # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
        # this still needs to be more intorctive for the months so that it knows what days are "active"
        # i am not sure if this is the function to handle the event data yet, 
        # it could hand back the data on newly placed as well as the needed coords

        # todo [ ] make these dynamic
        StaticTopWidthoffset = 360
        StaticTopHightOffset = 150
        StaticBottomWidthOffset = Window.winfo_width() - 10
        StaticBottomHightOffset = Window.winfo_height() - 10

        # test squere to check if i put in the right spot
        # MainCanvas.create_rectangle(StaticTopWidthoffset, StaticTopHightOffset, StaticBottomWidthOffset, StaticBottomHightOffset, fill="red", outline="pink")
        
        # creates the actual working space i have for the main calinder squeres
        WorkingWidth = StaticBottomWidthOffset - StaticTopWidthoffset
        WorkingHight = StaticBottomHightOffset - StaticTopHightOffset
        
        # the size of each day box
        DayWidth = WorkingWidth/7
        DayHight = WorkingHight/6

        # the active off set that changes to place each day correclty
        DayWidthOffSet = StaticTopWidthoffset
        DayHightOffSet = StaticTopHightOffset

        #creates the calnder gird that is 7 across and 6 down
        for Hight in range(6): # how meany weeks to add
            for Width in range(7): # how meany days in a week
                MainCanvas.create_rectangle(
                    DayWidthOffSet, DayHightOffSet, # top left
                    DayWidthOffSet+DayWidth, DayHightOffSet+DayHight, # bottom right 
                    fill=self.CC.LightBackGroundColor(), 
                    outline=self.CC.HighLightColor())

                DayWidthOffSet += DayWidth # adds the correct offset 
            DayWidthOffSet = StaticTopWidthoffset # resets the day row 
            DayHightOffSet += DayHight # adds the correct offset 