from bs4 import BeautifulSoup
import requests
import os

def rss_check_for_changes(r, file):
    soup = BeautifulSoup(r.text, 'xml')
    items = get_items(soup)
    events = get_list(items)
    new_events =  is_change(file, events)
    for new_event in new_events:
        print(new_event)
    log_changes(file, events)


def log_changes(name, events):
    with open(name, "w") as file:
        for event in events:
            file.write(f"{event}\n")

def is_same(event_list, compare):
    for event in event_list:
        if event == compare:
            return True
    return False

def is_change(file_name, events):
    new = []

    if not os.path.exists(file_name):
        return [f"New event: {event}" for event in events]

    with open(file_name, 'r') as file:
        file_lines = [line.strip() for line in file.readlines()]
    
    for event in events:
        if is_same(file_lines, event) == False:
            new.append(f"New event: {event}")
    return new

def get_list(items):
    events = []
    for item in items:
        try:
            title = item.title.text
        except:
            title = None

        try:
            date = item.pubDate.text
        except:
            date = None
        
        try:
            link = item.link.text
        except:
            link = None
        events.append(f"{title}, {date}, {link}")
    return events

def get_items(soup):
    if soup.find_all('item'):
        return soup.find_all('item')
    return None

r = requests.get("https://pace.ucmerced.edu/rss.xml")
rss_check_for_changes(r, "logs/rss/pace_log.txt")
# items = soup.find_all('item')
# events = []
# for item in items:
#     try:
#         title = item.title.text
#     except:
#         title = None

#     try:
#         date = item.pubDate.text
#     except:
#         date = None
    
#     try:
#         link = item.link.text
#     except:
#         link = None
    
#     events.append(f"{title}, {date}, {link}")
# is_change("logs/rss/pace_log.txt", events)
# log_changes("logs/rss/pace_log.txt", events)