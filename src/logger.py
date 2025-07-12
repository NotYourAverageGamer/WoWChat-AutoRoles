import logging
from colorama import init, Fore, Style

def setup_logger():
    init()
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
