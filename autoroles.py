import re, discord

DISCORD_BOT_TOKEN = 'YourTokenHere' # Replace with your bots token
GUILD_ID = YourServerID  # Replace with your server ID
CHANNEL_ID = YourChannelID  # Replace with your channel ID where the `?who` command is issued
ROLE_NAME = 'YourRoleName'  # Replace with the role name you want to assign
WOWCHAT = 'YourWowChatBotName' # Username of bot that REPLIES to the `?who` command (without #1234)

intents = discord.Intents.default()
intents.message_content = True  # Enable message content intent
intents.members = True  # Enable privileged members intent

client = discord.Client(intents=intents)

async def parse_and_assign_roles(message_content):
    # Extract player names from the message content using regex
    player_names = re.findall(r'\b[A-Za-z]+(?:\s[A-Za-z]+)*(?=\s\()', message_content)
    if not player_names:
        print("No player names found in the message content.")
        return

    print(f"\nParsed player names: {player_names}")

    guild = client.get_guild(GUILD_ID)
    if not guild:
        print(f"Guild with ID {GUILD_ID} not found.")
        return

    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    if not role:
        print(f"Role '{ROLE_NAME}' not found in the server.")
        return

    for member in guild.members:
        if member.nick in player_names or member.name in player_names:
            if role not in member.roles:
                try:
                    await member.add_roles(role)
                    print(f"Assigned {ROLE_NAME} role to {member.display_name}")
                except discord.Forbidden:
                    print(f"Permission denied to assign role to {member.display_name}")
                except discord.HTTPException as e:
                    print(f"Failed to assign role to {member.display_name}: {e}")
            else:
                print(f"{member.display_name} already has the {ROLE_NAME} role.")

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    if not client.get_channel(CHANNEL_ID):
        print(f"Channel with ID {CHANNEL_ID} not found.")
        await client.close()
        return

    # Sending the ?who command
    await client.get_channel(CHANNEL_ID).send('?who')

@client.event
async def on_message(message):
    if message.author.name == WOWCHAT and message.channel.id == CHANNEL_ID:
        if re.match(r'^Currently \d+ guildies online:', message.content):
            await parse_and_assign_roles(message.content)

client.run(DISCORD_BOT_TOKEN)
