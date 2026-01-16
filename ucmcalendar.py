from bs4 import BeautifulSoup
from  checksFunctions import is_change, log_changes, database_format

#Returns the new events from a calendar
def calendar_changes(r, table, url):
    url = url[:url.rfind("/")]
    soup  = BeautifulSoup(r.text, 'html.parser')
    calendar = get_calendar(soup)
    events, dates, links = get_calendar_event_info(calendar, url)

    events_list = create_calendar_event_list(dates, events, links)

    new = is_change(table, events_list)
    log_changes(table, events_list)

    return new

def get_calendar(soup):
    return soup.find(class_="fullcalendar-content")

def get_all_events(soup):
    return soup.find_all('h3')

def get_all_dates(soup):
    return soup.find_all('a')

def get_all_links(soup, url):
    a_elements = soup.find_all('a')
    return [f"{url}{a_element.get('href')}" for a_element in a_elements if a_element.get('href')]

def get_calendar_event_info(soup, url):
    return get_all_events(soup), get_all_dates(soup), get_all_links(soup, url)

def create_calendar_event_list(dates, events, links):
    event_list = []
    for i in range(len(events)):
        event_list.append(database_format("",events[i],dates[i],"","",links[i]))
    return event_list