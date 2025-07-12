__version__ = "2.0.0"

import logging
import re
import asyncio
import discord

from colorama import Fore, Style
from config import load_config
from logger import setup_logger
from roles import parse_and_assign_roles


setup_logger()
config = load_config()

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    logging.info('%s+ Logged in as %s%s', Fore.GREEN, Style.RESET_ALL, client.user)
    guild = client.get_guild(config['SERVER_ID'])
    if not guild:
        logging.error('%s!! Server with ID%s %d %snot found.%s', Fore.RED, Style.RESET_ALL, config['SERVER_ID'], Fore.RED, Style.RESET_ALL)
        await client.close()
        return

    channel = client.get_channel(config['CHANNEL_ID'])
    if not channel:
        logging.error('%s!! Channel with ID %s%d%s not found.%s', Fore.RED, Style.RESET_ALL, config['CHANNEL_ID'], Fore.RED, Style.RESET_ALL)
        await client.close()
        return

    await channel.send('?who')

    if config['WHO_INTERVAL_ENABLED']:
        logging.info('%s~ WHO interval enabled, running every %d hours%s.', Fore.CYAN, config['WHO_INTERVAL_HOURS'], Style.RESET_ALL)
        asyncio.create_task(who_interval_task(channel, config['WHO_INTERVAL_HOURS']))

@client.event
async def on_message(message):
    if message.author.name == config['WOWCHAT'] and message.channel.id == config['CHANNEL_ID']:
        if re.match(r'^Currently \d+ guildies online:', message.content):
            guild = client.get_guild(config['SERVER_ID'])
            await parse_and_assign_roles(client, guild, config['ROLE_NAME'], message.content)

async def who_interval_task(channel, interval_hours):
    while True:
        await asyncio.sleep(interval_hours * 3600)
        logging.info('%s~ Running ?who command%s', Fore.CYAN, Style.RESET_ALL)
        await channel.send('?who')

client.run(config['DISCORD_TOKEN'])
