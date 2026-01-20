from database import get_all_tables_from_database, get_all_times_from_table, get_like_rows_from_table
from datetime import date
from date_extractor import extract_dates

def get_today_events():
    # Needs to get the entire table
    tables = format_table_times(get_all_tables_from_database())
    today = date.today().isoformat()
    events = [formatted for formatted in tables if today in formatted[2]]
    return events

def messages_text(events):
    messages = []
    for event in events:
        items = [item for item in event if item and str(item).strip()]
        message = ", ".join(items)
        messages.append(message)
    return messages

def format_table_times(tables):
    formatted_tables = []
    for table in tables:
        times = get_like_rows_from_table(table, "start_time", "%2026%")
        for time in times:
            formatted_tables.append((time[0], time[1], str(extract_dates(time[2])[0]), time[3], time[4], time[5]))
    return formatted_tables

# print(get_today_events())