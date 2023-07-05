import asyncio
import random
import discord

from discord.ext import commands
from discord import app_commands

from data import Data as data

welcome_messages = [
	"Welcome, {user}! Get comfy and enjoy the company!",
	"Hey there, {user}! We've been waiting for you. Let's have some fun!",
	"Welcome aboard, {user}! Prepare for an adventure of a lifetime!",
	"Greetings, {user}! Grab a virtual snack and join the party!",
	"Buckle up, {user}! The excitement starts now!",
	"Welcome, {user}! Get ready to meet fantastic people!",
	"Hey, {user}! This server is all about good vibes and great times!",
	"Step right in, {user}! The fun train is about to depart!",
	"Welcome, {user}! Brace yourself for epic moments!",
	"Hey there, {user}! Prepare to be blown away by our awesome community!",
	"Welcome, {user}! Let's dive into the sea of endless conversations!",
	"Hey, {user}! We've saved you a spot in the laughter zone!",
	"Greetings, {user}! Your presence makes this server even more awesome!",
	"Welcome, {user}! Embrace the chaos and enjoy the ride!",
	"Hey there, {user}! Your arrival just made this server 10 times cooler!",
	"Welcome, {user}! You've joined a family of fantastic individuals!",
	"Welcome, {user}! Prepare to have your socks knocked off!",
	"Hey there, {user}! We're thrilled to have you join our community!",
	"Welcome aboard, {user}! Get ready for a wild ride filled with laughter!",
	"Greetings, {user}! You've just stepped into a realm of endless possibilities!",
	"Buckle up, {user}! Adventure awaits you in every corner of this server!",
	"Welcome, {user}! We're here to make memories and have a great time together!",
	"Hey, {user}! The party starts now. Let's create some unforgettable moments!",
	"Step right in, {user}! Prepare to be amazed by the incredible people here!",
	"Welcome, {user}! Get ready for a community that feels like home!",
	"Hey there, {user}! We're a bunch of friendly folks ready to welcome you with open arms!"
]

class WelcomeButton(discord.ui.View):
	def __init__(self, *, timeout=180):
		super().__init__(timeout=timeout)
		self.vaule = None
		self.msg = None
		self.reacted = []

	async def disable_all(self):
		for i in self.children:
			i.disabled = True
		
		if self.msg:
			await self.og_msg.edit(view=self)

	async def on_timeout(self) -> None:
		await self.disable_all()
		self.msg = None
		self.reacted = None

	@discord.ui.button(label="Say hi!", emoji=random.choice(["🌞", "🌻", "🌼", "🎉", "🎊", "🎇", "🎁", "📚", "📬", "💌", "🎶", "🎈", "🎄", "🕊️", "⭐", "🍀"]))
	async def wave(self, interaction, button):
		await interaction.response.defer()
		if self.msg is None:
			self.msg = await interaction.followup.send(f"{interaction.user.mention} said hi!")
		else:
			self.msg = await interaction.channel.fetch_message(self.msg.id)
			if interaction.user.id not in self.reacted:
				content = f"{interaction.user.mention}, {self.msg.content}"
				await self.msg.edit(content=content)
			else:
				await interaction.followup.send("You've already greeted this individual!! :)", ephemeral=True)
		if interaction.user.id not in self.reacted:
			self.reacted.append(interaction.user.id)

class Welcomer(commands.Cog):
	def __init__(self, bot: commands.Bot):
		self.bot = bot

	@commands.Cog.listener("on_member_join")
	async def welcomer(self, member):
		if member.bot:
			return
		
		server_data = await data.load_db(table="servers", id=str(member.guild.id), columns=["welcomer"])
		if not server_data["welcomer"] > 0:
			return

		patterns = ["gen", "main", "chat"]
		channel = next((channel for channel in member.guild.text_channels if any(name.lower() in channel.name.lower() for name in patterns)), None)
		view = WelcomeButton() if server_data["welcomer"] > 1 else None

		if channel:
			og_msg = await channel.send(random.choice(welcome_messages).replace("{user}", member.mention), view=view)

			if server_data["welcomer"] > 1:
				view.og_msg = og_msg

				await asyncio.sleep(180)
				if view.reacted == [] or view.reacted is None:
					await og_msg.delete()
				else:
					await view.on_timeout()

async def setup(bot: commands.Bot):
	await bot.add_cog(Welcomer(bot))
