import calendar, time, os, json, requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import colorchooser, messagebox, font
from pynput import mouse, keyboard

import cal_v2_line_save, view_booking_window

# called when the window is resized
def window_update(hold):


    if view_type == "month":
        page_title()
        calendar_day_blocks()


# this is the list of months_list 
def page_title():
    months_list = [f"{calendar.month_name[looking_for_date[0]]} {looking_for_date[1]}"]
        
    page_title_month = render_window_canvas.create_text(
        calendar_window.winfo_width()/2, 
        65, 
        text=f"{calendar.month_name[looking_for_date[0]]} {looking_for_date[1]}", 
        font=("Arial", 100), 
        fill=color_dict[color_mode]["importent"], 
        anchor="center"
    )

    if f"last_render_month" in global_render_object_dict:
        render_window_canvas.delete(global_render_object_dict[f"last_render_month"])

    global_render_object_dict[f"last_render_month"] = page_title_month





        # print (font_size_i, month_name)

# this section is for when the user interacts with something
# handling the list of months_list when scrolling
def month_scroll(event):
    global creating_event
    if creating_event == True:
        return

    if event.y < 5+((calendar_window.winfo_height()/11)-12)*2 and event.x > (calendar_window.winfo_width()/5) and event.x < (calendar_window.winfo_width()/5)*4:
        global looking_for_date
        if event.delta > 0:
            looking_for_date[0] -= 1
            if looking_for_date[0] == 0:
                looking_for_date[0] = 12
                looking_for_date[1] -= 1

        elif event.delta < 0:
            looking_for_date[0] += 1
            if looking_for_date[0] == 13:
                looking_for_date[0] = 1
                looking_for_date[1] += 1

        window_update("")

def window_click(event):
    global creating_event
    if creating_event != True:
        return

    cc = [ 
        calendar_window.winfo_height()/2-(calendar_window.winfo_width()/8)+1, 
        calendar_window.winfo_width()/2+(calendar_window.winfo_width()/4)-1, 
        calendar_window.winfo_height()/2-(calendar_window.winfo_width()/8)+30, 
        calendar_window.winfo_width()/2+(calendar_window.winfo_width()/4)-30, 
    ]
    
    if event.y > cc[0] and event.x < cc[1] and event.y < cc[2] and event.x > cc[3]:
        creating_event = False
        print ("unlocked calendar")


def day_frame_clicked(when, yearly_events_today):
    global creating_event
    if creating_event == True and creating_event != None:
        print ("open create event", creating_event)
        return

    print ("locking create event", creating_event)
    creating_event = True

    view_booking_window.render_create_event_window(
        when, 
        yearly_events_today, 
        render_window_canvas, 
        calendar_window,
        color_dict,
        color_mode,
        global_render_object_dict
    )


