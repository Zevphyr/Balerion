import discord
import sys, traceback
from discord.ext import commands



TOKEN = TOKEN  #This token is what allows the bot to run -- it's its own unique identifier. 
description = '''Write your description of the bot here'''

"when the help command is called, the description above will be at the top of the help message"

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
initial_extensions = ['cogs.owner',
                      'cogs.role',
                      'cogs.admin',
                      'cogs.members',
                      'cogs.resources']

# login
@bot.event
async def on_ready():
    print(f'\n\nLogged in as: {bot.user.name}\n{bot.user.id}\nVersion: {discord.__version__}\n') 
    # prints and formats the bot name, id, and version of discord being run on separate new lines
    print('------')
    await bot.change_presence(activity=discord.Game(name='The Black Dread'))
    # This changes the status of the bot to: "Playing The Black Dread"  

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


#  Here we load our extensions(cogs) listed above in [initial_extensions]. It prints out a traceback if for some reason it fails.
if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
            print('Loaded {}'.format(extension))
        except Exception as error:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

"""bot.run is a method for simplicity's sake. You could take the more complicated route and use bot.start() but then
you would have to remember to close the loop; if you go down that road I reccommend you familiarize yourself with the 
official Discord API."""
bot.run(TOKEN, bot=True, reconnect=True)
