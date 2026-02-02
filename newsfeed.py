from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, database_format

def newsfeed_change(r, table, url):
    soup = BeautifulSoup(r, "html.parser")
    contents = get_contents(soup)
    headers = get_headers(contents)
    events = get_newsfeed_event_info(headers, url)
    new_events = is_change(table, events)
    log_changes(table, events)
    return new_events

def get_newsfeed_event_info(headers, page_url):
    events = []
    for header in headers:
        title = get_titles(header)
        url = get_url(header, page_url)
        events.append(database_format("",title,"","","",url))
    return events

def get_contents(soup):
    return soup.find("div", class_="view-content")

def get_headers(contents):
    return contents.find_all("h2", class_="field-content")

def get_titles(header):
    return header.find("a").text

def get_url(header, url):
    page_url = url[:url.rfind("/")]
    return f"{page_url}{header.find("a").get("href")}"

from database import *
def newsfeed_change_test(r, url):
    soup = BeautifulSoup(r.text, "html.parser")
    contents = get_contents(soup)
    headers = get_headers(contents)
    events = get_newsfeed_event_info(headers, url)
    for event in events:
        print(event)

import requests
r = requests.get("https://dfa.ucmerced.edu/news")
newsfeed_change_test(r, "https://dfa.ucmerced.edu/news")