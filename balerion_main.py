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
def role_channel():  # Create decorator
    def predicate(ctx):
        ch = ctx.message.channel
        if ch == 12324234183172:
            return True
    return commands.check(predicate)


roles_dict = {'python': 572081414007423016, 'c++': 572081414007423016, 'java': 572081491291668481,
              'web': 572081500875653150}


# administrative group
@bot.group(name='su', brief='This is for administrative commands', description='These commands are unable to \
                                                to be used if your role does not have administrator privileges')
@commands.has_permissions(administrator=True)  # Restricts command to administrators
async def su(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid su command passed...')

#
@su.command(name='purge', brief='Purges old messages', description='purges up to 100 messaged made within the \
                                                                                                last 14 days')
async def clean(ctx, limit: int):
    await ctx.channel.purge(limit=limit, bulk=True)
    await ctx.send('Cleared by {}'.format(ctx.author.mention))
    await ctx.message.delete()


@su.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
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
@bot.command(name='role', brief='Assigns or removes roles')
@role_channel()
# Error handling
async def clear_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You cant do that in this channel!")


async def change_role(ctx, lang):
    lang = lang.lower()
    if lang not in roles_dict:
        await ctx.send('Invalid role command passed or called in the wrong channel. Please try again...')
        print('fail')
    else:
        member = ctx.message.author
        guild = ctx.message.guild
        role = get(guild.roles, id=roles_dict[lang])
        have_role = True if role in member.roles else False
        if not have_role:
            await member.add_roles(role)
            status = 'added'
            await ctx.send('Congratulations, {} role has been {}!'.format(lang, status))
            print('added')
        elif have_role:
            await member.remove_roles(role)
            status = 'removed'
            await ctx.send('Congratulations, {} role has been {}!'.format(lang, status))
            print('removed')
        elif ctx.invoked_command is None:
            await ctx.send('Invalid role command passed. Please try again...')

bot.run(TOKEN)
