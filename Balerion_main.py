import discord
import sys, traceback
import logging
import asyncio
from .Balerion.utils.dataIO import dataIO
from discord.ext import commands

log = logging.getLogger('Balerion')


class Balerion(commands.AutoShardedBot):
    def __init__(self):

        def get_prefix(bot, message):
            # A callable Prefix for our bot. This could be edited to allow per server prefixes.

            # You can use spaces in prefixes. Try to keep them simple though.
            prefixes = ['/', '! ', '?']

            # Check to see if we are outside of a guild. e.g DM's etc.
            if not message.guild:
            # Only allow ? to be used in DMs
                return '?'
            else:
            # If in a guild, allow for the user to mention the bot or use any of the prefixes in our list.
                return commands.when_mentioned_or(*prefixes)(bot, message)

        description = '''Balerion is a bot made for administrative aid in small discord guilds. Creator is "Zevphyr" \
        and the source for the bot can be found at: https://github.com/Zevphyr/Balerion/'''

        self.settings = dataIO.load_json("Config/settings.json")

        super().__init__(command_prefix=get_prefix, description=description, case_insensitive=True)

        self.init_ok = False

        # Member index

        def get_member(self, id):
            try:
                return [m for m in self.get_all_members() if m.id == id][0]
            except IndexError:
                return None

        # Error handling ||WIP||

        async def on_command_error(self, ctx, error):
            channel = ctx.channel
            can_send = channel.permissions_for(ctx.me).send_messages

            if isinstance(error, commands.MissingRequiredArgument) or isinstance(error, commands.BadArgument):
                if can_send:
                    log.info(f"{error}.. Sending help...")
                    return await ctx.send(f"```cs\n{error}```\n\nMaybe try to use ``{ctx.prefix}help {ctx.command}``")
                else:
                    log.info("Can't send help - Missing Permissions")
                    return

            elif isinstance(error, commands.errors.CheckFailure):
                if can_send:
                    return await ctx.channel.send("Sorry, you don't have enough permissions to use this command.",
                                      delete_after=10)
                else:
                    log.info("Can't send permissions failure message - Missing Permissions")
                    return

            elif isinstance(error, commands.CommandNotFound):
                return

            else:
                if isinstance(error, commands.CommandInvokeError):
                    if isinstance(error.original, discord.errors.Forbidden):
                        log.info("discord.errors.Forbidden: FORBIDDEN (status code: 403): Missing Permissions")
                        return
                    if isinstance(error.original, discord.errors.NotFound):
                        # log.info("discord.errors.NotFound: NotFound (status code: 404): Message not found")
                        return

            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)

            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

            log.error(f'Exception in command {ctx.command.name}: {error}')

        """Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, 
        would be cogs.meme
        
        Think of it like a dot path import"""

        initial_extensions = ['src.cogs.owner',
                              'src.cogs.role',
                              'src.cogs.admin',
                              'src.cogs.members',
                              'src.cogs.resources',
                              'src.cogs.music']

        # login event
        @Balerion.event
        async def on_ready():
            print(f'\n\nLogged in as: {Balerion.user.name}\n{Balerion.user.id}\nVersion: {discord.__version__}\n')
            print('------')
            await Balerion.change_presence(activity=discord.Game(name='The Black Dread'))

        # Removes the default help command
        # bot.remove_command('help')

        # If its hidden it won't turn up in the help command.
        @Balerion.group(hidden=True, brief='Loads and unloads a module, manually.')
        @commands.is_owner()
        async def modules(ctx):
            if ctx.invoked_subcommand is None:
                await ctx.send.author('That\'s not quite right')


        # Load Cogs
        @modules.command(name='load', hidden=True, brief='Command which Loads a module.')
        async def load(extension, ctx):
            try:
                Balerion.load_extension(extension)
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.send('**`SUCCESS`**')


        # Unload Cogs
        @modules.command(name='unload', hidden=True, brief='Command which Unloads a module.')
        async def unload(extension, ctx):
            """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

            try:
                Balerion.unload_extension(extension)
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.send('**`SUCCESS`**')


        # Reload Cogs
        @modules.command(name='reload', hidden=True, brief='Command which Reloads a Module.')
        async def cog_reload(extension, ctx):
            try:
                Balerion.unload_extension(extension)
                Balerion.load_extension(extension)
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')
            else:
                await ctx.send('**`SUCCESS`**')


        #  Here we load our extensions(cogs) listed above in [initial_extensions].
        if __name__ == '__main__':
            for extension in initial_extensions:
                try:
                    self.load_extension(extension)
                    print('Loaded {}'.format(extension))
                except Exception as error:
                    print(f'Failed to load extension {extension}.', file=sys.stderr)
                    traceback.print_exc()

        def run(self, *args, **kwargs):
            super(Balerion, self).run(self.settings['TOKEN'], bot=True, reconnect=True)
