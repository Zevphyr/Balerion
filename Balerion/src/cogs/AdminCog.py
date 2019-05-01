import discord
import typing
from discord.ext import commands


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


# administrative group
    @commands.group(name='su', brief='This is for administrative commands', description='These commands are unable to \
                                                to be used if your role does not have administrator privileges')
    @commands.has_permissions(administrator=True)  # Restricts command to administrators
    async def su(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid su command passed...')

# Purge
    @su.command(name='purge', brief='Purges old messages', description='purges up to 100 messaged made within the \
                                                                                                last 14 days')
    async def clean(self, ctx, limit: int):
        await ctx.channel.purge(limit=limit, bulk=True)
        await ctx.send('Cleared by {}'.format(ctx.author.mention))
        await ctx.message.delete()

# Error Handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that!")


# ban

    @su.command(name='ban', brief='Bans users', description=' Requires 2 args minimum; The command can ban multiple \
    users at once. Usage is as follows /su ban @user1, @user2[optional], @user3[and so on], [reason for ban], \
     delete_days[optional]')
    async def ban(self, ctx, members: commands.Greedy[discord.Member],
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
    async def kick(self, ctx, members: commands.Greedy[discord.Member],
              delete_days: typing.Optional[int] = 0, *,
              reason: str):
        for member in members:
            await member.kick(delete_message_days=delete_days, reason=reason)
        else:
            await ctx.send("You don't have permission to use this command.")


def setup(bot):
    bot.add_cog(AdminCog(bot))
