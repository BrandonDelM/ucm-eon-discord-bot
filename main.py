import discord
import asyncio
from bs4 import BeautifulSoup
from key import API_KEY
import pandas as pd
from ics import Calendar

from ucmcalendar import *
from icscheck import *
from rssfeed import *
from checksFunctions import *
from CSVFunctions import *

def check_for_changes(r, file, url, type):
    if type == "calendar":
        return calendar_changes(r, file, url)
    elif type == "rss":
        return rss_changes(r, file)
    elif type == "ics":
        return ics_change(r, file)

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.loop.create_task(self.uc_merced_calendars_check())

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')
    
    async def automate_check(self, url, channel, file, type, delay_offset=0):
        channel = self.get_channel(channel)
        if  channel is None:
            print(f"Error: No channel {channel} for {url}")
            return

        await asyncio.sleep(delay_offset)

        while not self.is_closed():
            r = request(url)
            if r is None:
                await channel.send(f"Failure to find calendar for {url}")
                return
            
            new_events  = check_for_changes(r, file, url, type)

            new_events_text = ""
            if len(new_events) == 0:
                new_events_text = f"No changes found for {type}: {url}"
            else:
                new_events_text += f"Changes for {url}\n"
                for new_event in new_events:
                    if len(f"{new_events_text}{new_event}\n") > 2000:
                        break
                    new_events_text += f"{new_event}\n"

            await channel.send(new_events_text)
            await asyncio.sleep(3600)


    async def uc_merced_calendars_check(self):
        await self.wait_until_ready()
        tasks = []
        n = 0

        file = "./csvs/calendars.csv"
        type = "calendar"
        df = is_csv_accessible(file)
        if df is not None:
            df = is_csv_accessible(file)
            urls, channels, mentions, files = get_csv_columns(df)
            for i in range(len(urls)):
                task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i], type, delay_offset=i*20))
                n += 1
                tasks.append(task)

        file = "./csvs/ics.csv"
        type = "ics"
        df = is_csv_accessible(file)
        if df is not None:
            urls, channels, mentions, files = get_csv_columns(df)
            for i in range(len(urls)):
                task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i], type, delay_offset=n*20))
                n += 1
                tasks.append(task)

        file = "./csvs/rss.csv"
        type = "rss"
        df = is_csv_accessible(file)
        if df is not None:
            df = is_csv_accessible(file)
            urls, channels, mentions, files = get_csv_columns(df)
            for i in range(len(urls)):
                task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i], type, delay_offset=n*20))
                n += 1
                tasks.append(task)

        await asyncio.gather(*tasks)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(API_KEY)