from ics import Calendar
from checksFunctions import *

#Returns the new events from an ics
def ics_change(r, table):
    cal = Calendar(r.text)
    events = get_ics_events(cal)
    if events is not None:
        events_list = create_ics_event_list(events)
        new_events = is_change(table, events_list)
        log_changes(table, events_list)
        return new_events
    return None

def get_ics_events(cal):
    if cal.events:
        return cal.events
    return None

def create_ics_event_list(events):
    return [database_format("", event.name, event.begin, "", "", event.url) for event in events]