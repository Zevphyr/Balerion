import discord
import typing
from discord.ext import commands
from discord.utils import get

TOKEN = TOKEN
description = '''Balerion is a bot made for administrative aid in small discord guilds.'''

bot = commands.Bot(command_prefix='/', description=description)

# login
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='The Black Dread'))

''''# administrative group
@bot.group(name='su')
description = "Group of privileged commands"
async def su(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid su command passed...')


# ban

@su.command(name='ban')
@commands.has_role(id)
async def ban(ctx, members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0, *,
              reason: str):
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)
    else:
        await ctx.send("You don't have permission to use this command.")'''

# Roles
@bot.group(name='roles')
async def roles(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid role command passed. Please try again...')


@roles.command(name='-a python')
async def add_py(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the Python role!")
        await member.add_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the Python role!")
                break

@roles.command(name='-r python')
async def remove_py(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the Python role!")
        await member.remove_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the Python role!")
                break

roles.command(name='-a c++')
async def add_c_plus(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the C++ role!")
        await member.add_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the C++ role!")
                break

@roles.command(name='-r c++')
async def remove_c_plus(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the C++ role!")
        await member.remove_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the C++ role!")
                break

roles.command(name='-a java')
async def add_java(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the Java role!")
        await member.add_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the Java role!")
                break

@roles.command(name='-r java')
async def remove_java(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the Java role!")
        await member.remove_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the Java role!")
                break

roles.command(name='-a web')
async def add_web(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the Html/CSS/JS role!")
        await member.add_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the Html/CSS/JS role!")
                break

@roles.command(name='-r web')
async def remove_web(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the Html/CSS/JS role!")
        await member.remove_roles(role)
        for member in guild.members:
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the Html/CSS/JS role!")
                break


bot.run(TOKEN)
