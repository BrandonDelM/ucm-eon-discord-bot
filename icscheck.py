from ics import Calendar
from checksFunctions import *

#Returns the new events from an ics
def ics_change(r, file):
    cal = Calendar(r.text)
    events = get_ics_events(cal)
    if events is not None:
        events_list = create_ics_event_list(events)
        new_events = is_change(file, events_list)
        log_changes(file, events_list)
        return new_events
    return None

def get_ics_events(cal):
    if cal.events:
        return cal.events
    return None

def create_ics_event_list(events):
    #First time I formally did this
    return [f"{event.name}, {event.begin}, {event.url}" for event in events]