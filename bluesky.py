from bs4 import BeautifulSoup
from checksFunctions import is_change, log_changes, get_elements
from blueskyAuth import init_bluesky_client, get_bluesky_feed

#Returns new bluesky post from an rss
def bluesky_change(file):
    client = init_bluesky_client()
    data = get_bluesky_feed(client)
    feed = data.feed
    posts = get_bluesky_post_info(feed)
    new_posts = is_change(file, posts)
    log_changes(file, posts)
    return new_posts

def get_bluesky_post_info(feed):
    posts = []
    for post in feed:
        author = post.post.author.handle
        text = f"{post.post.record.text[:100].replace('\n','')}..."
        date = post.post.record.created_at
        url  = construct_bluesky_url(post)
        posts.append(f"{author}, {text}, {date}, {url}")
    return posts

# bluesky_change("./bluesky_log.txt")

def construct_bluesky_url(post):
    try:
        did = post.post.author.did
    except:
        return None
    
    try:
        uri = post.post.uri
        rkey = uri[uri.rfind("/")+1:]
    except:
        return None
    url = f"https://bsky.app/profile/{did}/post/{rkey}"
    return url