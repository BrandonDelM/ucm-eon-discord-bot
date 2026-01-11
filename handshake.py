from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, get_elements

def handshake_change(r, file):
    soup = BeautifulSoup(r.text, "html.parser")
    contents = get_contents(soup)
    headers = get_headers(contents)
    events = get_handshake_event_info(headers)
    new_events = is_change(file, events)
    log_changes(file, events)
    return new_events

def get_handshake_event_info(headers):
    events = []
    for header in headers:
        title = get_titles(header)
        url = get_url(header)
        events.append(f"{title}, {url}")
    return events

def get_contents(soup):
    return soup.find("div", class_="view-content")

def get_headers(contents):
    return contents.find_all("h2", class_="field-content")

def get_titles(header):
    return header.find("a").text

def get_url(header):
    url = "https://hire.ucmerced.edu"
    return f"{url}{header.find("a").get("href")}"

# import requests
# r = requests.get("https://hire.ucmerced.edu/upcoming-events")
# handshake_change(r, "")