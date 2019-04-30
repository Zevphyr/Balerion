import discord
import typing
from discord.ext import commands
from discord.utils import get

TOKEN = TOKEN
description = '''Balerion is a bot made for administrative aid in small discord guilds. Creator is "Zevphyr" \
 and the source for the bot can be found at: https://github.com/Zevphyr/Balerion/'''

bot = commands.Bot(command_prefix='/', description=description)

# login
@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    await bot.change_presence(activity=discord.Game(name='The Black Dread'))
    
    
# Globals
def role_channel():  # Creates own decorator
    def predicate(channel):
        channel = bot.get_channel(12324234183172)  # Retrieves channel id from guild
    return commands.check(predicate)

# administrative group
@bot.group(name='su', brief='This is for administrative commands', description='These commands are unable to \
                                                to be used if your role does not have administrator privileges')
@commands.has_permissions(administrator=True)  # Restricts command to administrators
async def su(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid su command passed...')


@su.command(name='purge', brief='Purges old messages', description='purges up to 100 messaged made within the \
                                                                                                last 14 days')
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit, bulk=True)
    await ctx.send('Cleared by {}'.format(ctx.author.mention))
    await ctx.message.delete()


@su.error # Error event
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions): # Missing permissions
        await ctx.send("You cant do that!")


# ban

@su.command(name='ban', brief='Bans users', description=' Requires 2 args minimum; The command can ban multiple \
    users at once. Usage is as follows /su ban @user1, @user2[optional], @user3[and so on], [reason for ban], \
     delete_days[optional]')
async def ban(ctx, members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0, *,
              reason: str):
    for member in members:
        await member.ban(delete_message_days=delete_days, reason=reason)
    else:
        await ctx.send("You don't have permission to use this command.")
      
      
# Kick
@su.command(name='kick', brief='Kicks users', description=' Requires 2 args minimum; The command can Kick multiple \
    users at once. Usage is as follows /su ban @user1, @user2[optional], @user3[and so on], [reason for kick], \
     delete_days[optional]')
async def kick(ctx, members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0, *,
              reason: str):
    for member in members:
        await member.kick(delete_message_days=delete_days, reason=reason)
    else:
        await ctx.send("You don't have permission to use this command.")
      

# Roles
@bot.group(name='roles', brief='This is for role commands', description='Individuals may assign any of the listed \
                                roles.')
@role_channel()
async def roles(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid role command passed. Please try again...')
    
    
@roles.error  # Error handling
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):  # role_channel
        await ctx.send("You cant do that in this channel!")


@roles.command(name='a-python', brief='Assigns the Python role')
async def add_py(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being assigned
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the Python role!")
        await member.add_roles(role)
        for member in guild.members:  # sends dm to member being assigned the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the Python role!")
                break


@roles.command(name='r-python', brief='Removes the Python role')
async def remove_py(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being removed
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the Python role!")
        await member.remove_roles(role)
        for member in guild.members:  # sends dm to member being removed from the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the Python role!")
                break


@roles.command(name='a-c++', brief='Assigns the C++ role')
async def add_c_plus(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being assigned
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the C++ role!")
        await member.add_roles(role)
        for member in guild.members:  # sends dm to member being assigned the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the C++ role!")
                break


@roles.command(name='r-c++', breif='Removes the C++ role')
async def remove_c_plus(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being removed
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the C++ role!")
        await member.remove_roles(role)
        for member in guild.members:  # sends dm to member being removed from the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the C++ role!")
                break


@roles.command(name='a-java', brief='Assigns the Java role')
async def add_java(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being assigned
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the Java role!")
        await member.add_roles(role)
        for member in guild.members:  # sends dm to member being assigned the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the Java role!")
                break


@roles.command(name='r-java', brief='Removes the Java role')
async def remove_java(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being removed
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the Java role!")
        await member.remove_roles(role)
        for member in guild.members:  # sends dm to member being removed from the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the Java role!")
                break


@roles.command(name='a-web', brief='Assigns the Web Developer role')
async def add_web(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being assigned
    if role in member.roles:
        await ctx.send('Silly human, you already have that role...')
    else:
        await ctx.send("Congratulations, you now have the Html/CSS/JS role!")
        await member.add_roles(role)
        for member in guild.members:  # sends dm to member being assigned the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have the Html/CSS/JS role!")
                break


@roles.command(name='r-web', brief='Removes the Web Developer role')
async def remove_web(ctx):
    member = ctx.message.author
    guild = ctx.message.guild
    role = get(guild.roles, id=id)  # replace id with the id of the discord role being removed
    if role not in member.roles:
        await ctx.send('Silly human, you don\'t have that role...')
    else:
        await ctx.send("Congratulation, you now have been removed from the Html/CSS/JS role!")
        await member.remove_roles(role)
        for member in guild.members:  # sends dm to member being removed from the role
            if role in member.roles:
                await ctx.author.send("Congratulation, you now have been removed from the Html/CSS/JS role!")
                break


bot.run(TOKEN)