# renders all the boxes for the calinder
def calendar_day_blocks():


    global events_of_year
    # gets the events for the year
    # this is called every month cos i am lazy and it works for now

    yearly_events = cal_v2_line_save.get_holidays(looking_for_date, events_of_year)
    # print (public_holidays)


    # creates the calinder matrix and gets it to be the correct lenght to not create errors 
    cal = calendar.monthcalendar(looking_for_date[1], looking_for_date[0])
    while len(cal) < 6:
        cal.append([0]*7)

    # this creates the the width and hight for each day frame of the month
    day_frame = {
        "width": ((calendar_window.winfo_width())/1.2)/7,
        "height": ((calendar_window.winfo_height())/1.3)/6,
        "margin": [
            (((calendar_window.winfo_width())/1.2)/7)/14, 
            ((calendar_window.winfo_height())/1.3/6)/14
        ]
    }
    # creates the start posiostion so that it dosnt have to be recalulated each time
    x_start_position = (calendar_window.winfo_width()/2)-((day_frame["width"]+day_frame["margin"][0])*3.5)
    y_start_position = (((calendar_window.winfo_height()+calendar_window.winfo_width())/2)/20)*2.3
    
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    # there is 7 days in the week
    # i am using 6 weeks instead of 4 becase there is over lap were some start diffrantly so if i render all 6 there is less "funky"
    for week in range(0,6):




        for day in range(0,7):
            # this is for the fade effect 
            fades = []

            # find the top right hand corner of the box
            day_frame_start_xpos = x_start_position + ((day_frame["width"]+day_frame["margin"][0])*day)
            day_frame_start_ypos = y_start_position + ((day_frame["height"]+day_frame["margin"][1])*week)

            if week == 0:
                week_day_name_backer = render_window_canvas.create_rectangle(
                    day_frame_start_xpos-5, 
                    y_start_position-29, 
                    day_frame_start_xpos+day_frame["width"]+5, 
                    (y_start_position)*6, 
                    outline=color_dict[color_mode]["backer_color"],
                    fill=color_dict[color_mode]["backer_color"]
                )

                week_day_name = render_window_canvas.create_text(
                    day_frame_start_xpos+(day_frame["width"]/2),
                    y_start_position-20, 
                    text=days_of_week[day], 
                    font=("Arial", 12), 
                    fill=color_dict[color_mode]["text_color"][1], 
                    anchor="center"
                )

     

            # checks that the day is in the month
            # this is the part that makes the day small or not
            shrink_facter_x = 0
            shrink_facter_y = 0
            if cal[week][day] == 0:
                shrink_facter_x = day_frame["width"]/2.4
                shrink_facter_y = day_frame["height"]/2.4

            day_frames = {
                "x1":int(day_frame_start_xpos) + shrink_facter_x,
                "y1":int(day_frame_start_ypos) + shrink_facter_y,
                "x2":int(day_frame_start_xpos + day_frame["width"]) - shrink_facter_x,
                "y2":int(day_frame_start_ypos + day_frame["height"]) - shrink_facter_y
            }



            day_box_frame = render_window_canvas.create_rectangle(
                day_frames["x1"], 
                day_frames["y1"], 
                day_frames["x2"], 
                day_frames["y2"], 
                outline=color_dict[color_mode]["line_color"],
                fill=color_dict[color_mode]["backer_color"]
            )

            if cal[week][day] != 0:


                day_text = cal[week][day]
                # print (f"{looking_for_date[1]}-{looking_for_date[0]}-{day} {events_of_year}")
                month = looking_for_date[0]
                if len(str(month)) < 2:
                    month = f"0{month}"

                day_temp = cal[week][day]
                if len(str(day_temp)) < 2:
                    day_temp = f"0{day_temp}"

                yearly_events_today = ""
                text_drop = 10
                max_len = 28

                # print (f"{looking_for_date[1]}-{month}-{day_temp}")
                if f"{looking_for_date[1]}-{month}-{day_temp}" in yearly_events:
                    day_text = f"{cal[week][day]} -> {events_of_year[f'{looking_for_date[1]}-{month}-{day_temp}']}"
                    day_text = cal_v2_line_save.line_spliter(day_text, max_len)
                    yearly_events_today = events_of_year[f'{looking_for_date[1]}-{month}-{day_temp}']


                    if len(str(day_text)) > max_len:
                        text_drop = 20 

                day_frame_text = render_window_canvas.create_text(
                    day_frame_start_xpos+(day_frame["width"]/2),
                    day_frame_start_ypos+text_drop, 
                    text=day_text, 
                    font=("Arial", 12), 
                    fill=color_dict[color_mode]["text_color"][1], 
                    anchor="center"
                )

                booked_events = cal_v2_line_save.read_events(looking_for_date[1], looking_for_date[0], cal[week][day])
                if booked_events != 404:
                    for i in range(len(booked_events)):
                        try:
                            booked_event = render_window_canvas.create_text(
                                day_frame_start_xpos+5,
                                day_frame_start_ypos+(text_drop*4)+(30*i), 
                                text=booked_events[i]["looks"][0], 
                                font=("Arial", 12), 
                                fill=booked_events[i]["looks"][1], 
                                anchor="w"
                            )

                        except:
                            booked_event = render_window_canvas.create_text(
                                day_frame_start_xpos+5,
                                day_frame_start_ypos+(text_drop*4)+(30*i), 
                                text=booked_events[i]["looks"][0], 
                                font=("Arial", 12), 
                                fill="pink", 
                                anchor="w"
                            )

                # bining the interactions for all the days 
                day_frame_tag = f"day_frame_{week}_{day}"
                render_window_canvas.addtag_withtag(day_frame_tag, day_box_frame)
                day_name_tag = f"day_frame_{week}_{day}"
                render_window_canvas.addtag_withtag(day_name_tag, day_frame_text)

                # Bind the event with the desired variable using the tag
                render_window_canvas.tag_bind(day_frame_tag, "<Button-1>", 
                    lambda event, d=cal[week][day], m=looking_for_date[0], y=looking_for_date[1], today_event=yearly_events_today: 
                    day_frame_clicked([d, m, y], today_event)
                )
                render_window_canvas.tag_bind(day_name_tag, "<Button-1>", 
                    lambda event, d=cal[week][day], m=looking_for_date[0], y=looking_for_date[1], today_event=yearly_events_today: 
                    day_frame_clicked([d, m, y], today_event)
                )

                if f"{looking_for_date[1]}-{looking_for_date[0]}-{cal[week][day]}" == f"{datetime.now().year}-{datetime.now().month}-{datetime.now().day}":
                    num_steps = -10
                    for step in range(0, num_steps, -1):
                        glow_factor = step / num_steps

                        start_color = [255, 255, 255]
                        color = f"#{int(start_color[0] * glow_factor):02X}{int(start_color[1] * glow_factor):02X}{int(start_color[2] * glow_factor):02X}"
                        glowing = render_window_canvas.create_rectangle(
                            day_frames["x1"] - step + num_steps, 
                            day_frames["y1"] - step + num_steps, 
                            day_frames["x2"] + step - num_steps, 
                            day_frames["y2"] + step - num_steps, 
                            outline=color, 
                            width=1
                        )
                        fades.append(glowing)



            if f"day_box{week}{day}" in global_render_object_dict:
                for i in range(len(global_render_object_dict[f"day_box{week}{day}"])):
                    render_window_canvas.delete(global_render_object_dict[f"day_box{week}{day}"][i])


            global_render_object_dict[f"day_box{week}{day}"] = [day_box_frame]
            if cal[week][day] != 0:
                global_render_object_dict[f"day_box{week}{day}"].append(day_frame_text)
                global_render_object_dict[f"day_box{week}{day}"].append(week_day_name)
                global_render_object_dict[f"day_box{week}{day}"].append(week_day_name_backer)
                for i in fades:
                    global_render_object_dict[f"day_box{week}{day}"].append(i)




