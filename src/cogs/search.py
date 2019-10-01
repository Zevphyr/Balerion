import re
from discord.ext import commands
from urllib.parse import urlencode
from Balerion.networking import get


class SearchCog(commands.Cog, name='Search Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(glob=True)
    async def google(*search):
        """Grabs the first related google result for a given search"""

        parameters = urlencode([('search_query', '+'.join(search))])
        html = await get('https://www.google.com/results?' + parameters)
        links = re.findall('<a href="()"', html)
        if links:
            link = 'http://google.com' + links[0]
            return link
        else:
            return 'No video found'
