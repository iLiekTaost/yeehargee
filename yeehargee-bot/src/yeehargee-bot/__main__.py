from argparse import Namespace
import sys

from .cli import parse_cli
from . import YeehargeeBot

if __name__ == '__main__':
    args = parse_cli()
    bot = YeehargeeBot.get_bot()
    sys.exit(bot.main(args))
