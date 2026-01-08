import os
import requests

def get_elements(soup, element_name):
    if soup.find_all(element_name):
        return soup.find_all(element_name)
    return None

def request(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r
    return None

def is_same(event_list, compare):
    for event in event_list:
        if event.strip() == compare.strip():
            return True
    return False

def is_change(file_name, events):
    new = []

    if not os.path.exists(file_name):
        return [f"**New event**: {event}" for event in events]

    with open(file_name, 'r') as file:
        file_lines = [line.strip() for line in file.readlines()]
    
    for event in events:
        if is_same(file_lines, event) == False:
            new.append(f"**New event**: {event}")
    return new

def log_changes(name, events):
    os.makedirs(os.path.dirname(name), exist_ok=True)
    with open(name, "w") as file:
        for event in events:
            file.write(f"{event}\n")