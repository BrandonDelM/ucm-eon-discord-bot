import os
import requests
from database import *

def get_elements(soup, element_name):
    if soup.find_all(element_name):
        return soup.find_all(element_name)
    return None

def request(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    return None

def is_same(events, comparison):
    for event in events:
        if event == comparison:
            return True
    return False

def is_change(table, events):
    new = []

    if not table_exists(table):
        create_table(table)
        add_many_to_table(events,table)
        return events
    
    table_items = get_all_rows_from_table(table)

    for event in events:
        if not is_same(table_items, event):
            new.append(event)
    return new

def log_changes(table, events):
    if not table_exists(table):
        create_table(table)
    
    clear_table(table)
    add_many_to_table(events,table)

def database_format(poster="", title="", start="", end="", building="", link=""):
    """""Format so I don't forget:
    poster, 
    title, 
    start, 
    end, 
    building, 
    link
    """
    return (poster,title,start,end,building,link)