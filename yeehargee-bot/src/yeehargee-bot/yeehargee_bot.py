from argparse import Namespace
# import asyncio
import coloredlogs, logging

import discord
from typing_extensions import Self

logger = logging.getLogger(__name__)
coloredlogs.install(level='DEBUG', logger=logger, isatty=True)
logging.basicConfig(level=logging.DEBUG)

class YeehargeeBot(discord.Client):
    bot: YeehargeeBot = None
    # def __init__(self, intents) -> None:
    #     super().__init__(self, intents)
    #     return

    @classmethod
    def _get_new_bot(cls) -> Self:
        """create singleton"""
        logger.info('created bot')
        logger.debug('testing color')
        print('yeehargee matey!')
        # self.setup(args)
        intents = discord.Intents.default()
        intents.members = True
        intents.message_content = True
        cls.bot = YeehargeeBot(intents=intents)  # singleton?
        return cls.bot

    @classmethod
    def get_bot(cls) -> Self:
        """get singleton instance"""
        return cls.bot if cls.bot is not None else cls._get_new_bot()

    @classmethod
    def main(cls, args) -> int:
        """Main entry point to entire program"""
        cls.bot = cls.get_bot()
        cls.bot.setup(args).run(args.token)

        return 0
    
    def setup(self, args: Namespace) -> Self:
        """Set up basic functionality to be appended to later"""
        return self

    async def on_ready(self):
        """on_ready interface implementation"""
        print(f'Logged in as {self.user}!')
        return

    async def on_message(self, message):
        """on_message interface implementation"""
        print(f'Message from {message.author}: {message.content}')
