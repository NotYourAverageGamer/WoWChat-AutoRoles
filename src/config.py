import os
from dotenv import load_dotenv

def load_config():
    load_dotenv('.env')

    try:
        config = {
            'SERVER_ID': int(os.getenv('SERVER_ID')),
            'ROLE_NAME': os.getenv('ROLE_NAME'),
            'CHANNEL_ID': int(os.getenv('CHANNEL_ID')),
            'WOWCHAT': os.getenv('WOWCHAT'),
            'WHO_INTERVAL_ENABLED': os.getenv('WHO_INTERVAL_ENABLED', 'False').lower() == 'true',
            'WHO_INTERVAL_HOURS': int(os.getenv('WHO_INTERVAL_HOURS', '6')),
            'DISCORD_TOKEN': os.getenv('DISCORD_TOKEN'),
        }
    except Exception as e:
        raise RuntimeError(f"Error loading configuration: {e}") from e

    for key, value in config.items():
        if value is None:
            raise RuntimeError(f"Missing required config value: {key}")

    return config
