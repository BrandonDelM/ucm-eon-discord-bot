from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, get_elements, database_format

#Returns the new events from an rss
def rss_changes(r, table):
    soup = BeautifulSoup(r.text, 'xml')
    items = get_elements(soup, 'item')
    events = create_rss_events_list(items)
    new_events = is_change(table, events)
    log_changes(table, events)
    return new_events

def create_rss_events_list(items):
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
        events.append(database_format("",title,date,"","",link))
    return events