from checksFunctions import is_change, log_changes, database_format
import aiohttp

async def sports_change(table):
    data = await get_sports_data()
    news_data = data['data']
    news = get_sports_news(news_data)
    new_news = is_change(table, news)
    log_changes(table, news)
    return new_news

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

async def get_sports_data():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
    }
    url = "https://ucmercedbobcats.com/services/archives.ashx/stories?index=1&page_size=30&sport=0&season=0"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                if response.status ==  200:
                    return await response.json()
                else:
                    print(f"Sports couldn't retrieved the new news with status {response.status}")
                    return None
    except Exception as e:
        print(f"Exception for {url}: {e}")
        return None


# async def sport_test():
#     data = await get_sports_data()
#     print(data)

# import asyncio
# asyncio.run(sport_test())