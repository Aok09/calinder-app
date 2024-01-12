import calendar, time, os, json, requests
import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta
from tkinter import colorchooser, messagebox, font
from pynput import mouse, keyboard


# this is genrating alot of the thigns that are displayed
def generate_month_list(month_displayed, year_displayed, num_months=[1, 10]):
    # Set the day to 1 to ensure consistent day across months_list
    month = datetime.now().replace(day=1, month=month_displayed, year=year_displayed)  
    months_list = [month.strftime("%B %Y")]
    for _ in range(num_months[0]):
        month -= timedelta(days=month.day)
        months_list.insert(0, month.strftime("%B %Y"))

    month = datetime.now().replace(day=1, month=month_displayed, year=year_displayed)  # Reset to the current month
    for _ in range(num_months[1]):
        month += timedelta(days=32)  # Move to the next month
        month = month.replace(day=1)  # Set the day to 1 to ensure consistent day across months_list
        months_list.append(month.strftime("%B %Y"))
    return months_list

def get_holidays(looking_for_date, events_of_year):

    return []
    holidays_types = [
        "public_holiday",
        "observance",
        "national_holiday",
        "federal_holiday",
        "season",
        "state_holiday",
        "optional_holiday",
        "clock_change_daylight_saving_time",
        "local_holiday",
        "united_nations_observance",
        "observance_christian",
        "bank_holiday",
        "common_local_holiday",
        "national_holiday_christian",
        "christian",
        "observance_hebrew",
        "jewish_holiday",
        "muslim",
        "hindu_holiday",
        "restricted_holiday",
        "official_holiday",
        "national_holiday_orthodox",
        "local_observance"
    ]

    new_year = True
    if looking_for_date[1] < 2031:
        for i in events_of_year:
            if str(looking_for_date[1]) in i:
                new_year = False
                break
    else:
        new_year = False

    if new_year == True:

        try:
            api_url = f'https://api.api-ninjas.com/v1/holidays?country=GB&year={looking_for_date[1]}'.format("GB", looking_for_date[1])
            response = requests.get(api_url, headers={'X-Api-Key': '73vhBVXMJUfKD0GGpZ6Plg==AjLjBMPndJn6j97H'})


            public_holidays = json.loads(response.content)

            for public_holiday in public_holidays:
                events_of_year[public_holiday["date"]] = public_holiday["name"]

        except:
            return []
    return events_of_year


def line_spliter(text, max_len):
    text = str(text)

    if "/" in list(text) and len(text) > max_len:
        return text.replace('/', '\n')

    if "(" in list(text) and len(text) > max_len:
        line_1 = text.split("(")
        if len(line_1) < 2:
            for i in range(len(text)):
                if list(text)[i] == "(":
                    line_2 = text[i:]
                    break
            line_1 = text.split("(")[0]


        else:
            line_1 = text.split("(")[0]
            line_2 = f"{text.split('(')[1]}"

            if len(line_1) > len(line_2):
                out_text = line_1 + "\n" + f"({line_2}".center(len(line_1))
            else:
                out_text = line_1.center(len(line_2)) + "\n(" + line_2

            return out_text

        if len(line_1) > len(line_2):
            out_text = line_1 + "\n" + f"({line_2}".center(len(line_1))
        else:
            out_text = line_1.center(len(line_2)) + "\n" + line_2

        # print ("braket split", out_text)
        return out_text

    if len(text) > max_len:
        text = text.split(" ")

        line_1 = text.pop(0)
        for i in range(int(len(text)/2)):
            line_1 = line_1 + " " + text.pop(0)

        # out_text = out_text + "\n"
        line_2 = text.pop(0)
        for i in range(int(len(text))):
            line_2 = line_2 + " " + text.pop(0)

        if len(line_1) > len(line_2):
            out_text = line_1 + "\n" + line_2.center(len(line_1))
        else:
            out_text = line_1.center(len(line_2)) + "\n" + line_2

        # print ("split", out_text)
        return out_text

    # print ("no change", text)
    return text


def read_events(year, month, day):
    file_path = f"data/events/{year}/{month}/{day}.json"

    if os.path.exists(file_path):
        file = open(file_path, 'r')
        day_events = json.load(file)
        file.close()

        return day_events

    return 404


def text_formatter(text, max_line_length):
    out_text = ""
    line_len = 0
    for i in list(text):
        line_len += 1
        out_text = out_text + i
        if i == " " or i == "\n":
            last_space = len(out_text)

        if line_len == max_line_length:
            out_text = (out_text[:last_space]) + "\n" + out_text[last_space:]
            line_len = 0

    return out_text