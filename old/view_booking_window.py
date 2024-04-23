import calendar, time, os, json, requests, pprint
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import colorchooser, messagebox, font
from pynput import mouse, keyboard

import cal_v2_line_save
global window_settings
window_settings = {}


global color_dict
color_dict ={
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

# will need to add a data management and dead window id cleaning 
def create_new_window_data(id_tag, baked_date, yearly_events_today):
    # creates the new window data 
    new_window_data = {
        "speed": 0, # the speed of the scrolling
        "offset": 0, # the offset for the scroll
        "scrolling_depth": 3, # the the pix that each scroll takes 
        "max_scroll_limits": {"upper": 0, "lowwer": 0}, # upper and lower limits of the scroll bar 
        "speed_reduction": 0.3, # how much resistance the scroll has 
        "running": [False, False], # if the bar is moving witch way
        "tick_speed": 25, # the base time for the scroll bar to update
        "clicked": None, # if any witch event is clicked
        "window_size": { # the window dimensions and spacing for the events
            "width": 240,
            "height": 44,
            "spacing": 70
        },
        "events_of_the_year": yearly_events_today, 
        "events_booked": [], # the events that are booked in
        "render_list":{
            "events_list_renderd": {}, # list everything in the events today list
            "event_info_render_list": {}, # list everything in the info side
            "clicked": None
        }
    }


    # grabs the booking data separately to check 
    bookings_today = cal_v2_line_save.read_events(baked_date)

    # if the day has booked events then it will assign
    if bookings_today != 404 and len(bookings_today) != 0:
        new_window_data["events_booked"] = bookings_today

    # adds the a trigger to the events list that will create an add event button at the end of the events list
    new_window_data["events_booked"].append(102059)

    # dumps the new window data into the global window settings
    window_settings[str(id_tag)] = new_window_data



def run_sim():
    render_booking_view_window([8,1,2024], "", "dark_mode")

def render_booking_view_window(baked_date, yearly_events_today, color_mode):
    # print (baked_date, yearly_events_today, color_mode)
    global sub_window
    sub_window = tk.Tk()
    title = f"{baked_date[0]} {baked_date[1]} {baked_date[2]} {yearly_events_today}"
    sub_window.title(title)
    sub_window.geometry(f"{int(sub_window.winfo_screenwidth()/2)}x{int(sub_window.winfo_screenheight()/2)}")
    subwindow_render_canvas = tk.Canvas(
        sub_window,
        width=sub_window.winfo_screenwidth()/2,
        height=sub_window.winfo_screenheight()/2,
        # highlightthickness=0,
        background=color_dict[color_mode]["main_background_color"]
    )
    subwindow_render_canvas.pack()
    
    create_new_window_data(sub_window, baked_date, yearly_events_today)
    window_settings[str(sub_window)]["offset"] = 0
    window_settings[str(sub_window)]["speed"] = 0

    sub_window.focus_set()
    subwindow_render_canvas.bind("<MouseWheel>", lambda event, baked_date=baked_date, yearly_events_today=yearly_events_today, subwindow_render_canvas=subwindow_render_canvas, sub_window=sub_window, color_mode=color_mode:
        scrolling(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)
    )

    subwindow_render_canvas.bind("<Configure>", lambda event, baked_date=baked_date, yearly_events_today=yearly_events_today, subwindow_render_canvas=subwindow_render_canvas, sub_window=sub_window, color_mode=color_mode:
        resizse_event(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode),
    )
    render_create_event_window("", baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)
    render_events_list("", baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)
    # runner()
    sub_window.focus_set()
    sub_window.mainloop()


def resizse_event(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode):
    render_create_event_window(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)
    render_events_list(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)

def render_create_event_window(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode):

    global creating_event_window_objects

    creating_event_window_objects = []


    events_today_box = subwindow_render_canvas.create_rectangle(
        0,0,
        20+((subwindow_render_canvas.winfo_reqwidth()/(15/2))*2),
        subwindow_render_canvas.winfo_reqheight(),
        outline=color_dict[color_mode]["line_color"]
        # fill= color_dict[color_mode]["backer_color"]
    )

    if str(sub_window)+"view_booking_window" in window_settings[str(sub_window)]:
        for i in range(len(local_render_object_dict[str(sub_window)+"view_booking_window"])):
            subwindow_render_canvas.delete(local_render_object_dict[str(sub_window)+"view_booking_window"][i])

    booked_events = cal_v2_line_save.read_events(baked_date)
    if type(booked_events) != int and int(subwindow_render_canvas.winfo_reqheight()/70) < len(booked_events)+1:
            window_settings[str(sub_window)]["max_scroll_limits"]["upper"] = abs(70*((len(booked_events)-int(subwindow_render_canvas.winfo_reqheight()/70))+1)-subwindow_render_canvas.winfo_reqheight())
            window_settings[str(sub_window)]["scrolling"] = True
    else:
        window_settings[str(sub_window)]["scrolling"] = False

# deleates and unbinds them from the mouse button 
def remove_rendered(target_list, sub_list):
    if sub_list in target_list:
        for i in range(len(target_list[sub_list])):
            subwindow_render_canvas.delete(target_list[sub_list][i])

# def render_event_buttons(subwindow_render_canvas, color_mode):
# rendering the list of events in the day
def render_events_list(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode):
    
    remove_rendered(window_settings[str(sub_window)]["render_list"], "events_list_renderd")

    # todays events title
    global save_me_list
    save_me_list = [event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode]

    booked_events = window_settings[str(sub_window)]["events_booked"]

    # this needs to be more robost as it keeps falling and not 
    global event_number
    event_number = 0
    event_render_list = []
    event_number = len(booked_events)
    for i in range(len(booked_events)):
        target_event = booked_events[i]

        if target_event not in [404, 102059] :
            frame_info = [
                10+(subwindow_render_canvas.winfo_reqwidth()/(15/2))+120,
                70*(i+1)+22 + window_settings[str(sub_window)]["offset"],
                10+(subwindow_render_canvas.winfo_reqwidth()/(15/2))-120,
                70*(i+1)-22 + window_settings[str(sub_window)]["offset"]
            ]

            booked_event_backer = subwindow_render_canvas.create_rectangle(
                frame_info,
                outline=color_dict[color_mode]["backer_color"],
                fill=color_dict[color_mode]["backer_color"]
            )
            event_render_list.append(booked_event_backer)

            tag1 = str(target_event["looks"])+str(i)+"backer"
            subwindow_render_canvas.addtag_withtag(tag1, booked_event_backer)   
            subwindow_render_canvas.tag_bind(tag1, "<Button-1>", 
                lambda event, pas=[target_event, sub_window, subwindow_render_canvas, color_mode, i, baked_date, frame_info]:  
                clicked_event(event, pas)
            )


            booked_event = subwindow_render_canvas.create_text(
                10+subwindow_render_canvas.winfo_reqwidth()/(15/2),
                70*(i+1) + window_settings[str(sub_window)]["offset"], 
                text=target_event["looks"][0], 
                font=("Arial", 12), 
                fill=target_event["looks"][1], 
                anchor="center"
            )  
            event_render_list.append(booked_event)


            target_event["render_point"] = [
                10+subwindow_render_canvas.winfo_reqwidth()/(15/2), 
                70*(i+1) + window_settings[str(sub_window)]["offset"]
            ]

            tag2 = str(target_event["looks"])+str(i)
            subwindow_render_canvas.addtag_withtag(tag2, booked_event)   
            subwindow_render_canvas.tag_bind(tag2, "<Button-1>", 
                lambda event, pas=[target_event, sub_window, subwindow_render_canvas, color_mode, i, baked_date, frame_info]:  
                clicked_event(event, pas)
            )

            if target_event == window_settings[str(sub_window)]["clicked"]:
                booking_high = subwindow_render_canvas.create_rectangle(
                    frame_info,
                    outline=target_event["looks"][1]
                )

                event_render_list.append(booking_high)
                local_render_object_dict[str(sub_window)+"clicked"] = booking_high

        # adds the create even button to the end of the events list
        else:  
            frame_info = [
                10+(subwindow_render_canvas.winfo_reqwidth()/(15/2))+120,
                70*(i+1)+22 + window_settings[str(sub_window)]["offset"],
                10+(subwindow_render_canvas.winfo_reqwidth()/(15/2))-120,
                70*(i+1)-22 + window_settings[str(sub_window)]["offset"]
            ]

            booked_event_backer = subwindow_render_canvas.create_rectangle(
                frame_info,
                outline="pink", #color_dict[color_mode]["backer_color"],
                fill="pink" #color_dict[color_mode]["backer_color"]
            )
            event_render_list.append(booked_event_backer)

            tag1 = "lol"+str(i)+"backer"
            subwindow_render_canvas.addtag_withtag(tag1, booked_event_backer)   
            subwindow_render_canvas.tag_bind(tag1, "<Button-1>", 
                lambda event, CL = sub_window, date=baked_date: 
                create_event_event_window(event, CL, date)
            )

            booked_event = subwindow_render_canvas.create_text(
                10+subwindow_render_canvas.winfo_reqwidth()/(15/2),
                70*(i+1) + window_settings[str(sub_window)]["offset"], 
                text="lol", #target_event["looks"][0], 
                font=("Arial", 12), 
                fill="pink", #target_event["looks"][1], 
                anchor="center"
            )  
            event_render_list.append(booked_event)


            tag2 = str("target_event[]")+str(i)
            subwindow_render_canvas.addtag_withtag(tag2, booked_event)   
            subwindow_render_canvas.tag_bind(tag2, "<Button-1>", 
                lambda event, CL = sub_window, date=baked_date: 
                create_event_event_window(event, CL, date)
            )




            if target_event == window_settings[str(sub_window)]["clicked"]:
                booking_high = subwindow_render_canvas.create_rectangle(
                    frame_info,
                    outline=target_event["looks"][1]
                )

                event_render_list.append(booking_high)





    title_cover_plate = subwindow_render_canvas.create_rectangle(
        0, 0,
        20+((subwindow_render_canvas.winfo_reqwidth()/(15/2))*2)-1, 45,
        outline=color_dict[color_mode]["main_background_color"],
        fill=color_dict[color_mode]["main_background_color"]
    )
    todays_events_title_text = subwindow_render_canvas.create_text(
        10+(subwindow_render_canvas.winfo_reqwidth()/(15/2)),
        20, 
        text="events today", 
        font=("Arial", 25), 
        fill=color_dict[color_mode]["text_color"][1], 
        anchor="center"
    )
    event_render_list.append(todays_events_title_text)



    window_settings[str(sub_window)]["events_list_render"] = event_render_list


def clicked_event(event, pas):
    pprint.pprint (window_settings)

    booking, sub_window, subwindow_render_canvas, color_mode, pos, baked_date, frame_info = pas
    global clicked_event_deets_disp
    clicked_event_deets_disp = []
    
    # # this is for the highlighting the event that has been clicked and allowing the highlight to scroll with the events list 


    if window_settings[str(sub_window)]["render_list"]["clicked"] == pos:
        window_settings[str(sub_window)]["render_list"]["clicked"] = None
    else:
        window_settings[str(sub_window)]["render_list"]["clicked"] = pos


    booking_colord_border = subwindow_render_canvas.create_rectangle(
        frame_info,
        outline=booking["looks"][1]
    )
    window_settings[str(sub_window)]["render_list"]["events_list_renderd"] = (booking_colord_border)
    window_settings[str(sub_window)]["render_list"]["clicked"] = booking_colord_border




    booking_info_XY = [
        (subwindow_render_canvas.winfo_reqwidth()/4)+((subwindow_render_canvas.winfo_reqwidth()/15)*2), 
        (subwindow_render_canvas.winfo_reqwidth()/8), 
        (subwindow_render_canvas.winfo_reqwidth()/4), 
        (subwindow_render_canvas.winfo_reqwidth()/8), 
    ]

    delete_event_button = subwindow_render_canvas.create_rectangle(
        20+((subwindow_render_canvas.winfo_reqwidth()/(15/2))*2)+25, 
        10,
        20+((subwindow_render_canvas.winfo_reqwidth()/(15/2))*2)+125, 
        30,
        outline=color_dict[color_mode]["line_color"],
        fill=color_dict[color_mode]["backer_color"]
    )
    creating_event_window_objects.append(delete_event_button) 

    delete_event_bttn_text = subwindow_render_canvas.create_text(
        20+((subwindow_render_canvas.winfo_reqwidth()/(15/2))*2)+25+(125/2),
        20,
        text="delete event",
        font=("Arial", 12),
        fill=color_dict[color_mode]["text_color"][1],
        anchor="center"
    )
    creating_event_window_objects.append(delete_event_bttn_text)
    
    tag = "del"
    subwindow_render_canvas.addtag_withtag(tag, delete_event_button)   
    subwindow_render_canvas.tag_bind(tag, "<Button-1>", 
        lambda event, pas=[pos, baked_date, sub_window]:  
        delete_sected_event(event, pas)
    )

    tag = "de1"
    subwindow_render_canvas.addtag_withtag(tag, delete_event_bttn_text)   
    subwindow_render_canvas.tag_bind(tag, "<Button-1>", 
        lambda event, pas=[pos, baked_date, sub_window]:  
        delete_sected_event(event, pas)
    )




    booking_info = subwindow_render_canvas.create_text(
        40+((subwindow_render_canvas.winfo_reqwidth()/(15/2))*2),
        50, 
        text=cal_v2_line_save.text_formatter(booking["info"][0], 120),
        font=("Arial", 12), 
        fill=booking["looks"][1], 
        anchor="nw"
    )
    clicked_event_deets_disp.append(booking_info)

    booking_hour = booking["time"][0]
    if len(str(booking_hour)) == 1:
        booking_hour = f"0{booking_hour}"

    booking_minute = booking["time"][1]
    if len(str(booking_minute)) == 1:
        booking_minute = f"0{booking_minute}"

    booking_end_hour = booking["time"][2]
    if len(str(booking_end_hour)) == 1:
        booking_end_hour = f"0{booking_end_hour}"

    booking_end_min = booking["time"][3]
    if len(str(booking_end_min)) == 1:
        booking_end_min = f"0{booking_end_min}"


    booking_time = subwindow_render_canvas.create_text(
        (subwindow_render_canvas.winfo_reqwidth()/8)*7,
        50, 
        text=f"{booking_hour}:{booking_minute} to {booking_end_hour}:{booking_end_min}",
        font=("Arial", 12), 
        fill=booking["looks"][1], 
        anchor="nw"
    )
    clicked_event_deets_disp.append(booking_time)
    remove_rendered(window_settings[str(sub_window)]["render_list"], "show_event")
    # if str(sub_window)+"show_event" in local_render_object_dict:
    #     for i in range(len(local_render_object_dict[str(sub_window)+"show_event"])):
    #         subwindow_render_canvas.delete(local_render_object_dict[str(sub_window)+"show_event"][i])

    window_settings[str(sub_window)]["render_list"]["show_event"] = clicked_event_deets_disp
                               # event, baked_date, yearly_events_today,                                    subwindow_render_canvas, sub_window, color_mode
    render_create_event_window(event, baked_date, window_settings[str(sub_window)]["events_of_the_year"], subwindow_render_canvas, sub_window, color_mode)

def delete_sected_event(event, pas):
    # pas 1 is the position on the list, and 2 is the baked_date
    events_listed = cal_v2_line_save.read_events(pas[1])
    event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode = save_me_list
    
    result = messagebox.askquestion("Confirmation", f"do you want to delete {events_listed[pas[0]]['looks'][0]}")
    if result == "yes":
        events_listed.pop(pas[0])
        cal_v2_line_save.save_events(events_listed, {"date": [pas[1][2], pas[1][1], pas[1][0]], "mode": "mass", "kick_code": 5504})
        render_events_list(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)
    elif result == "no":
        pass

    else:
        print (f"unser how got here: {result}")

    sub_window.focus_set()

global clicked_event_deets_disp
clicked_event_deets_disp = []


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# this is for scroling up and down with custom rasistance so it fels nice                   #
# needs a masive rework and to not be file dependant and instead just spits out an offset   #
# baked_date run will keep running till the speed or an offset limit is reached             #
# also changes the rendering for the events list for this (split it)                        #
# so that it only needs to keep rendering the evens and dosnt need render the window again  #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def neg(num):
    if max(num, 0) == 0:
        return num
    return int("-"+str(num))

def scrolling(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode):
    if window_settings[str(sub_window)]["scrolling"] == False:
        # print ("scroll kick: no scrolling len")
        return

    window_settings[str(sub_window)]["max_scroll_limits"]["upper"] = neg((window_settings[str(sub_window)]["window_size"]["spacing"]*event_number)-sub_window.winfo_height()+window_settings[str(sub_window)]["window_size"]["spacing"])
    # print (event.delta)
    if event.delta > 0: # and window_settings[str(sub_window)]["running"][1] != True:
        window_settings[str(sub_window)]["speed"] -= window_settings[str(sub_window)]["scrolling_depth"]
        # print ("scroll_up")
        scrolling_funk(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)

    if event.delta < 0: # and window_settings[str(sub_window)]["running"][0] != True:
        window_settings[str(sub_window)]["speed"] += window_settings[str(sub_window)]["scrolling_depth"]
        # print ("scroll_down")
        scrolling_funk(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)



def scrolling_funk(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode):
    # print ("scrilling,", window_settings[str(sub_window)])
    if int(window_settings[str(sub_window)]["speed"]) != 0:

        if window_settings[str(sub_window)]["offset"] - window_settings[str(sub_window)]["speed"] < window_settings[str(sub_window)]["max_scroll_limits"]["upper"]:
            window_settings[str(sub_window)]["speed"] = 0
            # print (f"scroll kicked: ofset will exseed given scroll limit of :{window_settings[str(sub_window)]['max_scroll_limits']['upper']} with :{window_settings[str(sub_window)]['offset'] + window_settings[str(sub_window)]['speed']} || ID: 2044568")
            # window_settings[str(sub_window)]["offset"] = window_settings[str(sub_window)]["max_scroll_limits"]["upper"]+1
            return

        if window_settings[str(sub_window)]["offset"] - window_settings[str(sub_window)]["speed"] > window_settings[str(sub_window)]["max_scroll_limits"]["lowwer"]:
            window_settings[str(sub_window)]["speed"] = 0
            # print (f"scroll kicked: ofset will exseed given scroll limit of :{window_settings[str(sub_window)]['max_scroll_limits']['lowwer']} with :{window_settings[str(sub_window)]['offset'] + window_settings[str(sub_window)]['speed']} || ID: 2044568")
            # window_settings[str(sub_window)]["offset"] = window_settings[str(sub_window)]["max_scroll_limits"]["lowwer"]-1
            return


        if int(window_settings[str(sub_window)]["speed"]) > 0:
            window_settings[str(sub_window)]["offset"] -= int(window_settings[str(sub_window)]["speed"])
            window_settings[str(sub_window)]["speed"] -= window_settings[str(sub_window)]["speed_reduction"]/4

        if int(window_settings[str(sub_window)]["speed"]) < 0:
            window_settings[str(sub_window)]["offset"] -= int(window_settings[str(sub_window)]["speed"])
            window_settings[str(sub_window)]["speed"] += window_settings[str(sub_window)]["speed_reduction"]/4

        render_events_list(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)

        sub_window.after(25, lambda event="", baked_date=baked_date, yearly_events_today=yearly_events_today, subwindow_render_canvas=subwindow_render_canvas, sub_window=sub_window, color_mode=color_mode:
            scrolling_funk(event, baked_date, yearly_events_today, subwindow_render_canvas, sub_window, color_mode)
        )


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# for creating events and handling the new event window               #
# also handals displaying even data after the event has been click on #
# and event editing (to be added)                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def create_event_event_window(event, sub_window, baked_date):
    global event_input_frame
    global event_date_selecter
    sub_window = tk.Toplevel(sub_window)
    sub_window.title("Create Event")

    event_input_frame = ttk.Frame(sub_window)
    event_input_frame.pack(side="right")
    event_date_selecter = ttk.Frame(event_input_frame)
    event_date_selecter.pack(side="top")


    create_date_widgets(baked_date[2], baked_date[1], baked_date[0], [0], "", sub_window)

def create_date_widgets(year_clciked, month_clciked, day_clicked, event_viewing, run_mode, sub_window):
    global color_entry, info_input_entery, color_label, color_hold
    global year_var, month_var, day_var, start_hour_var, end_hour_var, start_minute_var, end_minute_var, choose_color_button
    global date_label, day_combobox, event_name_entery
    global year_combobox, month_combobox, day_combobox, hour_end_Comb, hour_start_Comb, minute_start_Comb, minute_end_Comb 
    color_hold = None
    years = []
    
    for year in range(2020, 2030):
        years.append(str(year))



    year_var = tk.StringVar()
    year_combobox = ttk.Combobox(event_date_selecter, textvariable=year_var, values=years, width=5)
    year_combobox.grid(row=0, column=0)
    year_combobox.set(year_clciked) 

    months = [str(month) for month in range(-1, 14)]
    month_var = tk.StringVar()
    month_combobox = ttk.Combobox(event_date_selecter, textvariable=month_var, values=months, width=5)
    month_combobox.grid(row=0, column=1)
    month_combobox.set(month_clciked) 

    day_var = tk.StringVar()
    day_combobox = ttk.Combobox(event_date_selecter, textvariable=day_var, width=5)
    day_combobox.grid(row=0, column=2)

    day_combobox.set(day_clicked)

    start_hours = [str(hour) for hour in range(-1, 25)]
    start_hour_var = tk.StringVar()

    hour_start_Comb = ttk.Combobox(event_date_selecter, textvariable=start_hour_var, values=start_hours, width=5)
    hour_start_Comb.grid(row=0, column=3)

    start_minutes = [str(minute)for minute in range(-1, 61)]
    start_minute_var = tk.StringVar()
    minute_start_Comb = ttk.Combobox(event_date_selecter, textvariable=start_minute_var, values=start_minutes, width=5)
    minute_start_Comb.grid(row=0, column=4)

    end_hours = [str(hour) for hour in range(-1, 25)]
    end_hour_var = tk.StringVar()
    hour_end_Comb = ttk.Combobox(event_date_selecter, textvariable=end_hour_var, values=end_hours, width=5)
    hour_end_Comb.grid(row=1, column=3)

    end_minutes = [str(minute)for minute in range(-1, 61)]
    end_minute_var = tk.StringVar()
    minute_end_Comb = ttk.Combobox(event_date_selecter, textvariable=end_minute_var, values=end_minutes, width=5)
    minute_end_Comb.grid(row=1, column=4)

    if run_mode == "reading":
        update_date_button = tk.Button(event_input_frame, text="update event", command= lambda: update_event(event_viewing))
        update_date_button.pack()
        hour_start_Comb.set(event_viewing["time"][0]) 
        minute_start_Comb.set(event_viewing["time"][1]) 
        hour_end_Comb.set(event_viewing["time"][2]) 
        minute_end_Comb.set(event_viewing["time"][3]) 

    else:
        update_date_button = tk.Button(event_input_frame, text="add event", command=create_event_main)
        update_date_button.pack()




    choose_color_button = tk.Button(event_input_frame, text="Choose Color", command=lambda: color_selecter(sub_window))
    choose_color_button.pack()


    color_label = tk.Label(event_input_frame, text="Selected Color", width=30, height=3, relief=tk.SOLID)
    color_label.pack()

    event_name_entery = tk.Entry(event_input_frame)
    event_name_entery.pack()

    info_input_entery = tk.Text(event_input_frame, height=5, width=40)
    # info_input_entery.configure(font=("Arial", 12, "italic"), fg="blue")
    info_input_entery.pack()

    if run_mode == "reading":
        event_name_entery.insert(0, event_viewing["looks"][0])
        info_input_entery.insert(tk.END, event_viewing["info"][0])
        color_label.config(bg=event_viewing["looks"][1])

    update_datedays()
    dateselcter_month_display("")
    event_day_selecter("")
    event_start_hour_selecter("")
    event_start_minute_selecter("")
    event_end_hour_selecter("")
    event_end_minute_selecter("")
    day_combobox.set(day_clicked)

    year_combobox.bind("<<ComboboxSelected>>", update_datedays)
    month_combobox.bind("<<ComboboxSelected>>", dateselcter_month_display)
    day_combobox.bind("<<ComboboxSelected>>", event_day_selecter)
    hour_start_Comb.bind("<<ComboboxSelected>>", event_start_hour_selecter)
    minute_start_Comb.bind("<<ComboboxSelected>>", event_start_minute_selecter)
    hour_end_Comb.bind("<<ComboboxSelected>>", event_end_hour_selecter)
    minute_end_Comb.bind("<<ComboboxSelected>>", event_end_minute_selecter)


def show_event_details(event_data):
    global event_input_frame
    global event_date_selecter
    sub_window = tk.Toplevel(window)
    sub_window.title("Event Editer")

    event_input_frame = ttk.Frame(sub_window)
    event_input_frame.pack(side="right")
    event_date_selecter = ttk.Frame(event_input_frame)
    event_date_selecter.pack(side="top")
    sub_window.lift()
    create_date_widgets(event_data["date"][0], event_data["date"][1], event_data["date"][2], event_data, "reading", sub_window)

    sub_window.destroy()

def color_selecter(sub_window):
    global color_label
    global color_hold

    color_hold = colorchooser.askcolor(title="Select a color")[1]
    color_label.config(bg=color_hold)
    if color_hold == None:
        color_hold = "orange"

    sub_window.lift()

def dateselcter_month_display(event):
    global month_var
    if int(month_var.get()) == 13:
        month_combobox.set(1)

    if int(month_var.get()) == 0:
        month_combobox.set(12)
    update_datedays()

def event_day_selecter(event):
    global day_var
    if int(day_combobox['values'].index(day_var.get()))+1 == len(day_combobox['values']):
        day_combobox.set(1)

    if int(day_combobox['values'].index(day_var.get())) == 0:
        day_combobox.set(len(day_combobox['values'])-2)

def event_start_hour_selecter(event):
    global start_hour_var

    try:
        int(start_hour_var.get())
    except:
        hour_start_Comb.set(0)

    if int(start_hour_var.get()) == 24:
        hour_start_Comb.set(0)
    if int(start_hour_var.get()) == -1:
        hour_start_Comb.set(23)

    event_end_hour_selecter(event)

def event_start_minute_selecter(event):
    global start_minute_var
    if int(start_minute_var.get()) == -1:
        minute_start_Comb.set(59)
    if int(start_minute_var.get()) == 60:
        minute_start_Comb.set(0)
    event_end_hour_selecter(event)

def event_end_hour_selecter(event):
    global end_hour_var
    global start_hour_var
    global start_minute_var
    global time_ahead
    try:
        int(end_hour_var.get())
    except:
        hour_end_Comb.set(0)

    try:
        int(end_minute_var.get())
    except:
        end_minute_var.set(0)

    try:
        int(start_minute_var.get())
    except:
        start_minute_var.set(0)


    if int(end_hour_var.get()) == 24:
        hour_end_Comb.set(int(start_hour_var.get()))
    if int(end_hour_var.get()) < int(start_hour_var.get()):
        hour_end_Comb.set(23)

    end_time = (int(hour_end_Comb.get()) * 60) + int(end_minute_var.get())
    start_time = (int(start_hour_var.get()) * 60 ) + int(start_minute_var.get())
    event_end_minute_selecter(event)

def event_end_minute_selecter(event):
    global hour_end_Comb
    global start_hour_var
    global start_minute_var
    global time_ahead
    global end_minute_var
    global time_ahead
    
    end_time = (int(hour_end_Comb.get()) * 60) + int(end_minute_var.get())
    start_time = (int(start_hour_var.get()) * 60 ) + int(start_minute_var.get())
    if end_time-start_time < 15:

        if int(end_minute_var.get()) > 59:

            minute_end_Comb.set(int(start_minute_var.get())+15)
            if int(end_minute_var.get()) > 59:
                minute_end_Comb.set(0)
                hour_end_Comb.set(int(end_hour_var.get())+1)



        if int(end_minute_var.get()) < int(start_minute_var.get())+15:
            minute_end_Comb.set(59)
            if int(end_minute_var.get()) < 59:
                minute_end_Comb.set(0)
                hour_end_Comb.set(int(end_hour_var.get())+1)

    if end_time-start_time > 15:
        if int(end_minute_var.get()) > 59:
            minute_end_Comb.set(0)
            event_end_hour_selecter(event)
        if int(end_minute_var.get()) < 0:
            minute_end_Comb.set(59)


def update_datedays(*args):
    global day_combobox
    selected_year = int(year_var.get())
    selected_month = int(month_var.get())

    if selected_month == 12:
        days_in_month = (datetime(selected_year + 1, 1, 1) - datetime(selected_year, 12, 1)).days
    else:
        days_in_month = (datetime(selected_year, selected_month + 1, 1) - datetime(selected_year, selected_month, 1)).days

    days = [str(day) for day in range(0, days_in_month + 2)]
    day_combobox['values'] = days
    day_combobox.set(1)  # Set default to the first day


def create_event_main():
    global color_label
    selected_year = year_var.get()
    selected_month = month_var.get()
    selected_day = day_var.get()
    start_hour = start_hour_var.get()
    start_minute = start_minute_var.get()
    end_hour = end_hour_var.get()
    end_minute = end_minute_var.get()
    event_name = event_name_entery.get()
    info_input = info_input_entery.get("1.0", "end-1c")
    if color_label == None:
        color_label == "orange"
        


    event_place_data = ({
        "date": [int(selected_year),
                 int(selected_month),
                 int(selected_day)],
        "time": [int(start_hour), 
                 int(start_minute), 
                 int(end_hour), 
                 int(end_minute)], 
        "looks": [event_name, 
                  str(color_hold)], 
        "tags": [500, 600], 
        "info": [info_input], 
        "id": 1231,
        "type": "event"}
    )

    save_check = cal_v2_line_save.save_events(event_place_data, {"mode": "single"})

    # place_event_today(event_place_data, current_day_canvas)
    # full_month_view(current_year, current_month)

# run_sim()