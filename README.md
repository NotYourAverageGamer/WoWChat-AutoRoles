# Autoroles integration for WoWChat/AscensionChat

This script integrates with WoWChat/AscensionChat to automatically assign roles to Discord server members based on their character names in the `?who` reply.

> [!NOTE]
> In-game and Discord Nicknames must match for this to work.

## 📖 How it Works

The script uses the `discord.py` library to interact with the Discord API. It sends a `?who` command to the specified channel, which triggers the WoWChat/AscensionChat bot to respond with a list of currently online guild members. The script then extracts the character names using regular expressions (regex) and assigns the specified role to Discord server members with matching names. It will then continue to monitor the specified channel while running. If anyone sends a `?who` command in the monitored channel, this bot will once again parse the response and assign roles to those without the role already.

## 🛠️ Setup

### Create the Discord Bot

1. Go to the [**Discord Developer Portal**](https://discord.com/developers/applications) and create a new app/bot
2. Click the `Bot` tab on the left side.
3. Copy your bot `TOKEN`. _(You might need to reset it first)_
4. Disable `Public Bot`.

> [!IMPORTANT]<br>5. Under `Privileged Gateway Intents`: Enable `Server Members Intent` and `Message Content Intent`.
> <br>
>
>   <details>
>   <summary><i>(click)</i> <b>Intents Example</b></summary>
>   <img src="images/1_intents.png" width="800"/>
>   </details>
> <b>Without these enabled the bot will not work!</b>

6. To skip steps 7-9:

- Copy this link, making sure to replace `YOUR_CLIENT_ID` with your bot's client ID. Open the link in your browser to invite the bot.

  ```https
  https://discord.com/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=268503040&integration_type=0&scope=bot
  ```

### OAuth2

7. Go to the `OAuth2` tab and select `bot` under `OAuth2 URL Generator -> Scopes`

   <details>
   <summary><i>(click)</i> <b>oAuth2 Example</b></summary>
   <img src="images/2_oAuthGen.png" width="650"/>
   </details>

### Permissions

> [!IMPORTANT]<br>8. Underneath `Scopes`, in `Bot Permissions` select: `Manage Roles`, `Send Messages` and `Read Message History`.
> <br>
>
>   <details>
>   <summary><i>(click)</i> <b>Bot Perms Example</b></summary>
>   <img src="images/3_bot_perms.png" width="650"/>
>   </details>
> <b>Make sure these are correct! Incorrect permissions will cause issues with the bot's functions!</b>

9. Copy the generated URL and open it in a browser. You can now invite the bot to your Discord Server.

## 💻 Dependencies

### Install Required Packages

1. Install [**Python**](https://www.python.org/downloads/) 3.8 or higher, if you don't have it installed already.
2. Open your terminal and navigate to the WoWChat-AutoRoles directory.
3. Run the following command to install (or update if you already have) the dependencies `discord.py`, `python-dotenv` and `colorama`:

   ```terminal
   pip install -U -r requirements.txt
   ```

## 🔧 Configuration

### Configure the Script

1. Open `CONFIG.env` in your favorite text editor.
2. `WHO_INTERVAL_ENABLED` Set `True` or `False` depending on if you want the bot to auto send `?who` at a specified interval. Default is false.
3. `WHO_INTERVAL_HOURS` Set how often (in hours) the bot should send the `?who` command, if set to `True` above
4. Replace `YourTokenHere` with your Discord bot token.
5. Replace `YourServerId` with your Discord server ID.
6. Replace `YourChannelID` with the Channel ID of the channel this bot will monitor for the `?who` command.
7. Replace `YourRoleName` with the name of the role you want the bot to assign.
8. Replace `YourWowChatBotName` with the name of your WoWChat/AscensionChat bot. _(your bot that replies to the `?who` command)_
9. Save your config changes and rename `CONFIG.env` to just `.env`.

## 🚀 Run

### Run the Script

1. Open your terminal and `cd` into the `src` directory that `autoroles.py` is saved in. (eg, `cd ~/Downloads/WoWChat-AutoRoles/src`)
2. Run the script using Python:
   - Linux/MacOS: `python3 autoroles.py`
   - Windows: `python.exe autoroles.py`
