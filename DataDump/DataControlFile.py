import json, os, re
class DataControler:
    def __init__(self):
        # grabs the path to THIS file 
        self.ScriptDir = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(self.ScriptDir, "UkHolidaysNewFile.json"), "r") as File:
            self.UkHolidays = json.load(File)


    def GetHoldaysForDayX(self, Date):
        # the date is stored so that the month and day have a 0 if thay are less than 10 
        # this just adds a 0 if the input date is less that 10 so thay match
        Date[1] = f"0{Date[1]}" if len(str(Date[1])) == 1 else Date[1]
        Date[2] = f"0{Date[2]}" if len(str(Date[2])) == 1 else Date[2]
        
        # puts the date togeth into and then checks it
        TextDate = f"{Date[0]}-{Date[1]}-{Date[2]}"
        if TextDate in self.UkHolidays:
            holday = self.UkHolidays[TextDate]

            # some of the data got fucked in translation so it just removes any of the unwated ucky ness
            CleanedText = holday.encode("ascii", "ignore").decode()
            
            return CleanedText
        
        return " "


