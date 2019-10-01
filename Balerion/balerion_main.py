import discord
import sys, traceback
import logging
import asyncio
from Balerion.utils.dataIO import dataIO
from discord.ext import commands

try:
    import uvloop
except ImportError:  # uvloop not available on Windows
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

log = logging.getLogger('Balerion')


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

bot = commands.Bot(command_prefix=get_prefix, description=description)


class Balerion(commands.AutoShardedBot):
    def __init__(self):

        self.settings = dataIO.load_json("Balerion/Config/settings.json")

        super().__init__(command_prefix=get_prefix, description=description, case_insensitive=True)

        self.init_ok = False

        """Below cogs represents our folder our cogs are in. Following is the file name. So 'meme.py' in cogs, 
                would be cogs.meme

                Think of it like a dot path import"""

        initial_extensions = ['src.cogs.owner',
                              'src.cogs.role',
                              'src.cogs.admin',
                              'src.cogs.members',
                              'src.cogs.resources',
                              'src.cogs.music']

        #  Here we load our extensions(cogs) listed above in [initial_extensions].

        for extension in initial_extensions:
            try:
                self.load_extension(extension)
                print('Loaded {}'.format(extension))
            except Exception as error:
                print(f'Failed to load extension {extension}.', file=sys.stderr)
                traceback.print_exc()

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

    # login event

    async def on_ready(self):
        users = len(set(self.get_all_members()))
        servers = len(self.guilds)
        channels = len([c for c in self.get_all_channels()])
        print(f'\n\nLogged in as: {self.user.name}\n{self.user.id}\nVersion: {discord.__version__}\n')
        log.info(str(self.user))
        log.info("{} server{}".format(servers, 's' if servers > 1 else ''))
        log.info("{} shard{}".format(self.shard_count, 's' if self.shard_count > 1 else ''))
        log.info("{} channel{}".format(channels, 's' if channels > 1 else ''))
        log.info("{} users".format(users))
        print('------')
        self.init_ok = True
        await self.change_presence(activity=discord.Game(name='The Black Dread'))

    async def on_shard_ready(self, shard_id):
        log.info(f"Shard {shard_id} is ready")

    def run(self, *args, **kwargs):
        super().run(self.settings['TOKEN'], bot=True, reconnect=True)

