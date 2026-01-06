import discord
import datetime
import asyncio
import requests
from bs4 import BeautifulSoup
from ucmcalendar import *
from key import API_KEY
import pandas as pd
from rssfeed import *
from checksFunctions import *

def rss_changes(r, file):
    soup = BeautifulSoup(r.text, 'xml')
    items = get_items(soup)
    events = create_rss_events_list(items)
    new_events = is_change(file, events)
    log_changes(file, events)
    return new_events

def check_for_changes(r, file, url, type):
    if type == "calendar":
        return calendar_changes(r, file, url)
    elif type == "rss":
        return rss_changes(r, file)

def calendar_changes(r, file, url):
    url = url[:url.rfind("/")]
    soup  = BeautifulSoup(r.text, 'html.parser')
    calendar = get_calendar(soup)
    events, dates, links = get_calendar_event_info(calendar, url)

    events_list = create_calendar_event_list(dates, events, links)

    new = is_change(file, events_list)
    log_changes(file, events_list)

    return new

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
        try:
            df = pd.read_csv("./csvs/calendars.csv")
        except FileNotFoundError:
            print("./csv/calendars.csv can't be found")
            return
        except Exception as e:
            print("Error reading ./csv/calendar.csv: " + e)
            return
        
        urls = df['URL']
        channels = df['CHANNEL']
        files = df['FILE']
        tasks = []
        n = 0
        type = "calendar"
        for i in range(len(urls)):
            task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i], type, delay_offset=i*20))
            n += 1
            tasks.append(task)

        try:
            df = pd.read_csv("./csvs/rss.csv")
        except FileNotFoundError:
            print("./csv/rss.csv can't be found")
            return
        except Exception as e:
            print("Error reading ./csv/rss.csv: " + e)
            return
        urls = df['URL']
        channels = df['CHANNEL']
        mentions = df['MENTION']
        files = df['FILE']
        type = "rss"
        for i in range(len(urls)):
            task = self.loop.create_task(self.automate_check(urls[i], channels[i], files[i], type, delay_offset=n*20))
            n += 1
            tasks.append(task)

        await asyncio.gather(*tasks)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(API_KEY)