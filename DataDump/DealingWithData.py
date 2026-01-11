import json
with open("UkHolidaysFile.json", "r") as File:
    Holidays = json.load(File)

DictOfHolidays = {}


for area in Holidays:
    for eventtype in Holidays[area]:
        if type(Holidays[area][eventtype]) == list:
            for event in Holidays[area][eventtype]:
                DictOfHolidays[event["date"]] = event["title"]

# for event in DictOfHolidays:
    # print (event, DictOfHolidays[event])

with open("UkHolidaysNewFile.json", "w") as File:
    json.dump(DictOfHolidays, File)


