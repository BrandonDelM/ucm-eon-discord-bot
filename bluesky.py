from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, get_elements

#Returns new bluesky post from an rss
def bluesky_change(r, file):
    soup = BeautifulSoup(r.text)
    items = get_elements(soup, "item")
    posts = create_bluesky_post_list(items)
    new_posts = is_change(file, posts)
    log_changes(file, posts)
    return new_posts

def create_bluesky_post_list(items):
    posts = []
    for item in items:
        try:
            date = item.pubDate.text
        except:
            date = None

        try:
            link = item.link.text
        except:
            link = None
        
        try:
            description = item.description.text[:100]
        except:
            description = None
        
        posts.append(f"{description}, {date}, {link}")
    return posts