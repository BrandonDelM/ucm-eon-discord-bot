import requests
from bs4 import BeautifulSoup
import os

def request(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    return None

def is_notable(mismatches, year):
    notables = []
    for mismatch in mismatches:
        if year in mismatch:
            notables.append(mismatch)
    return notables

def is_changed(file_name, compare_list):
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

def get_calendar(soup):
    return soup.find(class_="fullcalendar-content")

def get_all_events(soup):
    return soup.find_all('h3')

def get_all_dates(soup):
    return soup.find_all('a')

def log_changes(name, content):
    with open(name, "w") as file:
        file.write(content)

def prettify_events(dates, events):
    all_events = ""
    for i in range(len(events)):
        all_events += dates[i].get_text() + " - " + events[i].get_text() + "\n"
    return all_events

def format_text(mismatches):
    text = ""
    for mismatch in mismatches:
        if len(text + mismatch + "\n") > 2000:
            break
        text += mismatch + "\n"
    return text

def events_to_list(dates, events):
    compare_list = []
    for i in range(len(events)):
        compare_list.append(dates[i].get_text() + " - " + events[i].get_text())
    return compare_list