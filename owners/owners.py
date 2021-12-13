import re
import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import psutil


class Owners(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_member_update(self, before, after):
		if str(before.activity) == str(after.activity):
			return

		guild = self.bot.get_guild(645753561329696785)

		if after in guild.members:
			if re.search(r'\bdiscord.gg/dank\b', str(after.activity)):
				role = guild.get_role(916271809333166101)
				if role in after.roles:
					return
				await after.add_roles(role)

			else:
				role = guild.get_role(916271809333166101)
				if role not in after.roles:
					return

				await after.remove_roles(role)

	@commands.command()
	async def usage(self, ctx):
		await ctx.send(f'RAM memory % used: {psutil.virtual_memory()[2]}')
		await ctx.send(f'The CPU % usage is: {psutil.cpu_percent(4)}')

	@commands.command()
	async def dm(self, ctx, user: discord.Member, *, message):
		await user.send(f'Message from Bot Owner: {message}')
		await ctx.channel.send("Sent the message")

	@commands.command(aliases=['logoff'])
	async def shutdown(self, ctx):
		await ctx.send(f"Shutdown the bot?? (y/n)")
		msg = await self.bot.wait_for("message",
									  check=lambda m: m.author == ctx.author and m.channel.id == ctx.channel.id)
		if msg.content.lower() in ("y", "yes"):
			await ctx.send("Ugh bye now")
			await self.bot.close()
		else:
			await ctx.send("Okay bro wyd here then?")

	async def cog_check(self, ctx):
		return ctx.channel.permission_for(ctx.author).manage_guild


def setup(bot):
	bot.add_cog(Owners(bot))
