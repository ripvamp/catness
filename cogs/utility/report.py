import discord
import datetime
import aiohttp

from discord.ext import commands
from discord import app_commands


class ConfirmModal(discord.ui.Modal):
    def __init__(self, *, title: str = "Big bug report modal cool", timeout: float | None = 120, bot) -> None:
        super().__init__(title=title, timeout=timeout)
        self.bot = bot

    short = discord.ui.TextInput(
        style=discord.TextStyle.short,
        label="Describe briefly",
        required=True,
        max_length=100,
        placeholder="<command> says The application did not respond..."
    )

    long = discord.ui.TextInput(
        style=discord.TextStyle.long,
        label="Details / how to reproduce",
        required=True,
        max_length=4000,
        placeholder="When i press x button after y button it fails and like\nFeel free to use codeblocks if needed"
    )

    async def on_submit(self, interaction: discord.Interaction):
        embed = discord.Embed(title=self.short.value, description=self.long.value)
        embed.set_author(name="bug report")
        embed.set_footer(
            text=f"submitted by {str(interaction.user)} | {interaction.user.id}",
            icon_url=interaction.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()

        await interaction.response.send_message(f"Thank you!! While you wait, you can join support server real and maybe you can help me figure it out\nhttps://discord.gg/invitelink", ephemeral=True)

        webhook_url = "https://canary.discord.com/api/webhooks/1125181467937476658/RJitjrKZTKSNdx2LhUzzIz8OHD0zJn5HhK5m4Tzc0mctoYh3yVDsQVjUWO5G2FmYO6x_"

        async with aiohttp.ClientSession() as session:
            webhook = discord.Webhook.from_url(url=webhook_url, session=session)
            await webhook.send(embed=embed)


class Report(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name='report', description='Report silly issues and errors please')
    @app_commands.checks.cooldown(1, 86400, key=lambda i: (i.user.id))
    async def report(self, interaction):
        modal = ConfirmModal(bot=self.bot)
        await interaction.response.send_modal(modal)


async def setup(bot: commands.Bot):
    await bot.add_cog(Report(bot))
