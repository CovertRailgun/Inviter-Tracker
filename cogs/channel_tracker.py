import json
import pathlib
import datetime

import disnake
from disnake.ext import commands, tasks


import settings


class test(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.location = pathlib.Path(settings.BASE_DIR / 'saved_data' / 'who_invited_n.json')
        self.log = settings.logging.getLogger('bot')
        self.channel_id = 1062547302885105866

    @commands.slash_command()
    async def morning(self, inter) -> None:
        await inter.response.send_message(
            "Let us know what pokemon you would like see hosted in\nScarlet & Violet by using my /request_pokemon command.\nPokemon with enough votes will be added to the filters in\nRaidcrawler. This command can only be used once a day\nbut you are able to vote for the same Pokemon more than once."
        )
        

def setup(bot: commands.Bot):
    bot.add_cog(test(bot))