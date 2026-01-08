from screeninfo import get_monitors
import tkinter as tk

from Ui.MainWindowFile import CreateUiElimants as Eliment

class MainWindow(tk.Tk):
    """docstring for MainWindow"""
    def __init__(self):
        super().__init__() # this is what tels the class to use tk

        self.Monitor = get_monitors()[0] # gets the second monitor

        # creates the window and places it on the second screen
        self.geometry(f"+{self.Monitor.x}+{self.Monitor.y}")
        self.state("zoomed")
        
        # crates the canvas
        self.CalinderCanvas = tk.Canvas(self, bg="#44626d")
        self.CalinderCanvas.pack(fill="both", expand=True)

        Eliment().EventsToDay() # creates the side bar to view the the events of today
        self.mainloop()

MainWindow()