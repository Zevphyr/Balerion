from discord.ext import commands

py_resources = []
js_resources = []

# initializes the cog
class ResourceCog(commands.Cog, name='Resource Commands'):


    def __init__(self, bot):
        self.bot = bot # all functions require the 'self' parameter

    @commands.command(name='addpython', brief='adds a Python resource to a resource list')
    async def add_py_resources(self, ctx):
        try:   # if you wanna get a b it fancy with error handling
            resource = ctx.message.content.replace('/addpython', '')
            py_resources.append(resource)
            await ctx.message.channel.send(f"Thank you, '{resource}' has been added to Python resources :)")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')


    @commands.command(name='pythonresources', brief='send a list of currently stored Python resources')
    async def get_py_resources(self, ctx):
        try:
            await ctx.message.author.send('CURRENTLY STORED PYTHON RESOURCES ARE:')
            for resource in py_resources:
                await ctx.message.author.send(resource)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')


    @commands.command(name='addjs', brief='add a Javascript resource to a resource list')
    async def add_js_resources(self, ctx):
        try:
            resource = ctx.message.content.replace('/addjs', '')
            js_resources.append(resource)
            await ctx.message.channel.send(f"Thank you, '{resource}' has been added to Javascript resources :)")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')


    @commands.command(name='jsresources', brief='sends a list of currently stored Javascript resources')
    async def get_js_resources(self, ctx):
        try:
            await ctx.message.author.send('CURRENTLY STORED JAVASCRIPT RESOURCES ARE:')
            for resource in js_resources:
                await ctx.message.author.send(resource)
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')


# you MUST set this up at the end.
def setup(bot):
    bot.add_cog(ResourceCog(bot))
