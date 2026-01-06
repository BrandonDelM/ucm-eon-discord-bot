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
        event_list.append(f"{events[i].get_text()}, {dates[i].get_text()}, {links[i]}")
    return event_list