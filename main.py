import discord
import datetime
import asyncio
import requests
from bs4 import BeautifulSoup
from scrape import *
from key import API_KEY

class Client(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.loop.create_task(self.cec_message())

    async def on_message(self, message):
        if message.author == self.user:
            return
        
        if message.content.startswith('hello'):
            await message.channel.send(f'Hi there {message.author}')
    
    async def cec_message(self):
        await self.wait_until_ready()
        channel = self.get_channel(1456771381629812787)
        file = "cec_log.txt"
        while not self.is_closed():
            await asyncio.sleep(3600)
            if channel:
                r = request("https://cec.ucmerced.edu/calendar")
                if r is None:
                    await channel.send("Failure to find calendar")
                    continue

                soup  = BeautifulSoup(r.text, 'html.parser')
                calendar = get_calendar(soup)
                events = get_all_events(calendar)
                dates = get_all_dates(calendar)

                content = prettify_events(dates, events)
                events_list = events_to_list(dates, events)

                mismatches = is_changed(file, events_list)

                notables = is_notable(mismatches, f"{datetime.datetime.now().year}")
                compiled_notables = format_text(notables)

                if len(notables) == 0:
                    await channel.send("No changes")
                else:
                    await channel.send(compiled_notables)
                
                log_changes(file, content)
        

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(API_KEY)