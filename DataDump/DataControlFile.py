from pathlib import Path

import json, os, re, time
class DataControler:
    def __init__(self):
        # grabs the path to THIS file 
        self.ScriptDir = os.path.dirname(os.path.abspath(__file__))
        
        with open(os.path.join(self.ScriptDir, "Holidays\\UkHolidaysNewFile.json"), "r") as File:
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


    def SaveEventData(self, EventData):
        Pathed = Path(f"{self.ScriptDir}\\UserEvents\\{EventData['Date'][0]}\\{EventData['Date'][1]}\\{EventData['Date'][2]}\\DayEvents.json")

        if not Pathed.exists():
            # Create folders if needed
            Pathed.parent.mkdir(parents=True, exist_ok=True)

            # Write JSON correctly
            with open(Pathed, "w", encoding="utf-8") as File:
                json.dump({time.time():EventData}, File, indent=4)

            return
        
        if Pathed.exists():
            with open(Pathed, "r", encoding="utf-8") as File:
                OpendFile = json.load(File)
            
            OpendFile[time.time()] = EventData
            
            with open(Pathed, "w", encoding="utf-8") as File:
                json.dump(OpendFile, File, indent=4)

    def GetDayEvents(self, Date):
        Pathed = Path(f"{self.ScriptDir}\\UserEvents\\{Date[0]}\\{int(Date[1])}\\{Date[2]}\\DayEvents.json")

            

        if Pathed.exists():
            with open(Pathed, "r", encoding="utf-8") as File:
                OpendFile = json.load(File)
            
            return OpendFile

        return []