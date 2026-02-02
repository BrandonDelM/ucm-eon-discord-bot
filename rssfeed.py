from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, get_elements, get_element, database_format
import lxml

#Returns the new events from an rss
def rss_changes(r, table):
    soup = BeautifulSoup(r, 'xml')
    items = get_elements(soup, 'item')
    if items is None:
        print(f"No return found for link with table {table}")
        return []
    events = create_rss_events_list(items)
    new_events = is_change(table, events)
    log_changes(table, events)
    return new_events

def create_rss_events_list(items):
    events = []
    for item in items:
        poster = get_element(item, "dc:creator").get_text(strip=True) if get_element(item, "dc:creator") is not None else None
        title = get_element(item, "title").get_text() if get_element(item, "title").get_text() is not None else None
        start = get_element(item, "pubDate").get_text() if get_element(item, "pubDate").get_text() is not None else None
        url = get_element(item, "link").get_text() if get_element(item, "link").get_text() is not None else None
        events.append(database_format(poster,title,start,"","",url))
    return events