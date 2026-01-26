from bs4 import BeautifulSoup

# Should pass request text in separately from init
# This would allow another column in the google worksheet for headers

class Event():
    def __init__(self):
        self.poster = ""
        self.title = ""
        self.start = ""
        self.end = ""
        self.building = ""
        self.link = ""

class Checker():
    def __init__(self):
        self.url = ""
        self.table = ""
        self.events = []
    
    def set_soup(self, soup):
        self.soup = soup
    
    def get_element(self, element_name):
        element = self.soup.find(element_name)
        return element if element else None
    
    def get_elements(self, element_name):
        elements = self.soup.find_all(element_name)
        return elements if elements else None
    
    def format_events(self):
        return [(poster,title,start,end,building,link) for poster, title, start, end, building, link in zip(self.posters, self.titles, self.starts, self.ends, self.buildings, self.links)]

class CalendarCheck(Checker):
    def __init__(self, calendar):
        self.calendar = calendar

    def get_events(self):
        return self.calendar.events
    
class RSSCheck(Checker):
    pass

class ICSCheck(Checker):
    pass

class FeedCheck(Checker):
    pass

class YouTubeCheck(Checker):
    pass

class BlueSkyCheck(Checker):
    pass

class AaisCloudCheck(Checker):
    pass

class ListServCheck(Checker):
    pass
