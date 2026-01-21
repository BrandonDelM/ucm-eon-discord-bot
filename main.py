import discord
from discord.ext import commands
import asyncio
from key import API_KEY

from ucmcalendar import *
from icscheck import *
from rssfeed import *
from bluesky import *
from checksFunctions import *
from googleSheets import init_sheets_client
from sheetsFunctions import *
from aaiscloud import aaiscloud_changes
from youtube import youtube_change
from handshake import handshake_change
from sports import sports_change
from dailyevents import get_today_events

def messages_text(events):
    messages = []
    for event in events:
        items = [item for item in event if item and str(item).strip()]
        message = ", ".join(items)
        messages.append(message)
    return messages

def message_format(events):
    messages = []
    for event in events:
        poster, title, start, end, building, link = event
        if link:
            message = f"> :calendar: __New update__: **[{title}]({link})**\n"
        else:
            message = f"> :calendar: __New update__: **{title}**\n"
        if start:
            message += f"> :alarm_clock: __Time__: {start}"
            if end:
                message += f" - {end}"
            message += "\n"
        if building:
            message += f"> :school: __Location__: {building}\n"
        if poster:
            message += f"> :writing_hand:  __Posted By__: {poster}"
        messages.append(message)
    return messages

def check_for_changes(r, table, url, type):
    if type == "calendar":
        return calendar_changes(r, table, url)
    elif type == "rss":
        return rss_changes(r, table)
    elif type == "ics":
        return ics_change(r, table)
    elif type == "youtube":
        return youtube_change(r, table)
    elif type == "bluesky":
        return bluesky_change(table)
    elif type == "aaiscloud":
        return aaiscloud_changes(table)
    elif type == "handshake":
        return handshake_change(r, table)
    elif type == "sports":
        return sports_change(table)

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sheets_client = init_sheets_client()
        self.feed_sheet = get_sheet(self.sheets_client, "1ras1Fi3I2b_6a8OxEhbHW1LUiDe_3ZH1ou-AlMUYoUA")
        self.update_worksheet = get_worksheet(get_sheet(self.sheets_client, "1CGTzpS3Ie8QTi0HI6xEhTDZoT8j8eRrAcFu-SDcOHpY"), "UPDATES")

    async def on_ready(self):
        self.loop.create_task(self.uc_merced_check())
        # self.loop.create_task(self.post_todays_event())

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not message.content.startswith('$'):
            return

        if message.content == "$today":
            await self.post_todays_event(message.channel)

    async def post_todays_event(self, channel):
        events = get_today_events()
        messages = message_format(events)
        compiled = "**Today's Updates**:\n"
        for message in messages:
            if len(compiled + f"{message}\n\n") > 2000:
                await channel.send(compiled)
                compiled = ""
                await asyncio.sleep(20)
            compiled += f"{message}\n\n"
        if len(messages) > 0:
            await channel.send(compiled)

    async def automate_check(self, url, channel, table, type, delay_offset=0):
        channel = self.get_channel(channel)
        if channel is None:
            print(f"Error: No channel {channel} for {url}")
            return

        await asyncio.sleep(delay_offset)

        while not self.is_closed():
            print(f"Checking {type}: {url}")
            r = request(url)
            if r is None:
                # Corresponds to the #Updates channel
                channel = self.get_channel(1331494875350171679)
                await channel.send(f"Failure to find {url}")
                return
            
            new_events = check_for_changes(r, table, url, type)

            # A format for the worksheet update file
            messages = messages_text(new_events)
            update_worksheet_logs(self.update_worksheet, messages, url)

            # A different format specifically for the discord channel
            messages = message_format(new_events)
            compiled = f"**Updates for {type}: {url}**:\n"
            

            for message in messages:
                if len(compiled + f"{message}\n\n") > 2000:
                    await channel.send(compiled)
                    compiled = ""
                    await asyncio.sleep(20)
                compiled += f"{message}\n\n"
            await asyncio.sleep(3600)

    async def get_tasks(self, title, type, offset):
        tasks = []
        worksheet = get_worksheet(self.feed_sheet, title)
        urls, channels, mentions, tables = get_worksheet_columns(worksheet)
        for i in range(len(urls)):
            task = self.loop.create_task(self.automate_check(urls[i], channels[i], tables[i], type, delay_offset=offset*20))
            offset += 1
            tasks.append(task)
        return tasks

    async def uc_merced_check(self):
        await self.wait_until_ready()
        tasks = []
        offset = 0

        tasks.append(self.loop.create_task(self.automate_check("https://bsky.app/profile/starringon.bsky.social/feed/aaajx5bhjuexc", 1459382789060431924, "bluesky", "bluesky", offset)))
        offset = len(tasks)

        tasks.append(self.loop.create_task(self.automate_check("https://www.aaiscloud.com/UCAMerced/default.aspx", 1459661967336804464, "aaiscloud", "aaiscloud", offset)))
        offset = len(tasks)

        #UC Merced Bobcats Sports News
        tasks.append(self.loop.create_task(self.automate_check("https://www.ucmerced.edu/athletics-and-recreation", 1461569361973215334, "sports", "sports", offset)))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("HANDSHAKE", "handshake", offset))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("CALENDAR", "calendar", offset))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("ICS", "ics", offset))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("RSS", "rss", offset))
        offset = len(tasks)

        tasks.extend(await self.get_tasks("YOUTUBE", "youtube", offset))
        offset = len(tasks)

        await asyncio.gather(*tasks)

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)

client = Client(intents=intents)

client.run(API_KEY)