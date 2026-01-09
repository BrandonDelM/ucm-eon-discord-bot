import discord
import asyncio
from key import API_KEY

from ucmcalendar import *
from icscheck import *
from rssfeed import *
from checksFunctions import *
from bluesky import *
from googleSheets import init_sheets_client
from sheetsFunctions import *

def check_for_changes(r, file, url, type):
    if type == "calendar":
        return calendar_changes(r, file, url)
    elif type == "rss":
        return rss_changes(r, file)
    elif type == "ics":
        return ics_change(r, file)
    elif type == "youtube":
        return rss_changes(r, file)
    elif type == "bluesky":
        return bluesky_change(file)

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sheets_client = init_sheets_client()
        self.feed_sheet = get_sheet(self.sheets_client, "1ras1Fi3I2b_6a8OxEhbHW1LUiDe_3ZH1ou-AlMUYoUA")
        self.update_worksheet = get_worksheet(get_sheet(self.sheets_client, "1CGTzpS3Ie8QTi0HI6xEhTDZoT8j8eRrAcFu-SDcOHpY"), "UPDATES")

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.loop.create_task(self.uc_merced_calendars_check())

    async def automate_check(self, url, channel, file, type, delay_offset=0):
        channel = self.get_channel(channel)
        if channel is None:
            print(f"Error: No channel {channel} for {url}")
            return

        await asyncio.sleep(delay_offset)

        while not self.is_closed():
            r = request(url)
            if r is None and file:
                await channel.send(f"Failure to find {url}")
                return
            
            new_events = check_for_changes(r, file, url, type)
            update_worksheet_logs(self.update_worksheet, new_events, type, url)

            new_events_text = ""
            if len(new_events) == 0:
                new_events_text = f"No changes found for {type}: {url}"
            else:
                new_events_text += f"Changes for {type}: {url}\n"
                for new_event in new_events:
                    if len(f"{new_events_text}{new_event}\n") > 2000:
                        break
                    new_events_text += f"{new_event}\n"

            await channel.send(new_events_text)
            await asyncio.sleep(3600)

    async def get_tasks(self, title, type, offset):
        tasks = []
        worksheet = get_worksheet(self.feed_sheet, title)
        urls, channels, mentions, files = get_worksheet_columns(worksheet)
        for i in range(len(urls)):
            task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i], type, delay_offset=offset*20))
            offset += 1
            tasks.append(task)
        return tasks


    async def uc_merced_calendars_check(self):
        await self.wait_until_ready()
        tasks = []
        offset = 0

        # tasks.extend(await self.bluesky_check(1456797841803444367, "logs/bluesky/bluesky_log.txt", offset))
        # offset = len(tasks)

        tasks.extend(await self.get_tasks("CALENDAR", "calendar", offset))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("ICS", "ics", offset))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("RSS", "rss", offset))
        offset = len(tasks)

        await asyncio.gather(*tasks)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(API_KEY)