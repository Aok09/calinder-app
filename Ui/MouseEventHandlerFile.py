class MouseEventHandler:
    def __init__ (self):
        print("mouse")
    def WhereIsMouse(self, event, ScreenCordanteData):
        LCGB = ScreenCordanteData["CalinderGrid"][1]["HitBox"]
        # print (LCGB, event)
        OverCalinderGrid = bool(LCGB[0] < event.x) and bool(LCGB[2] > event.x) and bool(LCGB[1] < event.y) and bool(LCGB[3] > event.y)
        print(OverCalinderGrid)
        if OverCalinderGrid:
            DOD = ScreenCordanteData["CalinderGrid"][1]["TheDayArray"]

            Found = False
            while not Found:
                for Day in DOD:
                    Outer = ScreenCordanteData["CalinderGrid"][1]["TheDayArray"][Day]["MainBox"]
                    Found = bool(Outer[0] < event.x) and bool(Outer[2] > event.x) and bool(Outer[1] < event.y) and bool(Outer[3] > event.y)  

                    if Found:
                        break
                        
                break
            
            print(Day)