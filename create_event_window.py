import calendar, time, os, json, requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import colorchooser, messagebox, font
from pynput import mouse, keyboard

import cal_v2_line_save
def render_create_event_window(when, yearly_events_today, render_window_canvas, calendar_window, color_dict, color_mode, global_render_object_dict):
    # 'render_window_canvas', 'creating_event_window_objects', and 'global_render_object_dict'
    
    global creating_event_window_objects
    creating_event_window_objects = []
    # gets the right size for the window
    event_window_coords = [
        calendar_window.winfo_width()/2-(calendar_window.winfo_width()/4), 
        calendar_window.winfo_height()/2-(calendar_window.winfo_width()/8), 
        calendar_window.winfo_width()/2+(calendar_window.winfo_width()/4), 
        calendar_window.winfo_height()/2+(calendar_window.winfo_width()/8), 
    ]
    # there has to be a better way to set this up than declearing each one by hand ;-
    # renders the background for the window

    title_box = render_window_canvas.create_polygon(
        event_window_coords[0],
        event_window_coords[1],

        calendar_window.winfo_width()/2-20,
        event_window_coords[0],

        event_window_coords[2],
        calendar_window.winfo_width()/2-20,

        event_window_coords[2],
        event_window_coords[3],
        outline="pink"
    )

    create_event_window_box = render_window_canvas.create_rectangle(
        event_window_coords[0],
        event_window_coords[1],
        event_window_coords[2],
        event_window_coords[3],
        outline=color_dict[color_mode]["line_color"],
        fill=color_dict[color_mode]["backer_color"]
    )
    creating_event_window_objects.append(create_event_window_box)
    # creates a bigger pad for the user to click on
    X_backer = render_window_canvas.create_rectangle(
        event_window_coords[2]-1,
        event_window_coords[1]+1,
        event_window_coords[2]-30,
        event_window_coords[1]+30,
        outline=color_dict[color_mode]["backer_color"],
        fill=color_dict[color_mode]["backer_color"]
    )
    creating_event_window_objects.append(X_backer)

    # creats the 2 dignal lines for the X
    line1_corss = render_window_canvas.create_line(event_window_coords[2]-10,event_window_coords[1]+10,event_window_coords[2]-20,event_window_coords[1]+20,width=2, fill="red")
    creating_event_window_objects.append(line1_corss)
    line2_corss = render_window_canvas.create_line((event_window_coords[2]-10),(event_window_coords[1]-10)+30,(event_window_coords[2]-20),(event_window_coords[1]-20)+30,width=2, fill="red")
    creating_event_window_objects.append(line2_corss)

    # sets the title for the create event window
    day_title_text = f"{when[0]} {when[1]} {when[2]} {yearly_events_today}"
    day_title = render_window_canvas.create_text(
        calendar_window.winfo_width()/2,
        event_window_coords[1]+20, 
        text=day_title_text, 
        font=("Arial", 12), 
        fill=color_dict[color_mode]["text_color"][1], 
        anchor="center"
    )
    creating_event_window_objects.append(day_title)


    # todays events box
    events_today_box = render_window_canvas.create_rectangle(
        event_window_coords[0],
        event_window_coords[1],
        event_window_coords[0]+((calendar_window.winfo_width()/15)*2),
        event_window_coords[3],
        outline=color_dict[color_mode]["line_color"],
        fill= color_dict[color_mode]["backer_color"]
    )
    creating_event_window_objects.append(events_today_box)

    # todays events title
    todays_events_title_text = render_window_canvas.create_text(
        event_window_coords[0]+(calendar_window.winfo_width()/15),
        event_window_coords[1]+20, 
        text="events today", 
        font=("Arial", 25), 
        fill=color_dict[color_mode]["text_color"][1], 
        anchor="center"
    )
    creating_event_window_objects.append(todays_events_title_text)


    create_event_button = render_window_canvas.create_rectangle(
        calendar_window.winfo_width()/2-200,
        event_window_coords[1]+2, 
        calendar_window.winfo_width()/2-50,
        event_window_coords[1]+38, 
        outline=color_dict[color_mode]["line_color"]
    )

    creating_event_window_objects.append(create_event_button)
    global_render_object_dict["create_event_window"] = creating_event_window_objects


    booked_events = cal_v2_line_save.read_events(when[2], when[1], when[0])
    if booked_events != 404:
        for i in range(len(booked_events)):

            booked_event_backer = render_window_canvas.create_rectangle(
                (event_window_coords[0]+(calendar_window.winfo_width()/15))+120,
                ((event_window_coords[1]+20)+50*(i+1))+22,
                (event_window_coords[0]+(calendar_window.winfo_width()/15))-120,
                ((event_window_coords[1]+20)+50*(i+1))-22,
                outline=color_dict[color_mode]["backer_color"],
                fill=color_dict[color_mode]["backer_color"]
            )

            creating_event_window_objects.append(booked_event_backer)
            tag = str(booked_events[i]["looks"])+str(i)+"bacler"
            render_window_canvas.addtag_withtag(tag, booked_event_backer)   
            render_window_canvas.tag_bind(tag, "<Button-1>", 
                lambda event, booking=booked_events[i], cw=calendar_window, rw=render_window_canvas, gr=global_render_object_dict:  
                clicked_event(event, booking, cw, rw, gr)
            )


            booked_event = render_window_canvas.create_text(
                event_window_coords[0]+(calendar_window.winfo_width()/15),
                (event_window_coords[1]+20)+50*(i+1), 
                text=booked_events[i]["looks"][0], 
                font=("Arial", 12), 
                fill=booked_events[i]["looks"][1], 
                anchor="center"
            )

            booked_events[i]["render_point"] = [event_window_coords[0]+(calendar_window.winfo_width()/15), (event_window_coords[1]+20)+50*(i+1)]
            tag = str(booked_events[i]["looks"])+str(i)
            render_window_canvas.addtag_withtag(tag, booked_event)   
            render_window_canvas.tag_bind(tag, "<Button-1>", 
                lambda event, booking=booked_events[i], cw=calendar_window, rw=render_window_canvas, gr=global_render_object_dict:  
                clicked_event(event, booking, cw, rw, gr)
            )

            creating_event_window_objects.append(booked_event)




    render_window_canvas.addtag_withtag("line1", line1_corss)   
    render_window_canvas.tag_bind("line1", "<Button-1>", 
        lambda event, WOR=[render_window_canvas, creating_event_window_objects, global_render_object_dict]: 
        close_create_event(event, WOR)
    )

    render_window_canvas.addtag_withtag("line2", line2_corss)
    render_window_canvas.tag_bind("line2", "<Button-1>", 
        lambda event, WOR=[render_window_canvas, creating_event_window_objects, global_render_object_dict]: 
        close_create_event(event, WOR)
    )

    render_window_canvas.addtag_withtag("backer", X_backer)
    render_window_canvas.tag_bind("backer", "<Button-1>", 
        lambda event, WOR=[render_window_canvas, creating_event_window_objects, global_render_object_dict]: 
        close_create_event(event, WOR)
    )


    # return True

