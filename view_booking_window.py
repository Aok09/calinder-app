import calendar, time, os, json, requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import colorchooser, messagebox, font
from pynput import mouse, keyboard

import cal_v2_line_save

def render_booking_view(when, yearly_events_today, render_window_canvas, calendar_window, color_dict, color_mode, global_render_object_dict):
    sub_window = tk.Toplevel(calendar_window)
    sub_window.title(f"{when[0]} {when[1]} {when[2]} {yearly_events_today}")
    sub_window.geometry(f"{int(calendar_window.winfo_screenwidth()/2)}x{int(calendar_window.winfo_screenheight()/2)}")
    
    subwindow_render_canvas = tk.Canvas(
        sub_window,
        width=calendar_window.winfo_screenwidth()/2,
        height=calendar_window.winfo_screenheight()/2,
        # highlightthickness=0,
        background=color_dict[color_mode]["main_background_color"]
    )
    subwindow_render_canvas.pack()

    subwindow_render_canvas.bind("<Configure>", lambda event, when=when, yearly_events_today=yearly_events_today, subwindow_render_canvas=subwindow_render_canvas, sub_window=sub_window, color_dict=color_dict, color_mode=color_mode, global_render_object_dict=global_render_object_dict:
        render_create_event_window(event, when, yearly_events_today, subwindow_render_canvas, sub_window, color_dict, color_mode, global_render_object_dict)
    )
    sub_window.mainloop()

def render_create_event_window(event, when, yearly_events_today, subwindow_render_canvas, sub_window, color_dict, color_mode, global_render_object_dict):

    global creating_event_window_objects
    if "view_booking_window" in global_render_object_dict:
        for i in range(len(global_render_object_dict["view_booking_window"])):
            subwindow_render_canvas.delete(global_render_object_dict["view_booking_window"][i])
    creating_event_window_objects = []
    # gets the right size for the window
    event_window_coords = [
        0, 
        0, 
        sub_window.winfo_width(), 
        sub_window.winfo_height(), 
    ]



    # todays events title
    todays_events_title_text = subwindow_render_canvas.create_text(
        100,
        20, 
        text="events today", 
        font=("Arial", 25), 
        fill=color_dict[color_mode]["text_color"][1], 
        anchor="center"
    )
    creating_event_window_objects.append(todays_events_title_text)

    create_event_button = subwindow_render_canvas.create_rectangle(
        sub_window.winfo_width(), 
        5,
        sub_window.winfo_width()-100, 
        30,
        outline=color_dict[color_mode]["line_color"],
        fill=color_dict[color_mode]["backer_color"]
    )
    creating_event_window_objects.append(create_event_button)

    create_event_button_text = subwindow_render_canvas.create_text(
        sub_window.winfo_width()-50,
        15,
        text="crete event",
        font=("Arial", 12),
        fill=color_dict[color_mode]["text_color"][1],
        anchor="center"
    )
    creating_event_window_objects.append(create_event_button_text)
    

    subwindow_render_canvas.addtag_withtag("event_text", create_event_button_text)   
    subwindow_render_canvas.tag_bind("event_text", "<Button-1>", 
        lambda event, CL = sub_window, date=when: 
        create_event_event_window(event, CL, date)
    )

    subwindow_render_canvas.addtag_withtag("event_btton", create_event_button)   
    subwindow_render_canvas.tag_bind("event_btton", "<Button-1>", 
        lambda event, CL = sub_window, date=when: 
        create_event_event_window(event, CL, date)
    )



    
    booked_events = cal_v2_line_save.read_events(when[2], when[1], when[0])
    if booked_events != 404:
        for i in range(len(booked_events)):

            booked_event_backer = subwindow_render_canvas.create_rectangle(
                10+(sub_window.winfo_width()/(15/2))+120,
                70*(i+1)+22,
                10+(sub_window.winfo_width()/(15/2))-120,
                70*(i+1)-22,
                outline=color_dict[color_mode]["backer_color"],
                fill=color_dict[color_mode]["backer_color"]
            )

            creating_event_window_objects.append(booked_event_backer)
            tag = str(booked_events[i]["looks"])+str(i)+"bacler"
            subwindow_render_canvas.addtag_withtag(tag, booked_event_backer)   
            subwindow_render_canvas.tag_bind(tag, "<Button-1>", 
                lambda event, booking=booked_events[i], cw=sub_window, rw=subwindow_render_canvas, gr=global_render_object_dict:  
                clicked_event(event, booking, cw, rw, gr)
            )


            booked_event = subwindow_render_canvas.create_text(
                10+sub_window.winfo_width()/(15/2),
                70*(i+1), 
                text=booked_events[i]["looks"][0], 
                font=("Arial", 12), 
                fill=booked_events[i]["looks"][1], 
                anchor="center"
            )  


            booked_events[i]["render_point"] = [
                10+sub_window.winfo_width()/(15/2), 
                70*(i+1)
            ]

            tag = str(booked_events[i]["looks"])+str(i)
            subwindow_render_canvas.addtag_withtag(tag, booked_event)   
            subwindow_render_canvas.tag_bind(tag, "<Button-1>", 
                lambda event, booking=booked_events[i], cw=sub_window, rw=subwindow_render_canvas, gr=global_render_object_dict:  
                clicked_event(event, booking, cw, rw, gr)
            )

            creating_event_window_objects.append(booked_event)


    global_render_object_dict["view_booking_window"] = creating_event_window_objects


    # return True