def clock():

    if "clock" in global_render_object_dict:
        for i in range(len(global_render_object_dict["clock"])):
            render_window_canvas.delete(global_render_object_dict["clock"][i])

    clock_list = []
    hour_disp = datetime.now().hour
    if len(str(hour_disp)) < 2:
        hour_disp = f"0{hour_disp}"
    hour = render_window_canvas.create_text(
        calendar_window.winfo_width()/20, 
        65,
        text=hour_disp, 
        font=("Arial", 100), 
        fill=color_dict[color_mode]["text_color"][1], 
        anchor="center"
    )
    clock_list.append(hour)

    min_disp = datetime.now().minute
    if len(str(min_disp)) < 2:
        min_disp = f"0{min_disp}"
    minute = render_window_canvas.create_text(
        calendar_window.winfo_width()-(calendar_window.winfo_width()/20), 
        65,
        text=min_disp, 
        font=("Arial", 100), 
        fill=color_dict[color_mode]["text_color"][1], 
        anchor="center"
    )
    clock_list.append(minute)

    global_render_object_dict["clock"] = clock_list
    calendar_window.after(500, clock)

global holidays_of_the_year
holidays_of_the_year = []




# genral global settings and dicts
global view_type
view_type = "month"
global looking_for_date
looking_for_date = [datetime.now().month, datetime.now().year]
global events_of_year
events_of_year = {}
global creating_event
creating_event = False
# defining all the colors in one place to make it easyer to change them
global color_mode
color_mode = "dark_mode" # or light_mode
global color_dict
color_dict ={
    "light_mode":{
        "main_background_color": "#FFF5C2",
        "text_color": "#6DB9EF",
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

# dict of all the things that are renderd
global global_render_object_dict
global_render_object_dict = {}
calendar_window = tk.Tk()
calendar_window.title("calendar app")
calendar_window.state('zoomed')


render_window_canvas = tk.Canvas(
    calendar_window,
    width=calendar_window.winfo_screenwidth(),
    height=calendar_window.winfo_screenheight(),
    # highlightthickness=0,
    background=color_dict[color_mode]["main_background_color"]
)
render_window_canvas.pack()
render_window_canvas.bind("<MouseWheel>", month_scroll)

clock()
# page_title("")
render_window_canvas.bind("<Configure>", window_update)
render_window_canvas.bind("<Button-1>", window_click)

calendar_window.mainloop()