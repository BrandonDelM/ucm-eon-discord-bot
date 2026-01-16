from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, database_format



def sports_change(file):
    data = get_sports_data()
    news_data = data['data']
    news = get_sports_news(news_data)
    new_news = is_change(file, news)
    log_changes(file, news)
    return new_news

import requests

def get_sports_news(news_data):
    news = []
    for headline in news_data:
        try:
            title = headline['story_headline']
        except:
            title = headline
        
        try:
            date = headline['story_postdate']
        except:
            date = headline
        
        try:
            link = f"https://ucmercedbobcats.com{headline['story_path']}"
        except:
            link = None
        news.append(database_format("",title,date,"","",link))
    return news

def get_sports_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36"
    }
    url = "https://ucmercedbobcats.com/services/archives.ashx/stories?index=1&page_size=30&sport=0&season=0"
    response = requests.get(url, headers=headers)
    if response.status_code ==  200:
        return response.json()
    return None


from database import *
def sport_test():
    data = get_sports_data()
    news_data = data['data']
    news = get_sports_news(news_data)
    new_news = is_change(news,"sports")
    for new in new_news:
        print(new)
    log_changes("sports",news)
    return new_news

sport_test()