def clicked_event(event, booking, sub_window, subwindow_render_canvas, global_render_object_dict):
    global clicked_event_deets_disp
    for i in range(len(clicked_event_deets_disp)):
        subwindow_render_canvas.delete(clicked_event_deets_disp[i])

    clicked_event_deets_disp = []

    booking_info_XY = [
        (sub_window.winfo_width()/4)+((sub_window.winfo_width()/15)*2), 
        (sub_window.winfo_width()/8), 
        (sub_window.winfo_width()/4), 
        (sub_window.winfo_width()/8), 
    ]


    create_event_window = subwindow_render_canvas.create_rectangle(
        booking["render_point"][0]+120,
        booking["render_point"][1]+22,
        booking["render_point"][0]-120,
        booking["render_point"][1]-22,
        outline=booking["looks"][1]
    )

    clicked_event_deets_disp.append(create_event_window)


    booking_title = subwindow_render_canvas.create_text(
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


    booking_start_min = subwindow_render_canvas.create_text(
        booking["render_point"][0]+380,
        booking_info_XY[1]+50, 
        text=f"{booking_hour}:{booking_minute} to {booking_end_hour}:{booking_end_min}",
        font=("Arial", 12), 
        fill=booking["looks"][1], 
        anchor="nw"
    )
    creating_event_window_objects.append(booking_start_min)
    clicked_event_deets_disp.append(booking_start_min)


global clicked_event_deets_disp
clicked_event_deets_disp = []


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# for creating events and handling the new event window               #
# also handals displaying even data after the event has been click on #
# and event editing (to be added)                                     #
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def create_event_event_window(event, sub_window, when):
    global event_input_frame
    global event_date_selecter
    sub_window = tk.Toplevel(sub_window)
    sub_window.title("Create Event")

    event_input_frame = ttk.Frame(sub_window)
    event_input_frame.pack(side="right")
    event_date_selecter = ttk.Frame(event_input_frame)
    event_date_selecter.pack(side="top")


    create_date_widgets(when[2], when[1], when[0], [0], "", sub_window)

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


    year_combobox.bind("<<ComboboxSelected>>", update_datedays)
    month_combobox.bind("<<ComboboxSelected>>", dateselcter_month_display)
    day_combobox.bind("<<ComboboxSelected>>", event_day_selecter)
    hour_start_Comb.bind("<<ComboboxSelected>>", event_start_hour_selecter)
    minute_start_Comb.bind("<<ComboboxSelected>>", event_start_minute_selecter)
    hour_end_Comb.bind("<<ComboboxSelected>>", event_end_hour_selecter)
    minute_end_Comb.bind("<<ComboboxSelected>>", event_end_minute_selecter)


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
    print (color_label)
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

    cal_v2_line_save.save_events(event_place_data)
    # place_event_today(event_place_data, current_day_canvas)
    # full_month_view(current_year, current_month)