import discord
import aiosqlite
import time
import datetime

from data import Data
from discord import app_commands
from discord.ext import commands


class Rep(commands.Cog):
	def __init__(self, bot):
		super().__init__()
		self.bot = bot

	@app_commands.command(name="rep", description="Tatsu copied me")
	async def rep(self, inter, user:discord.User):
		if inter.user == user:
			await inter.response.send_message("You can't rep yourself! That'd be a little weird")
			return
		if user.bot:
			await inter.response.send_message("You can't rep bots! End of line")
			return

		async with aiosqlite.connect('data/data.db') as db:
			db.row_factory = aiosqlite.Row
			muser = await Data.load_db(table="rep", id=user.id)
			if muser is None:
				await db.execute("INSERT INTO rep (id, rep, time) VALUES (?, 0, 0)", (user.id,))
				await db.commit()
				muser = await Data.load_db(table="rep", id=user.id)
		
			ruser = await Data.load_db(table="rep", id=inter.user.id)
			if ruser is None:
				await db.execute("INSERT INTO rep (id, rep, time) VALUES (?, 0, 0)", (inter.user.id,))
				await db.commit()
				ruser = await Data.load_db(table="rep", id=inter.user.id)

			expiration_time = datetime.datetime.fromtimestamp(ruser['time']) + datetime.timedelta(hours=12)
			
			if expiration_time < datetime.datetime.now() or inter.user.id == 809275012980539453:
				await db.execute("UPDATE rep SET rep=? WHERE id=?", (muser['rep'] + 1, user.id))
				await db.execute("UPDATE rep SET time=? WHERE id=?", (int(time.time()), inter.user.id))
				await db.commit()
				await inter.response.send_message(f"You gave {user.mention} a reputation point!!")
			else:
				await inter.response.send_message(f"You don't have any reputation points left! Return <t:{int(datetime.datetime.timestamp(expiration_time))}:R>")



async def setup(bot):
	await bot.add_cog(Rep(bot))
