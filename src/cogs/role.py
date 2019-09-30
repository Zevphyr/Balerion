from discord.ext import commands
from discord.utils import get


class RoleCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.channel.name == 'assign-yourself-ranks'


# Roles
    @commands.command(name='role', case_insensitive=True, brief='Assigns or removes roles')
    async def change_role(self, ctx, lang):
        lang = lang.lower()
        roles_dict = {'python': 572081414007423016, 'c-family': 572081460740227072, 'java': 572081491291668481,
                      'web': 572081500875653150, 'query': 572645146886144052}
        if lang not in roles_dict:
            await ctx.send('Invalid role command passed or called in the wrong channel. Please try again...')
            print('fail')
        else:
            try:
                member = ctx.message.author
                guild = ctx.message.guild
                role = get(guild.roles, id=roles_dict[lang])
                have_role = True if role in member.roles else False
                if not have_role:
                    await member.add_roles(role)
                    status = 'added'
                    await ctx.send('Congratulations, {} role has been {}!'.format(lang, status))
                    print('Role Added')
                elif have_role:
                    await member.remove_roles(role)
                    status = 'removed'
                    await ctx.send('Congratulations, {} role has been {}!'.format(lang, status))
                    print('Role Removed')
                elif ctx.invoked_command is None:
                    await ctx.send('Invalid role command passed. Please try again...')
            except Exception as error:
                if isinstance(error, commands.CheckFailure):
                    print('R-FAIL')
                    await ctx.send("You cant do that!")


def setup(bot):
    bot.add_cog(RoleCog(bot))
