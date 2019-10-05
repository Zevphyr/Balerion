import discord
from discord.ext import commands


class ListenersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # New member join

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """ Welcome new user in the introduce-yourself channel and prompt to join the assign-yourself-ranks channel """

        introduce_yourself_channel = discord.utils.get(self.bot.get_all_channels(), name='introduce-yourself')
        assign_ranks_channel = discord.utils.get(self.bot.get_all_channels(), name='assign-yourself-ranks')
        welcome_string = f'Welcome {member.mention}! Please provide a brief introduction here and visit \
    <#{assign_ranks_channel.id}> to specify the programming language(s) you are interested in.'

        await introduce_yourself_channel.send(welcome_string)


def setup(bot):
    bot.add_cog(ListenersCog(bot))