import discord
from discord.ext import commands
import aiohttp
import asyncio
from key import API_KEY

from checksFunctions import *
from googleSheets import init_sheets_client
from sheetsFunctions import *
from dailyevents import get_today_events

from ucmcalendar import calendar_changes
from icscheck import ics_change
from rssfeed import rss_changes
from bluesky import bluesky_change
from aaiscloud import aaiscloud_changes
from youtube import youtube_change
from handshake import handshake_change
from sports import sports_change
from listserv import listserv_change

async def check_for_changes(r, table, url, type):
    match type:
        case "calendar":
            return calendar_changes(r, table, url)
        case "rss":
            return rss_changes(r, table)
        case "ics":
            return ics_change(r, table)
        case"youtube":
            return youtube_change(r, table)
        case "bluesky":
            return bluesky_change(table)
        case "aaiscloud":
            return aaiscloud_changes(table)
        case "handshake":
            return handshake_change(r, table)
        case "sports":
            return sports_change(table)
        case "listserv":
            return await listserv_change(r, table, url)

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

class Client(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sheets_client = init_sheets_client()
        self.feed_sheet = get_sheet(self.sheets_client, "1ras1Fi3I2b_6a8OxEhbHW1LUiDe_3ZH1ou-AlMUYoUA")
        self.update_worksheet = get_worksheet(get_sheet(self.sheets_client, "1CGTzpS3Ie8QTi0HI6xEhTDZoT8j8eRrAcFu-SDcOHpY"), "UPDATES")
        self.updates = []
        self.lock = asyncio.Lock()

    async def on_ready(self):
        self.loop.create_task(self.uc_merced_check())
        self.loop.create_task(self.post_updates())
    
    async def post_updates(self):
        await self.wait_until_ready()
        while not self.is_closed():
            async with self.lock:
                if len(self.updates) > 0:
                    channelid, type, mention, url, new_events = self.updates.pop(0)
                    channel = self.get_channel(channelid)
                    if channel is None:
                        errorchannel = self.get_channel(1331494875350171679)
                        await errorchannel.send(f"Channel {channel} not found")
                    else:
                        messages = message_format(new_events)
                        compiled = ""
                        if mention:
                            compiled += f"<@&{mention}> "
                        compiled += f"**Updates for {type}: {url}**:\n"
                        for message in messages:
                            if len(compiled + f"{message}\n\n") > 2000:
                                await channel.send(compiled)
                                compiled = ""
                                await asyncio.sleep(1)
                            compiled += f"{message}\n\n"
                        if compiled.strip():
                            await channel.send(compiled)
            await asyncio.sleep(5)

    async def on_message(self, message):
        if message.author == self.user:
            return

        if not message.content.startswith('$'):
            return

        if message.content == "$today":
            await self.post_todays_event(message.channel)

    async def post_todays_event(self, channel):
        events = await asyncio.to_thread(get_today_events)
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

    async def automate_check(self, url, channelid, mention, table, type):
        channel = self.get_channel(channelid)
        if channel is None:
            print(f"Error: No channel {channel} for {url}")
            return

        while not self.is_closed():
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    r = await response.text()
            
            if r is None:
                # Corresponds to the #Updates channel
                channel = self.get_channel(1331494875350171679)
                await channel.send(f"Failure to find {url}")
                return
            
            new_events = await check_for_changes(r, table, url, type)

            if new_events is None:
                print(f"new_events returned with a none type: {url}")
                return

            if len(new_events) > 0:
                async with self.lock:
                    messages = messages_text(new_events)
                    await asyncio.to_thread(update_worksheet_logs, self.update_worksheet, messages, url)
                    self.updates.append((channelid, type, mention, url, new_events))
                    print(f"{len(new_events)} updates found for {url}")
            else:
                print(f"No changes for {type}: {url}")
            
            await asyncio.sleep(3600)

    async def get_tasks(self, title, type):
        tasks = []
        worksheet = await asyncio.to_thread(get_worksheet, self.feed_sheet, title)
        urls, channels, mentions, tables = await asyncio.to_thread(get_worksheet_columns, worksheet)
        for i in range(len(urls)):
            task = self.loop.create_task(self.automate_check(urls[i], channels[i], mentions[i], tables[i], type))
            tasks.append(task)
        return tasks

    async def uc_merced_check(self):
        await self.wait_until_ready()
        tasks = []

        tasks.append(self.loop.create_task(self.automate_check("https://bsky.app/profile/starringon.bsky.social/feed/aaajx5bhjuexc", 1459382789060431924, "", "bluesky", "bluesky")))

        tasks.append(self.loop.create_task(self.automate_check("https://www.aaiscloud.com/UCAMerced/default.aspx", 1459661967336804464, "", "aaiscloud", "aaiscloud")))

        #UC Merced Bobcats Sports News
        tasks.append(self.loop.create_task(self.automate_check("https://www.ucmerced.edu/athletics-and-recreation", 1461569361973215334, "", "sports", "sports")))

        tasks.extend(await self.get_tasks("HANDSHAKE", "handshake"))
        tasks.extend(await self.get_tasks("CALENDAR", "calendar"))
        tasks.extend(await self.get_tasks("ICS", "ics"))
        tasks.extend(await self.get_tasks("RSS", "rss"))
        tasks.extend(await self.get_tasks("YOUTUBE", "youtube"))
        tasks.extend(await self.get_tasks("LISTSERV", "listserv"))

        await asyncio.gather(*tasks)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)

client.run(API_KEY)