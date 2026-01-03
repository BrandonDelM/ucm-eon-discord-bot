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
        mismatches = has_changed("logs/libcal_log.txt", events_list)
        if (len(mismatches)  == 0):
            print("No changes")
        for event in events_list:
            print(f"{event}")
        log_changes("logs/libcal_log.txt", compiled_events)

def is_notable(mismatches, year):
    notables = []
    for mismatch in mismatches:
        if year in mismatch:
            notables.append(mismatch)
    return notables

def has_changed(file_name, compare_list):
    mismatches = []

    if not os.path.exists(file_name):
        return [f"New event added: {item}" for item in compare_list]
    
    with open(file_name, 'r') as file:
        file_lines = [line.strip() for line in file.readlines()]

    max_len = max(len(file_lines), len(compare_list))

    for i in range(max_len):
        if i >= len(file_lines):
            add = 0
        elif i >= len(compare_list):
            removed = 0
        elif file_lines[i] != compare_list[i].strip():
            mismatches.append(f"Changed: {file_lines[i]} -> {compare_list[i]}")
    return mismatches

def events_to_list(events):
    #First time I formally did this
    return [f"{event.name}, {event.begin}, {event.url}" for event in events]

def compile_events(events):
    all_events = ""
    for event in events:
        all_events += f"{event.name}, {event.begin}, {event.url}\n"
    return all_events

def log_changes(name, content):
    with open(name, "w") as file:
        file.write(content)

events_calendar_check("https://events.ucmerced.edu/live/ical/events/header/All%20Events")
# library_check("https://libcal.ucmerced.edu/ical_subscribe.php?src=p&cid=7551")