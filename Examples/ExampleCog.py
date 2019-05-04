from discord.ext import commands

"""The __init__ function is called a constructor, or initializer, 
and is automatically called when you create a new instance of a class. You need this to
initialize the cog otherwise, you will not be able to call and use it."""

#The cog class contains all of our commands and events as methods.
class Test(commands.Cog, name="Test Commands"):
    def __init__(self, bot):
        self.bot = bot

"""
When objects are instantiated, the object itself is passed into the self parameter. 
Because of this, the object’s data is bound to the object; The Object is passed into 
the self parameter so that the object can keep hold of its own data.
"""

"""
Replace bot.command with commands.command 
(commands being from discord.ext import commands, which is why we import it at the beginning.)
"""
    @commands.command(name='test')
    async def test(self, ctx):  # include self at the beginning, as all of your commands and events are now methods of the cog class
        print('success')
        await self.bot.say('Success')  # all references of bot should be changed to self.bot


""" 
Just about all setup functions look the same:

def setup(bot):
    bot.add_cog(Cog(bot))

where Cog is the cog class.
 """

def setup(bot):
    bot.add_cog(Test(bot))