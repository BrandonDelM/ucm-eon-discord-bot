from bs4 import BeautifulSoup
from checksFunctions import get_elements, is_change, log_changes, database_format

def youtube_change(r, file):
    soup = BeautifulSoup(r.text, 'xml')
    entries = get_elements(soup, "entry")
    videos = create_youtube_video_list(entries)
    new_videos = is_change(file, videos)
    log_changes(file, videos)
    return new_videos

def create_youtube_video_list(entries):
    videos = []
    if not entries:
        return []
    
    for entry in entries:
        try:
            youtube_id = entry.find("yt:videoId")
            url = f"http://youtu.be/{youtube_id.text}"
        except:
            url = None
        
        try:
            title = entry.find("title").text
        except:
            title = None

        try:
            author = entry.find("author").find("name").text
        except:
            author = None

        try:
            date = entry.find("published").text
            date = date[:date.find("T")]
        except:
            date = None
        
        videos.append(database_format(author,title,date,"","",url))
    return videos