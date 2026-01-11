from screeninfo import get_monitors
import tkinter as tk
import time, calendar, inspect, copy
from datetime import datetime
from Ui.ColorControlFile import ColorControl

class CreateEventWindow(tk.Tk):
    def __init__(self, WorkingDate, InputData, StartTime=[datetime.now().hour, datetime.now().minute], EndTime=[datetime.now().hour, datetime.now().minute]):
        
        # if a day that is not in the month is clicked on
        if InputData["Deatils"]["DayData"]["DaysDate"] == 0:
            return "InvalidDay"

        super().__init__() # this is what tels the class to use tk
        
        self.StartTime = StartTime
        self.EndTime = EndTime

        self.ClickedOnDate = [WorkingDate[0], WorkingDate[1], InputData["Deatils"]["DayData"]["DaysDate"]]
        self.title(f"looking at: {self.ClickedOnDate[0]}/{self.ClickedOnDate[1]}/{self.ClickedOnDate[2]}")


        self.CC = ColorControl() # this is the color control

        self.Monitor = get_monitors()[0] # gets the second monitor
        self.geometry(f"500x400")

        self.after(1, self.BuildUi)
        self.mainloop()


    def BuildUi(self):

        # --- YEAR ---
        tk.Label(self, text="Year").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.YearInputData = tk.Entry(self, width=10)
        self.YearInputData.insert(0, self.ClickedOnDate[0])
        self.YearInputData.grid(row=0, column=1, padx=10, pady=5)

        # --- MONTH ---
        tk.Label(self, text="Month").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.MonthInputData = tk.Entry(self, width=10)
        self.MonthInputData.insert(0, self.ClickedOnDate[1])
        self.MonthInputData.grid(row=1, column=1, padx=10, pady=5)

        # --- DAY ---
        tk.Label(self, text="Day").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.DayInputData = tk.Entry(self, width=10)
        self.DayInputData.insert(0, self.ClickedOnDate[2])
        self.DayInputData.grid(row=2, column=1, padx=10, pady=5)

        # --- TITLE ---
        tk.Label(self, text="Title").grid(row=3, column=0, sticky="w", padx=10, pady=5)
        self.EventTitle = tk.Entry(self, width=30)
        self.EventTitle.grid(row=3, column=1, padx=10, pady=5)

        # --- HOUR ---
        tk.Label(self, text="Hour").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.StartHourInputData = tk.Entry(self, width=10)
        self.StartHourInputData.insert(0, self.StartTime[0])
        self.StartHourInputData.grid(row=4, column=1, padx=10, pady=5)

        # --- MINUTE ---
        tk.Label(self, text="Minute").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.StartMinuteInputData = tk.Entry(self, width=10)
        self.StartMinuteInputData.insert(0, self.StartTime[1])
        self.StartMinuteInputData.grid(row=5, column=1, padx=10, pady=5)

        # --- HOUR ---
        tk.Label(self, text="Hour").grid(row=4, column=0, sticky="w", padx=10, pady=5)
        self.EndHourInputData = tk.Entry(self, width=10)
        self.EndHourInputData.insert(0, self.EndTime[0])
        self.EndHourInputData.grid(row=4, column=2, padx=10, pady=5)

        # --- MINUTE ---
        tk.Label(self, text="Minute").grid(row=5, column=0, sticky="w", padx=10, pady=5)
        self.EndMinuteInputData = tk.Entry(self, width=10)
        self.EndMinuteInputData.insert(0, self.EndTime[1])
        self.EndMinuteInputData.grid(row=5, column=2, padx=10, pady=5)

        # --- DESCRIPTION ---
        tk.Label(self, text="Description").grid(row=6, column=0, sticky="nw", padx=10, pady=5)
        self.MoreInfoInputData = tk.Text(self, width=40, height=6)
        self.MoreInfoInputData.grid(row=6, column=1, padx=10, pady=5)

        # --- SAVE BUTTON ---
        self.SaveButton = tk.Button(self, text="Save Event", command=self.PackInputData)
        self.SaveButton.grid(row=7, column=1, pady=15)

    def PackInputData(self):
        EventData = {
            "EventTitle": self.EventTitle.get(),
            "EventInfo": self.MoreInfoInputData.get("1.0", "end").strip(),
            "StartTime": [self.StartHourInputData.get(), self.StartMinuteInputData.get()],
            "EndTime": [self.EndHourInputData.get(), self.EndMinuteInputData.get()],
            "Date": [self.YearInputData.get(), self.MonthInputData.get(), self.DayInputData.get()]
        }

        print(EventData)