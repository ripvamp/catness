import toml
import aiohttp
from discord.ext import commands
from discord import app_commands

from data import config

TENOR = config["TENOR"]

class Reaction(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@app_commands.command(name='reaction', description='Live slug reaction')
	async def reaction(self, interaction):
		try:
			async with aiohttp.ClientSession() as session:
				async with session.get(f"https://tenor.googleapis.com/v2/search?q=live-reaction&key={TENOR}&client_key=tenor-api&limit=50&random=true") as response:
					result = await response.json()
					result = result["results"][0]["itemurl"]
			await interaction.response.send_message(result)
		except Exception as e:
			print(e)
	
async def setup(bot):
	await bot.add_cog(Reaction(bot))
