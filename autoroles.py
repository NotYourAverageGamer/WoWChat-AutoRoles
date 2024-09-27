import os
import logging
import re
import discord
from colorama import init, Fore, Style
from dotenv import load_dotenv

# Initialize colorama and load environment variables
init()
load_dotenv()

SERVER_ID = int(os.getenv('SERVER_ID'))
ROLE_NAME = os.getenv('ROLE_NAME')
CHANNEL_ID = int(os.getenv('CHANNEL_ID'))
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
WOWCHAT = os.getenv('WOWCHAT')

# Logging
class ColorFormatter(logging.Formatter):
    def format(self, record):
        date = f'{Fore.LIGHTBLACK_EX}{self.formatTime(record, self.datefmt)}{Style.RESET_ALL}'
        levelname = {
            'INFO': f'{Fore.BLUE}{record.levelname}{Style.RESET_ALL}',
            'ERROR': f'{Fore.RED}{record.levelname}{Style.RESET_ALL}',
            'WARNING': f'{Fore.YELLOW}{record.levelname}{Style.RESET_ALL}'
        }.get(record.levelname, record.levelname)
        message = record.getMessage()
        return f'{date} {levelname} {message}'

root_logger = logging.getLogger()
if not root_logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = ColorFormatter('%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    handler.setFormatter(formatter)
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(handler)

discord_logger = logging.getLogger('discord')
discord_logger.propagate = False

# Intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
client = discord.Client(intents=intents)

async def parse_and_assign_roles(message_content):
    # Extract player names from the message content using regex
    player_names = re.findall(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*(?=\s\()', message_content)
    if not player_names:
        logging.warning('%s!! No player names found in message content.%s', Fore.LIGHTYELLOW_EX, Style.RESET_ALL)
        return

    logging.info('%s~ Parsed player names:%s %s', Fore.YELLOW, Style.RESET_ALL, ", ".join(player_names))

    guild = client.get_guild(SERVER_ID)
    if not guild:
        logging.error('%s!! Server with ID%s %d %snot found.%s', Fore.RED, Style.RESET_ALL, SERVER_ID, Fore.RED, Style.RESET_ALL)
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if not role:
        logging.error('%s!! Role %s%s%s not found in the server.%s', Fore.RED, Style.RESET_ALL, ROLE_NAME, Fore.RED, Style.RESET_ALL)
        return

    for member in guild.members:
        if member.nick in player_names or member.name in player_names:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                    logging.info('%s+ Assigned %s%s%s role to %s%s', Fore.GREEN, Style.RESET_ALL, ROLE_NAME, Fore.GREEN, Style.RESET_ALL, member.display_name)
                except discord.Forbidden:
                    logging.error('%s!! Permission denied assigning role to %s%s', Fore.RED, Style.RESET_ALL, member.display_name)
                except discord.HTTPException as e:
                    logging.error('%s!! Failed assigning role to %s%s: %s', Fore.RED, Style.RESET_ALL, member.display_name, e)
            else:
                logging.info('%s- %s%s%s already has the %s%s%s role.%s', Fore.BLUE, Style.RESET_ALL, member.display_name, Fore.BLUE, Style.RESET_ALL, ROLE_NAME, Fore.BLUE, Style.RESET_ALL)

@client.event
async def on_ready():
    logging.info('%s+ Logged in as %s%s', Fore.GREEN, Style.RESET_ALL, client.user)
    if not client.get_channel(CHANNEL_ID):
        logging.error('%s!! Channel with ID %s%d%s not found.%s', Fore.RED, Style.RESET_ALL, CHANNEL_ID, Fore.RED, Style.RESET_ALL)
        await client.close()
        return

    await client.get_channel(CHANNEL_ID).send('?who')

@client.event
async def on_message(message):
    if message.author.name == WOWCHAT and message.channel.id == CHANNEL_ID:
        if re.match(r'^Currently \d+ guildies online:', message.content):
            await parse_and_assign_roles(message.content)

client.run(DISCORD_TOKEN)
