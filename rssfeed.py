from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes

#Returns the new events from an rss
def rss_changes(r, file):
    soup = BeautifulSoup(r.text, 'xml')
    items = get_items(soup)
    events = create_rss_events_list(items)
    new_events = is_change(file, events)
    log_changes(file, events)
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
        events.append(f"{title}, {date}, {link}")
    return events

def get_items(soup):
    if soup.find_all('item'):
        return soup.find_all('item')
    return None