import time

from discord.ext import commands
from discord import app_commands


class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='ping', description='View bot\'s latency')
    async def ping(self, interaction):
        before = time.monotonic()
        await interaction.response.send_message("Pinging...", ephemeral=True)
        ping = (time.monotonic() - before) * 1000
        await interaction.edit_original_response(content=f"Pong! `{int((ping + self.bot.latency) / 2)} ms`")

async def setup(bot: commands.Bot):
    await bot.add_cog(Ping(bot))
