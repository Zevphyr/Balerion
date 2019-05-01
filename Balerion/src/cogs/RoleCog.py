from discord.ext import commands
from discord.utils import get


class RoleCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    async def cog_check(self, ctx):
        return ctx.message.channel.name == 'assign-yourself-ranks'

        # Error Handling
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You cant do that!")

# Roles
    @commands.command(name='role', brief='Assigns or removes roles')
    async def change_role(self, ctx, lang):
        lang = lang.lower()
        roles_dict = {'python': 572081414007423016, 'c++': 572081414007423016, 'java': 572081491291668481,
                      'web': 572081500875653150}
        if lang not in roles_dict:
            await ctx.send('Invalid role command passed or called in the wrong channel. Please try again...')
            print('fail')
        else:
            member = ctx.message.author
            guild = ctx.message.guild
            role = get(guild.roles, id=roles_dict[lang])
            have_role = True if role in member.roles else False
            if not have_role:
                await member.add_roles(role)
                status = 'added'
                await ctx.send('Congratulations, {} role has been {}!'.format(lang, status))
                print('added')
            elif have_role:
                await member.remove_roles(role)
                status = 'removed'
                await ctx.send('Congratulations, {} role has been {}!'.format(lang, status))
                print('removed')
            elif ctx.invoked_command is None:
                await ctx.send('Invalid role command passed. Please try again...')


def setup(bot):
    bot.add_cog(RoleCog(bot))
