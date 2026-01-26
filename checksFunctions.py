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

def is_change(table, events):
    new = []

    create_table(table)
    
    table_items = get_all_rows_from_table(table)
    if not table_items:
        add_many_to_table(events,table)
        return events

    table_set = set(table_items) if table_items else set()

    for event in events:
        if event not in table_set:
            new.append(event)
    return new

def log_changes(table, events):
    create_table(table)
    
    clear_table(table)
    add_many_to_table(events,table)

def database_format(poster="", title="", start="", end="", building="", link=""):
    return (poster,title,start,end,building,link)