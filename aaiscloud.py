from aaiscloudlink import build_aaiscloud_calendar_url, get_aaiscloud_headers
from checksFunctions import is_change, log_changes, database_format
import requests

def aaiscloud_changes(table):
    data = get_aaiscloud_events()
    events_data = data['data']
    events = get_aaiscloud_event_info(events_data)
    new_events = is_change(table, events)
    log_changes(table, events)
    return new_events

def get_aaiscloud_event_info(events_data):
    events = []
    for event in events_data:
        instructor = get_instructor(event)
        name = get_activity_name(event)
        start = get_start_date(event)
        end = get_end_date(event)
        building = get_building(event)
        events.append(database_format(instructor,name,start,end,building,""))
    return events

def get_aaiscloud_events():
    url = build_aaiscloud_calendar_url(days=1)
    headers = get_aaiscloud_headers()
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    return None

def get_instructor(data):
    return data[17]

def get_activity_name(data):
    return data[1]

def get_start_date(data):
    return data[8]

def get_end_date(data):
    return data[9]

def get_building(data):
    return data[7]