import calendar, time, os, json, requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import colorchooser, messagebox, font
from pynput import mouse, keyboard

class calendar_window_data(object):
    """docstring for calendar_window_data
adding or changing the color should be easy and is the first thing im going to add due to it being the first thing i found to add on v2


when transerfering dates:
 -- MUST BE: -- 
    [DAY:MONTH:YEAR]
in or out that is the format to use for dates to avoiod having to brake down fuctions
if if one of them is not given or is not output then fill with: -1
this is to fill list spot to keep the values correct but will not error out
#####
[DAY:MONTH:YEAR] -1
#####

Keys:
    CV = Color Variable
    HO = Hand Out
    UIV = User Interface Variable 
    ICV = Internal Calendar Variable
    WV = Window Variable
    VWV = Vital Window Variable
    VIWV = Vital Interal Window Variable 
    """
    def __init__(self, given_date, window_title, color_switch):

        # tk window state 
        # cant find anymore docs on it so am wondwondring why there is "zoomed" in the V2 
        # TODO:
        #   find all the sates and add them as hash after 
        self.WV_state = "zoomed"


        # options for diffrent ways of vewing the calinder
        # 0: months
        # TODO:
        #   add movew viewing methods
        self.UIV_viewing_method = 0

        # the date the calinder is looking for to be transferd to the calnder class
        self.ICV_date_today = given_date

        # simply window title
        self.VWV_title = window_title

        # dict of all the things that are renderd to the main window
        self.VWV_renderd_to_window = {}


        # pass off the the color handler 
        self.color_handler(color_switch)




# section for hadling new colors changing and giving color data when requested
# TODO:
#   alow users to change and save colors to later be imported vie the user file here
    def color_handler(self, color_switch):
        # this is what was used inn the v2 
        # i know its not the best and will be impoved on later
        color_dict = {
            "light_mode":{
                "main_background_color": "green",
                "text_color": ["pink",
                               "orange"],
                "importent": "#3081D0",
                "selected_color": "#faffc7",
                "line_color": "black",
                "button_color": "black",
                "backer_color": "green"
            },
            "dark_mode":{
                "main_background_color": "#161d20",
                "text_color": ["#36498f",
                               "#fbefd0"],
                "importent": "#2d7c9d",
                "selected_color": "#33a29e",
                "line_color": "#e6e6ff",
                "button_color": "164c6d",
                "backer_color": "#1d2125"
            }
        }


        self.CV_background = color_dict[color_switch]["main_background_color"]
        self.CV_text = color_dict[color_switch]["text_color"]
        self.CV_importent = color_dict[color_switch]["importent"]
        self.CV_selected = color_dict[color_switch]["selected_color"]
        self.CV_line = color_dict[color_switch]["line_color"]
        self.CV_button = color_dict[color_switch]["button_color"]
        self.CV_backer = color_dict[color_switch]["backer_color"]

    # this is the start of the running of the main window
    def Window_ingage(self):

        # the window will start fully opened and snaped to windows so it isnt spilling off the screen 
        self.VIWV_main_window = tk.Tk()
        self.VIWV_main_window.title(self.VWV_title)

        # this is used to render as mucking around with tk's internal grid or pack system is like sticking your dick in a fire ant nest
        self.VWV_render_window_screen = tk.Canvas(
            self.VIWV_main_window, 
            width = self.VIWV_main_window.winfo_screenwidth(),
            height = self.VIWV_main_window.winfo_screenheight(),
            background = self.CV_background)
        self.VWV_render_window_screen.pack()


    # this can be called when ready to run
    # this is so if i end up implomenting any mutli threding there is no race contiont
    # this will also be usfull for putting the windo into a "standby mode" where the code is still running but there is no window
    def window_run(self):
        # TODO:
        #   alow the user to change what the window starts 
        #   change the window live (maybe if thats posible
        #       may end up kulling and restarting the window but that may be something that would work
        self.VIWV_main_window.state(self.WV_state)
        self.VIWV_main_window.mainloop()

    # retunrs the requested color
    
    def HO_background(self):
        return self.CV_background
    
    def HO_text(self):
        return self.CV_text
    
    def HO_importent(self):
        return self.CV_importent
    
    def HO_selected(self):
        return self.CV_selected
    
    def HO_line(self):
        return self.CV_line
    
    def HO_button(self):
        return self.CV_button
    
    def HO_backer(self):
        return self.CV_backer

class scrolling_calinder(object):
    """docstring for scrolling_calinder

runs with an offset using an older project from v2 alowing things to scroll
this should be really nice instead of just jumping betwean months it can nicly scroll

as of yet unsure how this will work but should be intresting

when transerfering dates:
 -- MUST BE: -- 
    [DAY:MONTH:YEAR]
in or out that is the format to use for dates to avoiod having to brake down fuctions
if if one of them is not given or is not output then fill with: -1
this is to fill list spot to keep the values correct but will not error out
#####
[DAY:MONTH:YEAR] -1
#####

Keys:
    CV = Color Variable
    HO = Hand Out
    UIV = User Interface Variable 
    ICV = Internal Calendar Variable
    WV = Window Variable
    VWV = Vital Window Variable
    VIWV = Vital Interal Window Variable 
    """

    def __init__(self, arg):
        self.arg
        



class scroll_handler(object):
    """docstring for scroll_handler
an adaption of the scrolling-buttons project that was made for showing the events in v2

upgrading to a class to more easly alow more that one scroll to be working

########
this has no use for TK or events, this is just a number cruncher and alows for more wide spread code usage
########


if i rember correctly (im not going to go checking as my doc for that is just none)
i used a dict and then "scroll id's" for each diffrant scroller
this worked for sure but was intresting to work with and was a pain to implement without alot setting up

for this i am going to be using a simler ish stuctuer but with a more cut down version that will just be a simple call and responce
with less post call prosessing


########
this will take a dict so that it can be changed more easly and adably

settings = {
    "speed": 0,
    "offset": 0,
    "scrolling_depth": 3,
    "max_upper_scroll_limit": 0 # this is 
    "speed_reduction": 0.3,
    "running": [False, False],
    "tick_speed": 25

}
########
"""
    def __init__(self, arg):
        super(scroll_handler, self).__init__()
        self.
        

todays_date = [datetime.now().day, datetime.now().month, datetime.now().year]
window = calendar_window_data(todays_date, "calendar", "dark_mode")

window.Window_ingage()
window.window_run()