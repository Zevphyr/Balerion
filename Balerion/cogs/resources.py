from discord.ext import commands
import sqlite3


# initializes the cog
class ResourceCog(commands.Cog, name='Resource Commands'):

    def __init__(self, bot):
        self.bot = bot # all functions require the 'self' parameter
        self.pydb = sqlite3.connect('python.db')
        self.pycursor = self.pydb.cursor()
        self.pycursor.execute("CREATE TABLE IF NOT EXISTS python (id INTEGER PRIMARY KEY, py_item TEXT)")
        self.jsdb = sqlite3.connect('js.db')
        self.jscursor = self.jsdb.cursor()
        self.jscursor.execute("CREATE TABLE IF NOT EXISTS js (id INTEGER PRIMARY KEY, js_item TEXT)")
        self.pydb.commit()
        self.jsdb.commit()

    @commands.command(name='addpython', brief='Adds a Python resource to list', descruption='Adds a Python resource \
    to a resource list.')
    async def add_py_resources(self, ctx, *, id):
        try:   # if you wanna get a bit fancy with error handling
            resource = ctx.message.content.replace('/addpython', '')
            self.pycursor.execute("INSERT INTO python VALUES (NULL, ?)", (resource,))
            self.pydb.commit()
            # py_resources.append(resource)
            await ctx.message.channel.send(f"Thank you, '{resource}' has been added to Python resources :)")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='pythonresources', brief='Send a list of currently stored Python resources')
    async def get_py_resources(self, *, ctx):
        try:
            await ctx.message.author.send('CURRENTLY STORED PYTHON RESOURCES ARE:')
            self.pycursor.execute("SELECT * FROM python")
            py_resources = self.pycursor.fetchall()
            for resource in py_resources:
                await ctx.message.author.send(resource[1])
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='addjs', brief='add a Javascript resource to a resource list', descruption='Adds a Java resource \
    to a resource list.')
    async def add_js_resources(self, ctx, *, id):
        try:
            resource = ctx.message.content.replace('/addjs', '')
            self.jscursor.execute("INSERT INTO js VALUES (NULL, ?)", (resource,))
            self.jsdb.commit()
            await ctx.message.channel.send(f"Thank you, '{resource}' has been added to Javascript resources :)")
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='jsresources', brief='sends a list of currently stored Javascript resources')
    async def get_js_resources(self, *, ctx):
        try:
            await ctx.message.author.send('CURRENTLY STORED JAVASCRIPT RESOURCES ARE:')
            self.jscursor.execute("SELECT * FROM js")
            js_resources = self.jscursor.fetchall()
            for resource in js_resources:
                await ctx.message.author.send(resource[1])
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='deletepy', brief='removes a resource from stored Python resources')
    @commands.has_permissions(administrator=True)
    async def del_python(self, *, ctx):
        try:
            id_str = ctx.message.content.replace('/deletepy', '')
            self.pycursor.execute("DELETE FROM python WHERE id=?", (int(id_str),))
            self.pydb.commit()
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='deletejs', brief='removes a resource from stored Javascript resources')
    @commands.has_permissions(administrator=True)
    async def del_js(self, *, ctx):
        try:
            id_str = ctx.message.content.replace('/deletejs', '')
            self.jscursor.execute("DELETE FROM js WHERE id=?", (int(id_str),))
            self.jsdb.commit()
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')


def setup(bot):
    bot.add_cog(ResourceCog(bot))
