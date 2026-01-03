import discord
import datetime
import asyncio
import requests
from bs4 import BeautifulSoup
from scrape import *
from key import API_KEY
import pandas as pd

def check_for_changes(r, file):
    soup  = BeautifulSoup(r.text, 'html.parser')
    calendar = get_calendar(soup)
    events = get_all_events(calendar)
    dates = get_all_dates(calendar)

    content = prettify_events(dates, events)
    events_list = events_to_list(dates, events)

    mismatches = is_changed(file, events_list)
    log_changes(file, content)

    return is_notable(mismatches, f"{datetime.datetime.now().year}")


class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.loop.create_task(self.uc_merced_calendars_check())

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')
    
    async def automate_check(self, url, channel, file):
        channel = self.get_channel(channel)
        if  channel is None:
            print(f"Error: No channel {channel} for {url}")
            return

        while not self.is_closed():
            r = request(url)
            if r is None:
                await channel.send("Failure to find calendar for psychological Sciences")
                continue
            
            notables  = check_for_changes(r, file)

            if len(notables) == 0:
                await channel.send(f"No changes for {url}")
            else:
                compiled_notables = format_text(notables)
                await channel.send(compiled_notables)
            await asyncio.sleep(3600)

    async def uc_merced_calendars_check(self):
        await self.wait_until_ready()
        try:
            df = pd.read_csv("./csvs/calendars.csv")
        except FileNotFoundError:
            print("calendars.csv can't be found")
            return
        except Exception as e:
            print("Error reading Calendar.csv: " + e)
            return
        
        urls = df['URL']
        channels = df['CHANNEL']
        files = df['FILE']
        tasks = []
        for i in range(len(urls)):
            task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i]))
            tasks.append(task)
        await asyncio.gather(*tasks)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(API_KEY)