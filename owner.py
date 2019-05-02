from discord.ext import commands


class OwnerCog(commands.Cog, name="Owner Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='test')
    async def test(self, ctx):
        print('success')
        await ctx.send.author('Success')


def setup(bot):
    bot.add_cog(OwnerCog(bot))