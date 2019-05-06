import discord
from discord.ext import commands



class OwnerCog(commands.Cog, name="Info Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="Provides bot and author information")
    async def info(self, ctx):
        embed = discord.Embed(title="Balerion", description="A educational collaborative project. \
        Aids in administration, adds user interaction, provides music, and resources to learn from.   ", color=0xeee657)

    # give info about you here
        embed.add_field(name="Author", value="Zevphyr")

    # Shows the number of servers the bot is member of.
        embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}")

    # give users a link to invite this bot to their server
        embed.add_field(name="Invite", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=572165670901645352&permissions=334588935&scope=bot)")

    # provides a link to the GitHub repo
        embed.add_field(name="Contribute", value="[GitHub](https://github.com/Zevphyr/Balerion)")

        await ctx.send_typing
        await ctx.send("info", embed=embed)

def setup(bot):
    bot.add_cog(OwnerCog(bot))
