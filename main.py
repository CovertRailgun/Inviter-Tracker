import os

import disnake
from disnake.ext import commands

import settings


class bot(commands.InteractionBot):
    log = settings.logging.getLogger('bot')


    async def on_ready(self) -> None:
        self.log.info(f"User: {self.user} (ID: {self.user.id})")    

if __name__ == '__main__':

    Pearl = bot(
        intents=disnake.Intents.all(),
        asyncio_debug=True,
        )
    Pearl.load_extensions("cogs")


    Pearl.run(settings.DISCORD_PEARL_TOKEN)