def clicked_event(event, booking, calendar_window, render_window_canvas, global_render_object_dict):
    global clicked_event_deets_disp
    for i in range(len(clicked_event_deets_disp)):
        render_window_canvas.delete(clicked_event_deets_disp[i])

    clicked_event_deets_disp = []

    booking_info_XY = [
        calendar_window.winfo_width()/2-(calendar_window.winfo_width()/4)+((calendar_window.winfo_width()/15)*2), 
        calendar_window.winfo_height()/2-(calendar_window.winfo_width()/8), 
        calendar_window.winfo_width()/2+(calendar_window.winfo_width()/4), 
        calendar_window.winfo_height()/2+(calendar_window.winfo_width()/8), 
    ]

    create_event_window = render_window_canvas.create_rectangle(
        booking["render_point"][0]+120,
        booking["render_point"][1]+22,
        booking["render_point"][0]-120,
        booking["render_point"][1]-22,
        outline=booking["looks"][1]
    )
    clicked_event_deets_disp.append(create_event_window)


    booking_title = render_window_canvas.create_text(
        booking["render_point"][0]+140,
        booking_info_XY[1]+50, 
        text=cal_v2_line_save.text_formatter(booking["info"][0], 25),
        font=("Arial", 12), 
        fill=booking["looks"][1], 
        anchor="nw"
    )
    creating_event_window_objects.append(booking_title)
    clicked_event_deets_disp.append(booking_title)
    global_render_object_dict["showed_event"] = clicked_event_deets_disp

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


    booking_start_min = render_window_canvas.create_text(
        booking["render_point"][0]+380,
        booking_info_XY[1]+50, 
        text=f"{booking_hour}:{booking_minute} to {booking_end_hour}:{booking_end_min}",
        font=("Arial", 12), 
        fill=booking["looks"][1], 
        anchor="nw"
    )
    creating_event_window_objects.append(booking_start_min)
    clicked_event_deets_disp.append(booking_start_min)

def close_create_event(event, WOR):
    render_window_canvas, creating_event_window_objects, global_render_object_dict = WOR

    if "create_event_window" in global_render_object_dict:
        for i in range(len(creating_event_window_objects)):
            render_window_canvas.delete(global_render_object_dict["create_event_window"][i])

    if "showed_event" in global_render_object_dict:
        for i in range(len(global_render_object_dict["showed_event"])):
            render_window_canvas.delete(global_render_object_dict["showed_event"][i])

            
global clicked_event_deets_disp
clicked_event_deets_disp = []