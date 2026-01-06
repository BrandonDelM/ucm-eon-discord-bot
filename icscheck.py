import requests
from ics import Calendar
from checksFunctions import *

# def events_calendar_check(url):
#     response = requests.get(url)
#     file = ""

#     cal = Calendar(response.text)
#     if get_ics_events(cal):
#         events = get_ics_events(cal)
#         events_list = create_ics_event_list(events)
#         new_event = is_change(file, events_list)

# def library_check(url):
#     response = requests.get(url)

#     file = ""
#     cal = Calendar(response.text)
#     if cal:
#         events = cal.events
#         events_list = create_ics_event_list(events)
#         new_events = is_change(file, events_list)
#         log_changes(file, events)
#         return new_events

def get_ics_events(cal):
    if cal.events:
        return cal.events
    return None

def create_ics_event_list(events):
    #First time I formally did this
    return [f"{event.name}, {event.begin}, {event.url}" for event in events]