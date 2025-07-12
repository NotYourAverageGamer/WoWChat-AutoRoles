import re
import logging
import discord
from colorama import Fore, Style

def normalize_name(name):
    return re.sub(r'[^a-z]', '', name.lower())

async def parse_and_assign_roles(client, guild, role_name, message_content):
    player_names = re.findall(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*(?=\s\()', message_content)
    player_names = [normalize_name(name) for name in player_names]
    if not player_names:
        logging.warning('%s!! No player names found in message content.%s', Fore.LIGHTYELLOW_EX, Style.RESET_ALL)
        return

    logging.info('%s~ Parsed player names:%s %s', Fore.YELLOW, Style.RESET_ALL, ", ".join(player_names))

    role = discord.utils.get(guild.roles, name=role_name)
    if not role:
        logging.error('%s!! Role %s%s%s not found in the server.%s', Fore.RED, Style.RESET_ALL, role_name, Fore.RED, Style.RESET_ALL)
        return

    unmatched_names = set(player_names)

    await guild.chunk()
    for member in guild.members:
        display_name_normalized = normalize_name(member.display_name)
        if display_name_normalized in player_names:
            unmatched_names.discard(display_name_normalized)
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                    logging.info('%s+ Assigned %s%s%s role to %s%s', Fore.GREEN, Style.RESET_ALL, role_name, Fore.GREEN, Style.RESET_ALL, member.display_name)
                except discord.Forbidden:
                    logging.error('%s!! Permission denied assigning role to %s%s', Fore.RED, Style.RESET_ALL, member.display_name)
                except discord.HTTPException as e:
                    logging.error('%s!! Failed assigning role to %s%s: %s', Fore.RED, Style.RESET_ALL, member.display_name, e)
            else:
                logging.info('%s- %s%s%s already has the %s%s%s role.%s', Fore.BLUE, Style.RESET_ALL, member.display_name, Fore.BLUE, Style.RESET_ALL, role_name, Fore.BLUE, Style.RESET_ALL)

    if unmatched_names:
        for name in unmatched_names:
            logging.warning('%s~ Discord member: %s%s%s not found.%s', Fore.LIGHTYELLOW_EX, Style.RESET_ALL, name, Fore.LIGHTYELLOW_EX, Style.RESET_ALL)
