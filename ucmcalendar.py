import requests
from bs4 import BeautifulSoup
import os

def request(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    return None

def get_calendar(soup):
    return soup.find(class_="fullcalendar-content")

def get_all_events(soup):
    return soup.find_all('h3')

def get_all_dates(soup):
    return soup.find_all('a')

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