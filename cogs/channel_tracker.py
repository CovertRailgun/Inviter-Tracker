import pathlib
import json

import disnake
from disnake.ext import commands, tasks

import settings



class invite_tracker(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.log = settings.logging.getLogger('bot')
        self.guild_id = 1122681690683347047
        self.invites = []
        self.location = pathlib.Path(settings.BASE_DIR / 'saved_data' / 'who_invited_member.json')
        self.n = 0

    async def cog_load(self) -> None:
            self.get_invites.start()
            self.log.info("started invite tracker loop")

    def cog_unload(self) -> None:
            self.get_invites.stop()
            self.log.info("stopped invite tracker loop")

    @tasks.loop(seconds=5)
    async def get_invites(self) -> None:
        self.n += 1
        guild = self.bot.get_guild(self.guild_id)
        self.invites = await guild.invites()
        self.log.info(f"updated invites {self.n}") 

    @get_invites.before_loop
    async def before_get_invites(self) -> None:
        self.log.info("delaying loading get_invite loop")
        await self.bot.wait_until_ready()

    def find_invite_by_code(self, invite_list:disnake.Guild.invites, code:disnake.Invite.code) -> disnake.invite:
        self.log.info("finding invite by code")
        for invite in invite_list:
            if invite.code == code:
                return invite

    async def update_join_list(self, member:disnake.member) -> None:
        self.log.info("Starting update_join_list")
        with open(self.location, "r+") as file:
            who_invited = json.load(file)
            if member.id in who_invited:
                who_invited[member.id] += 1
            else:
                who_invited[member.id] = 1
            file.seek(0)
            json.dump(who_invited, file, indent=4) 
        self.log.info("Finished update_join_list")

    @commands.Cog.listener()
    async def on_member_join(self, member) -> None:
        self.log.info("member joined")
        invites_after_join = await member.guild.invites()

        for invite in self.invites:
            if invite.uses < self.find_invite_by_code(invites_after_join, invite.code).uses:
                await self.update_join_list(invite.inviter)
                self.invites = invites_after_join
                self.log.info("finished adding join to inviters count")
                return None

    @commands.Cog.listener()
    async def on_member_remove(self, member:disnake.member):
        self.log.info("member left")
        self.invites = await member.guild.invites()

def setup(bot: commands.Bot):
    bot.add_cog(invite_tracker(bot))