from bs4 import BeautifulSoup
import requests
from checksFunctions import is_change, log_changes, database_format

def listserv_change(r, table, url):
    soup = BeautifulSoup(r, "html.parser")
    email_url = get_archive_link(soup, url)

    r = requests.get(email_url)
    if r is None:
        print(f"No archive found for {url}")
        return []
    soup = BeautifulSoup(r.text, "html.parser")
    emails = get_email_info(soup, email_url)
    new_emails = is_change(table, emails)
    log_changes(table, emails)
    return new_emails

def get_archive_link(soup, url):
    table = soup.find('table')
    if (len(table.find_all('tr'))) <= 1:
        return ""

    row = table.find_all('tr')[1]
    email_url = f"{url}{row.find('a').get('href')}"
    return email_url

def get_email_info(soup, url):
    if (len(soup.find_all("ul")) < 2):
        return []
    items = []
    emails = soup.find_all("ul")[1]
    subjects = emails.find_all("a", href=True)
    url = url[:url.rfind("/")+1]
    for subject in subjects:
        title = subject.text.strip()
        html = subject.get('href')
        link = f"{url}{html}"
        items.append(database_format("",title,"","","",link))
    return items

# url = "https://lists.ucmerced.edu/pipermail/health_scholars/"
# r = requests.get(url)
# listserv_change(r.text, "health_scholars_listserv", url)