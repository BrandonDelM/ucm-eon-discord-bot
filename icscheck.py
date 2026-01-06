import requests
from  pathlib import Path
from ics import Calendar
import os

def events_calendar_check(url):
    response = requests.get(url)

    cal = Calendar(response.text)
    if cal:
        events = cal.events
        for event in events:
            print(f"{event.begin}, {event.name}, {event.url}")

def library_check(url):
    response = requests.get(url)

    cal = Calendar(response.text)
    if cal:
        events = cal.events
        events_list = events_to_list(events)
        compiled_events = compile_events(events)

def events_to_list(events):
    #First time I formally did this
    return [f"{event.name}, {event.begin}, {event.url}" for event in events]

def compile_events(events):
    all_events = ""
    for event in events:
        all_events += f"{event.name}, {event.begin}, {event.url}\n"
    return all_events

# def log_changes(name, content):
#     with open(name, "w") as file:
#         file.write(content)

events_calendar_check("https://events.ucmerced.edu/live/ical/events/header/All%20Events")
# library_check("https://libcal.ucmerced.edu/ical_subscribe.php?src=p&cid=7551")