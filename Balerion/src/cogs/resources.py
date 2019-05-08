from discord.ext import commands
import sqlite3


roles_list = ['python', 'javascript', 'c', 'webdev', 'java']


class ResourceCog(commands.Cog, name='Resource Commands'):

    def __init__(self, bot):
        self.bot = bot
        self.conn = sqlite3.connect('resources.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS resources (id INTEGER PRIMARY KEY, lang TEXT, resource TEXT)")
        self.conn.commit()

    @commands.command(name='add', brief="Stores a given resource for the given language")
    async def add_resource(self, ctx, lang):
        lang = lang.lower()
        if lang not in roles_list:
            await ctx.message.channel.send('That language is not currently stored')
        else:
            try:
                resource = ctx.message.content.replace(lang, '', 1)
                resource = resource.replace(resource[:4], '')
                self.cursor.execute("INSERT INTO resources VALUES (NULL, ?, ?)", (lang, resource,))
                self.conn.commit()
                await ctx.message.channel.send(f'Thank you. This has been added to {lang} resources \n {resource}')
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='get', brief="Returns stored resources for a given language")
    async def get_resources(self, ctx, lang):
        lang = lang.lower()
        if lang not in roles_list:
            await ctx.channel.send('That language is not currently stored.')
        else:
            try:
                self.cursor.execute("SELECT * FROM resources WHERE lang=?", (lang,))
                resource_list = self.cursor.fetchall()
                await ctx.message.author.send(f'CURRENTLY STORED {lang.upper()} RESOURCES ARE:')
                for resource in resource_list:
                    await ctx.message.author.send(resource[2])
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='manage', brief="Returns stored resources to an admin, to identify for deletion")
    @commands.has_permissions(administrator=True)
    async def manage_resources(self, ctx, lang):
        lang = lang.lower()
        if lang not in roles_list:
            ctx.channel.send('That language is not currently stored')
        else:
            try:
                self.cursor.execute("SELECT * FROM resources WHERE lang=?", (lang,))
                resource_list = self.cursor.fetchall()
                await ctx.message.author.send(f'CURRENTLY STORED {lang.upper()} RESOURCES ARE:')
                for resource in resource_list:
                    await ctx.message.author.send(f'Resource #{resource[0]} - {resource[1].upper()} - {resource[2]}')
            except Exception as e:
                await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')

    @commands.command(name='deleteresource', brief="Deletes resource corresponding to given resource ID")
    @commands.has_permissions(administrator=True)
    async def delete_resource(self, ctx, id):
        try:
            self.cursor.execute("DELETE FROM resources WHERE id=?", (int(id),))
            self.conn.commit()
            await ctx.message.author.send(f'Resource #{id} deleted')
        except Exception as e:
            await ctx.send(f'**`ERROR:`** {type(e).__name__} - {e}')


def setup(bot):
    bot.add_cog(ResourceCog(bot))
