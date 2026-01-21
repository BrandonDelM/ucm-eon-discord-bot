from ics import Calendar
from checksFunctions import *

#Returns the new events from an ics
def ics_change(r, table):
    try:
        cal = Calendar(r)
        events = get_ics_events(cal)
        if events is not None:
            events_list = create_ics_event_list(events)
            new_events = is_change(table, events_list)
            log_changes(table, events_list)
            return new_events
        return None
    except ValueError as e:
        print(f"Error parsing ICS calendar: {e}")
        return []
    except Exception as e:
        print(f"Unexpected error in ics_change: {e}")
        return []


def get_ics_events(cal):
    if cal.events:
        return cal.events
    return None

def create_ics_event_list(events):
    return [database_format("", event.name, str(event.begin), "", "", event.url) for event in events]