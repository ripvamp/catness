from __future__ import annotations

import discord
import psutil

from discord.ext import commands
from discord import app_commands

from cogs.events import start_time

from data import icons

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='about', description='thanks for checking on me!!')
    async def status(self, interaction):
        cmds = self.bot.tree.get_commands() or await self.bot.tree.fetch_commands()

        razy = self.bot.get_user(self.bot.owner_id or 592310159133376512) or await self.bot.fetch_user(self.bot.owner_id or 592310159133376512)

        embed = discord.Embed(title=str(self.bot.user))

        if len(self.bot.shards) > 20:
            shard_thing = f"Automatically sharded ~ `{len(self.bot.shards)}/{self.bot.shard_count}`"
        else:
            shard_thing = f"Automatically sharded ~ `{', '.join(str(i) for i in self.bot.shards.keys())}/{self.bot.shard_count}`"

        embed.description = f"""
        Hi i am discord bot for discord and real
        My prefix is `{self.bot.command_prefix}` and i support `/app commands`
        {shard_thing}
        """
        embed.set_thumbnail(url=self.bot.user.display_avatar.url)
        embed.add_field(name='owner', value=f'`deezerload#0`')
        embed.add_field(name='uptime',
                        value=f'<t:{int(start_time)}:R>',
                        inline=True)
        embed.add_field(name='total users',
                        value=f'`{len(self.bot.users)}`')
        embed.add_field(name='total guilds',
                        value=f'`{len(self.bot.guilds)}`')
        embed.add_field(name='d.py version',
                        value=f'`{discord.__version__}`')
        embed.add_field(name='cmd count',
                        value=f'`{len(cmds)}`')

        if interaction.user == razy:
            cpu_percent = psutil.cpu_percent()
            memory_usage = psutil.virtual_memory().percent

            embed.add_field(name="Usage", value=f"CPU: `{cpu_percent}%` | Mem: `{memory_usage}%`")

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(
            label='Invite', style=discord.ButtonStyle.link,
            url=f"https://discordapp.com/oauth2/authorize?client_id={self.bot.user.id}&scope=bot+applications.commands&permissions=1099511627775",
            emoji='<:grinning_face_smiling:1109581692819210311>')
        )
        view.add_item(discord.ui.Button(
            label="Source",
            url="https://github.com/razyness/catness",
            emoji=icons.github
        ))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))
