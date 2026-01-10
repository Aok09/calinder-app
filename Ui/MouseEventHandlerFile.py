class MouseEventHandler:
    def __init__ (self):
        print("mouse")
        self.MouseWasOver = None
        self.MouseIsOver = None
    def WhereIsMouse(self, event, ScreenCordanteData):
        # checks if the mouse is still over the thing from last time 
        # if it is just return what it found the last time
        if self.MouseWasOver is not None:
            MouseIsStillHere = self.MouseWasOver[0] < event.x < self.MouseWasOver[2] and self.MouseWasOver[1] < event.y < self.MouseWasOver[3]
            if MouseIsStillHere:
                return self.MouseWasOver
        
        # checks if the mouse is in the calinder grid
        LCGB = ScreenCordanteData["CalinderGrid"]["HitBox"]
        OverCalinderGrid = LCGB[0] < event.x < LCGB[2] and LCGB[1] < event.y < LCGB[3]
        if OverCalinderGrid:
            self.WhatDayIsTheMouseOver(ScreenCordanteData, event)
            
        else:
            self.MouseWasOver = None
        
        return self.MouseWasOver
    def WhatDayIsTheMouseOver(self, ScreenCordanteData, event):

        DOD = ScreenCordanteData["CalinderGrid"]["TheDayArray"]
        Searching  = False
        while True:
            for Day in DOD:
                Outer = ScreenCordanteData["CalinderGrid"]["TheDayArray"][Day]["MainBox"]
                Found = Outer[0] < event.x < Outer[2] and Outer[1] < event.y < Outer[3]

                if Found:
                    self.MouseWasOver = Outer
                    return

            self.MouseWasOver = None
            return