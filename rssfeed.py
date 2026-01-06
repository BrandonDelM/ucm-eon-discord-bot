from bs4 import BeautifulSoup
import requests
import os
from checksFunctions import *

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