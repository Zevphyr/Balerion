import discord
import sys, traceback
from discord.ext import commands



TOKEN = TOKEN
description = '''Balerion is a bot made for administrative aid in small discord guilds. Creator is "Zevphyr" \
 and the source for the bot can be found at: https://github.com/Zevphyr/Balerion/'''


def get_prefix(bot, message):
    # A callable Prefix for our bot. This could be edited to allow per server prefixes.

    # You can use spaces in prefixes. Try to keep them simple though.
    prefixes = ['/', '! ', '?']

    # Check to see if we are outside of a guild. e.g DM's etc.
    if not message.guild:
        # Only allow ? to be used in DMs
        return '?'

    # If in a guild, allow for the user to mention the bot or use any of the prefixes in our list.
    return commands.when_mentioned_or(*prefixes)(bot, message)


bot = commands.Bot(command_prefix=get_prefix, description=description)


# Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, would be cogs.meme
# Think of it like a dot path import
initial_extensions = ['src.cogs.owner',
                      'src.cogs.role',
                      'src.cogs.admin',
                      'src.cogs.members',
                      'src.cogs.resources',
                      'src.cogs.reddit']

# login
@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name}\n{bot.user.id}\nVersion: {discord.__version__}\n')
    print('------')
    await bot.change_presence(activity=discord.Game(name='The Black Dread'))


# Removes the default help command
bot.remove_command('help')
    
    
# If its hidden it won't turn up in the help command.
@bot.group(name="Cogs", hidden=True, brief='Loads and unloads a module manually.')
@commands.is_owner()
async def modules(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send.author('That\'s not quite right')


# Load Cogs
@modules.command(name='load', hidden=True, brief='Command which Loads a module.')
async def load(extension, *, ctx):
    try:
        bot.load_extension(extension)
    except Exception as e:
        await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')



# Unload Cogs
@modules.command(name='unload', hidden=True, brief='Command which Unloads a module.')
async def unload(extension, *, ctx):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            bot.unload_extension(extension)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
        else:
            await ctx.send('**`SUCCESS`**')


# Reload Cogs
@modules.command(name='reload', hidden=True, brief='Command which Reloads a Module.')
async def cog_reload(extension, *, ctx):
    try:
        bot.unload_extension(extension)
        bot.load_extension(extension)
    except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
    else:
        await ctx.send('**`SUCCESS`**')


#  Here we load our extensions(cogs) listed above in [initial_extensions].
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()


bot.run(TOKEN, bot=True, reconnect=True)
