from discord.ext import commands
import discord


class OwnerCog(commands.Cog, name="Info Commands"):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def info(self, ctx):
        embed = discord.Embed(title="Balerion", description="A educational collaborative project. \
        Aids in administration, adds user interaction, provides music, and resources to learn from.   ", color=0xeee657)
        # Author information
        embed.add_field(name="Author", value="Zevphyr")
        # Shows the number of servers the bot is member of.
        embed.add_field(name="Server count", value=f"{len(self.bot.guilds)}")
        # give users a link to invite this bot to their server
        embed.add_field(name="Click Here", value="[Invite link](https://discordapp.com/api/oauth2/authorize?client_id=572165670901645352&permissions=334588935&scope=bot)")
        # provides a link to the GitHub repo
        embed.add_field(name="Contribute", value="[GitHub](https://github.com/Zevphyr/Balerion)")
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(OwnerCog(bot))