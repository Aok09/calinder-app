class MouseEventHandler:
    def __init__ (self):
        self.MouseWasOver = None
        self.MouseIsOver = None
        self.OverCalinderGrid = False
        self.OverEventsOfToday = False
        self.OnDeatails = None

    def WhereIsMouse(self, event, ScreenCordanteData):
        # checks if the mouse is still over the thing from last time 
        # if it is just return what it found the last time
        if self.MouseWasOver is not None:
            MouseIsStillHere = self.MouseWasOver[0] < event.x < self.MouseWasOver[2] and self.MouseWasOver[1] < event.y < self.MouseWasOver[3]
            if MouseIsStillHere:
                return {"Outline": self.MouseWasOver, "WhatIsOn": [self.OverCalinderGrid, self.OverEventsOfToday], "Deatils": self.OnDeatails} 
        

        # checks if the mouse is in the calinder grid
        LCGB = ScreenCordanteData["CalinderGrid"]["HitBox"]
        self.OverCalinderGrid = LCGB[0] < event.x < LCGB[2] and LCGB[1] < event.y < LCGB[3]
        if self.OverCalinderGrid: 
            # if the mouse is over the calinder then kick it over to the thing
            self.WhatDayIsTheMouseOver(ScreenCordanteData, event)
        
        # checks if the mouse is over events of the day 
        LCGB = ScreenCordanteData["EventsOfToday"]["HitBox"]
        self.OverEventsOfToday = LCGB[0] < event.x < LCGB[2] and LCGB[1] < event.y < LCGB[3]
        if self.OverEventsOfToday:
            # if it is then its kicked over to the be dealth with over there 
            self.WhatEventIsTheMouseOver(ScreenCordanteData, event)

        # checks all and if all are false then it is set back to None
        if not self.OverCalinderGrid and not self.OverEventsOfToday:
            self.MouseWasOver = None
        
        return {"Outline": self.MouseWasOver, "WhatIsOn": [self.OverCalinderGrid, self.OverEventsOfToday], "Deatils": self.OnDeatails} 
    def WhatDayIsTheMouseOver(self, ScreenCordanteData, event):
        DOD = ScreenCordanteData["CalinderGrid"]["TheDayArray"]
        Searching  = False
        while True:
            # checks all the days 
            for Day in DOD:
                # cehcks each day in tern
                Outer = ScreenCordanteData["CalinderGrid"]["TheDayArray"][Day]["MainBox"]
                Found = Outer[0] < event.x < Outer[2] and Outer[1] < event.y < Outer[3]

                if Found: # if is the day then it sets it and returns to the main function
                    self.MouseWasOver = Outer
                    self.OnDeatails = ScreenCordanteData["CalinderGrid"]["TheDayArray"][Day]
                    return

            self.MouseWasOver = None
            return

    def WhatEventIsTheMouseOver(self, ScreenCordanteData, event):
        # no data to handle at the moment so just sets it as the main box and thats it
        self.MouseWasOver = ScreenCordanteData["EventsOfToday"]["HitBox"]
        pass