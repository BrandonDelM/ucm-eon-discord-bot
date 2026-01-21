### A Discord bot created for the UC Merced Events, Opportunities, and News (UCM EON) Discord, a server dedicated to supplying the previously mentioned updates to students, alumni, and faculty regarding UC Merced. 🤖

---
## Notable Libraries and APIs used 📚

* Implements the [discord.py](https://github.com/Rapptz/discord.py) API wrapper for coding in Python along with the [asyncio](https://docs.python.org/3/library/asyncio.html) library to handle rate limiting.
* The [Google Sheets API](https://developers.google.com/workspace/sheets/api/guides/concepts) provides the necessary links for checking alongside the Discord channel IDs, role IDs, and database tables.
* [Requests](https://en.wikipedia.org/wiki/Requests_(software)) and [Beautiful Soup](https://en.wikipedia.org/wiki/Beautiful_Soup_(HTML_parser)) are implemented to make the HTTPs requests and parse the HTML to monitor specific data, respectively.
* [sqlite3](https://docs.python.org/3/library/sqlite3.html) for data storage, with data from each URL being stored in a unique table. Data is then compared through each URL check for updates.
* The [atproto SDK](https://pypi.org/project/atproto/) is used specifically to get the post from the [UC Merced feed](https://bsky.app/profile/starringon.bsky.social/feed/aaajx5bhjuexc) created by me using [SkyFeed](https://skyfeed.app/).

---
## Files for monitoring 🔎
Files are split up for different feeds:

* **ucmcalendar.py** helps parse the HTML for events and calendar pages on the ucmerced.edu website.
* **icscheck.py** checks specific UC Merced related ics using the [ics iCalendar library](https://icspy.readthedocs.io/en/stable/)
* **rssfeed.py** monitors various feeds in an RSS format, including blogs, websites, and mailing lists.
* **aaiscloud.py** uses the aaiscloud RESTful API to obtain the daily events.
* **bluesky.py** checks the created UC Merced feed for new posts on BlueSky.
* **handshake.py** was specifically made for the Student Career Center's Handshake feed, but has been integrated into other niche cases of event monitoring.
* **sports.py** checks for news related to the UC Merced athletic news, using the RESTful API for news.

---
## Other files 📂
* **database.py** hosts various functions that are essential in updating the SQLite database and are used in every file mentioned above.
* **main.py** holds all the code used for providing the UCM EON Discord with updates by using the discord.py API wrapper.
* **sheets.py** both retrieves the URLs, channel IDs, role IDs, and unique table names for monitoring from one worksheet and writes the URL updates into a separate worksheet.
* **checksFunctions.py** and **sheetsFunctions.py** are separate files meant for the monitoring and sheets code, respectively.
  * **checksFunctions.py** is used throughout the project to reduce code length for each file.

---
## Notable changes during development 📝
* Originally stored URLs in a CSV file created using Google Sheets before using the Google Sheets API, bypassing the need for CSV files
* Began the project by storing data for each URL in separate text files sorted by URL type. Later switched to sqlite3 to store data in a database file.
* Earlier functions had unique comparison checks before creating **checksFunctions.py** to reduce repetitive code.

---
## Future goals 🏃‍♀️🏃‍♂️
* Use the Google Drive API to store and backup the database onto Google Drive to avoid data corruption.
* Create a github page that host the formatted events for people to see alongside the Discord.
* Implement a 'Today's events' functionality that would update the server on events happening that day. ✅
* Implement a RESTful API for other UC Merced student developers to retrieve events in a given time scale.
