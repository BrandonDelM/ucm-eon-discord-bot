from bs4 import BeautifulSoup
import requests
import os
from checksFunctions import *

def rss_check_for_changes(r, file):
    soup = BeautifulSoup(r.text, 'xml')
    items = get_items(soup)
    events = get_list(items)
    new_events =  is_change(file, events)
    for new_event in new_events:
        print(new_event)
    log_changes(file, events)

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