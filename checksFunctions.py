import os

def is_same(event_list, compare):
    for event in event_list:
        if event.strip() == compare.strip():
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

def log_changes(name, events):
    with open(name, "w") as file:
        for event in events:
            file.write(f"{event}\n")