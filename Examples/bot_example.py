import discord
from discord.ext import commands

"""
Bot is an extended version of Client (it's in a subclass relationship). 
Ie. it's an extension of Client with commands enabled, thus the name of the subdirectory ext/commands.

The Bot class inherits all the functionalities of Client, 
which means that everything you can do with Client, Bot can do it too. 
"""

bot = commands.Bot(command_prefix='>')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run('token')