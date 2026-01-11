import tkinter as tk
from Ui.ColorControlFile import ColorControl
from DataDump.DataControlFile import DataControler
from Ui.FontControlFile import FontControl

import math, calendar, time, inspect

def RoundToSigN(x, sig=3):
    return round(x, sig - int(math.floor(math.log10(abs(x)))) - 1)

class CreateUiElimants():
    """docstring for CreateUiElimants"""
    def __init__(self):
        self.CC = ColorControl() # this is the color control 
        self.DC = DataControler() # this is for data controlling
        self.FC = FontControl() # is for well font control

    def EventsToDay(self):
        pass

    def BuildDayEvents(self, Window, MainCanvas):
        LittleTempList = []
        
        # creates the back ground for day display
        T1 = MainCanvas.create_rectangle(10, 0, 350, Window.winfo_height(), fill=self.CC.LightBackGroundColor(), outline=self.CC.HighLightColor(), tag=f"DayDisplayBackGround")
        LittleTempList.append(T1)
        # T2 = MainCanvas.create_line(175, 0, 175, ScreenData.height, fill=self.CC.HighLightColor())
        # LittleTempList.append(T2)
        HourSepration = RoundToSigN(Window.winfo_height() / 24)-0.1
        offset = 0
        for x in range(25):
            # creates a line for each our in the day at a reguler interval
            T3 = MainCanvas.create_line(20, offset, 340, offset, fill=self.CC.HighLightColor(), tag=f"HourLineSeprator{offset}")
            LittleTempList.append(T3)

            # adds text to see what the hour is
            # todo [ ] add am and pm back 
            Hour = f"{x}"
            if x == 13 or x > 13:
                Hour = f"{x - 12}"
            T4 = MainCanvas.create_text(175, offset-7, text=Hour, fill=self.CC.HighLightColor(), tag=f"HourTextLabel{Hour}")
            offset += HourSepration
            LittleTempList.append(T4)
        
        return {"DayEventsBackingIds": LittleTempList, "HitBox": [10, 0, 350, Window.winfo_height()]}


    def BuildMonthDayGrid(self, Window, MainCanvas, WorkingDate):
        if bool(MainCanvas.find_withtag("TiTheCalinderGridtleCard")):
            MainCanvas.delete("TheCalinderGrid")

        # so that its not just the same array being passed around
        TempDate = [WorkingDate[0], WorkingDate[1], WorkingDate[2], "lol"]

        # this entier function only creates 1 thing
        LittleTempList = []
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

        FistDayOfMonth, MonthLength = calendar.monthrange(int(WorkingDate[0]), int(WorkingDate[1]))

        # this part has become very clunky but it works from my limeted testing and will be easy to update a a later date
        BoxNumber = 0 # the box number it self indopedant of the day 
        DayActive = False # is the day in the month or not 
        DayNumber = 0 # this is the actual in month day

        TheDaysMade = {}

        #creates the calnder gird that is 7 across and 6 down
        for Hight in range(6): # how meany weeks to add
            for Width in range(7): # how meany days in a week

                # this is the part that checks if the day is in the month
                BoxNumber += 1
                if BoxNumber > FistDayOfMonth: 
                    DayActive = True
                    DayNumber += 1
                    if DayNumber > MonthLength:
                        DayActive = False


                DaysHoliday = " "
                DaysActivtys = False
                if DayActive:
                    # selcets the correct color
                    BoxColor = self.CC.LightBackGroundColor()
                    # text color lol
                    TextColor = self.CC.HighLightColor()

                    # for now to get things done, the events are going to loaded from here as i cant think of a better place to add them from
                    TempDate[2] = DayNumber

                    DaysHoliday = self.DC.GetHoldaysForDayX(TempDate)
                    DaysActivtys = self.DC.GetDayEvents(TempDate)

                else:
                    BoxColor = self.CC.DarkBackGroundColor()
                    TextColor = self.CC.DarkBackGroundColor()


                # creates the box 
                T1 = MainCanvas.create_rectangle(
                    DayWidthOffSet, DayHightOffSet, # top left
                    DayWidthOffSet+DayWidth, DayHightOffSet+DayHight, # bottom right 
                    fill=BoxColor, 
                    outline=self.CC.HighLightColor(),
                    tags=(f"DaysInTheMonthBox{BoxNumber}", "TheCalinderGrid", "RenderdOnScreen")
                )
                LittleTempList.append(T1)

                
                # adds the number of the day 
                MainCanvas.create_text(
                    DayWidthOffSet+(DayWidth/16), 
                    DayHightOffSet+(DayHight/8), 
                    text=f"{DayNumber}", 
                    fill=TextColor,
                    tags=(f"DaysInTheMonthNumber{BoxNumber}", "TheCalinderGrid", "RenderdOnScreen")
                )
                
                # this is the text that adds the holiday if there is one
                MainCanvas.create_text(
                    DayWidthOffSet+(DayWidth/8), 
                    DayHightOffSet+(DayHight/8), 
                    text=DaysHoliday, 
                    anchor="w",
                    fill="pink",
                    tags=(f"DaysInTheMonthHoliday{BoxNumber}", "TheCalinderGrid", "RenderdOnScreen")
                )
                
                if DaysActivtys:
                    AmountRenderd = 0
                    for Activity in DaysActivtys:
                        print (Activity)
                        MainCanvas.create_text(
                            DayWidthOffSet+(DayWidth/16), 
                            DayHightOffSet+(DayHight/4)+((DayHight/8)*AmountRenderd), 
                            text=DaysActivtys[Activity]["EventTitle"], 
                            anchor="w",
                            fill="pink",
                            tags=(f"DaysInTheMonthHoliday{BoxNumber}", "TheCalinderGrid", "RenderdOnScreen")
                        )
                        AmountRenderd += 1


                # packs all the data for the day into 1 thing so the mouse knows where it is and what it needs to do
                TheDaysMade[BoxNumber] = {
                    "MainBox": [DayWidthOffSet, DayHightOffSet, DayWidthOffSet+DayWidth, DayHightOffSet+DayHight], 
                    "DayText": [DayWidthOffSet+(DayWidth/16), DayHightOffSet+(DayHight/8)],
                    "holidayText": [DayWidthOffSet+(DayWidth/8), DayHightOffSet+(DayHight/8)], 
                    "DayData": {"events": DaysActivtys, "Holiday": DaysHoliday, "DaysDate": DayNumber if DayActive else 0}
                    }
                
                # this is a debug text 
                # MainCanvas.create_text(DayWidthOffSet+(DayWidth/2), DayHightOffSet+(DayHight/2), text=f"box: {BoxNumber} | day: {DayNumber}", fill=self.CC.HighLightColor())



                DayWidthOffSet += DayWidth # adds the correct offset 
            DayWidthOffSet = StaticTopWidthoffset # resets the day row 
            DayHightOffSet += DayHight # adds the correct offset 
        
        # packs the box size and off set
        BoxSizeData = {
            "TheLittleList": LittleTempList,
            "Width": DayWidth,
            "Hight": DayHight,
            "HitBox": [StaticTopWidthoffset, StaticTopHightOffset, StaticBottomWidthOffset, StaticBottomHightOffset],
            "TheDayArray": TheDaysMade # a dict of each day box 
        }
        # MainCanvas.create_rectangle(StaticTopWidthoffset, StaticTopHightOffset, StaticBottomWidthOffset, StaticBottomHightOffset, fill="red", outline="pink")
        return BoxSizeData 

    def CreateCorrectTittles(self, Window, MainCanvas, WorkingDate):
        
    
        # is there allready a title month 
        if bool(MainCanvas.find_withtag("TitleCard")):
            MainCanvas.delete("TitleCard")



        monthplacement = (Window.winfo_width()/2)+350/4
        # time.strftime('%Y-%m-%d %H:%M:%S')
        Month = (str(calendar.month_name[int(WorkingDate[1])])).upper()
        Month = f"->{Month}<-" if WorkingDate[1] == int(time.strftime("%m")) else Month

        MainCanvas.create_text(
            monthplacement, 75, 
            text=Month, 
            fill=self.CC.HighLightColor(), 
            font=self.FC.TitleFont(), 
            tag="TitleCard"
        )

        MainCanvas.create_text(
            360, 25, 
            text=time.strftime('%Y-%m-%d'), 
            fill=self.CC.HighLightColor(), 
            font=self.FC.TimeFont(), 
            tag="TitleCard",
            anchor="w"
        )

        MainCanvas.create_text(
            360, 55, 
            text=time.strftime('%H:%M:%S'), 
            fill=self.CC.HighLightColor(), 
            font=self.FC.TimeFont(), 
            tag="TitleCard",
            anchor="w"
        )


        
        

    def PlaceLargeHand(self, Window, MainCanvas):

        if bool(MainCanvas.find_withtag("TheLargeHand")):
            MainCanvas.delete("TheLargeHand")

        # gets the amount of seconds we are throuh the day right now 
        Seconds = (int((int(time.strftime('%H'))*60) + int(time.strftime('%M')))*60) + int(time.strftime('%S'))

        # where should the single large hand go
        LargeHand = (Window.winfo_height()/86400)*Seconds

        TheHand = MainCanvas.create_line(20, LargeHand, 340, LargeHand, fill="pink", tag="TheLargeHand")

        return TheHand, [20, LargeHand, 340, LargeHand]
