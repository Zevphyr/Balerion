import requests
import json
import discord
from discord.ext import commands


def jsonDump(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)


Wardata = requests.get('https://war-service-live.foxholeservices.com/api/worldconquest/war')
MapStatic = requests.get('https://war-service-live.foxholeservices.com/api/worldconquest/worldconquest/maps/:mapName/static')
MapDataNames = [
    "StonecradleHex",
    "AllodsBightHex",
    "GreatMarchHex",
    "TempestIslandHex",
    "MarbanHollow",
    "ViperPitHex",
    "ShackledChasmHex",
    "DeadLandsHex",
    "LinnMercyHex",
    "HeartlandsHex",
    "EndlessShoreHex",
    "GodcroftsHex",
    "FishermansRowHex",
    "UmbralWildwoodHex",
    "ReachingTrailHex",
    "WestgateHex",
    "CallahansPassageHex",
    "OarbreakerHex",
    "DrownedValeHex",
    "FarranacCoastHex",
    "MooringCountyHex",
    "WeatheredExpanseHex",
    "LochMorHex"
]

worldconquest/maps/:mapName/dynamic/public


/worldconquest/maps/:mapName/static

class FoxholeCog(commands.Cog, name="Foxhole Data Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name='GET', case_insensitive=True, brief='This is for Foxhole-related commands', description='Retrieves \
    data from the Foxhole API')
    async def GET(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('Invalid request...')


    @GET.command(name='Raw')
    def warState(self):
        embed = discord.Embed(title="WarData", description=f"Balerion has joined {channel}!",
                                    color=discord.Color.dark_red())
    jsonDump(Wardata.json())

    @GET.command
    async def WarReport(self, ctx, region):
        region = region.lower
        MapWarReport = 'https://war-service-live.foxholeservices.com/api/worldconquest/warReport/{}'
        if region not in MapDataNames:
            await ctx.send('Invalid region...')
            print('fail')
        else:
            for region in MapDataNames:
            MWRM = MapWarReport.format(region)
            print(MWRM)
        member = ctx.message.author
        guild = ctx.message.guild