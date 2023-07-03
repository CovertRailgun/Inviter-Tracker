import disnake
from disnake.ext import commands

import settings

class Bot_Setup(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.log = settings.logging.getLogger('bot')

    @commands.slash_command()
    @commands.is_owner()
    async def z_cog(self, inter:disnake.ApplicationCommandInteraction) -> None:
        pass

    @z_cog.sub_command()
    async def reload(self, inter:disnake.ApplicationCommandInteraction, cog:str) -> None:
        self.log.info(f"reloading cogs.{cog.lower()}")
        self.bot.reload_extension(f"cogs.{cog.lower()}")
        await inter.response.send_message("reloaded!", ephemeral=True)
        self.log.info(f'done reloading {cog.lower()}')

    @z_cog.sub_command()
    async def load(self, inter:disnake.ApplicationCommandInteraction, cog:str) -> None:
        self.log.info(f"loading cogs.{cog.lower()}")
        self.bot.load_extension(f"cogs.{cog.lower()}")
        await inter.response.send_message("loaded!", ephemeral=True)
        self.log.info(f'done loading {cog.lower()}')

    @z_cog.sub_command()
    async def unload(self, inter:disnake.ApplicationCommandInteraction, cog:str) -> None:
        self.log.info(f"unloading cogs.{cog.lower()}")
        self.bot.unload_extension(f"cogs.{cog.lower()}")
        await inter.response.send_message("unloaded!", ephemeral=True)
        self.log.info(f'done unloading {cog.lower()}')
    
    async def cog_slash_command_error(self, inter:disnake.ApplicationCommandInteraction, error):
        self.log.info(f"error raised: {error}")
        if isinstance(error, commands.errors.NotOwner):
            await inter.response.send_message(f'Permission denied {error}', ephemeral=True)
        elif isinstance(error, commands.errors.CommandInvokeError):
            await inter.response.send_message(error, ephemeral=True)
        else:
            self.log.warning(f'cog loading error not handled, error raised is: {error}')
            raise error


def setup(bot: commands.Bot):
    bot.add_cog(Bot_Setup(bot))