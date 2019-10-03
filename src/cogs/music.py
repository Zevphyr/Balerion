import discord
import asyncio
import ffmpeg
import youtube_dl
from discord.ext import commands
from discord.voice_client import VoiceClient


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


class MusicCog(commands.Cog, name="Music Commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="join", brief="Connects to a voice channel", description="Joins the voice channel you are\
currently in", case_insensitive=True)
    @commands.cooldown(4, 30, commands.BucketType.user)  # Restricts spam
    async def connect_to_vc(self, ctx):
        channel = ctx.message.author.voice.channel
        embed = discord.Embed(title="Connected", description=f"Balerion has joined {channel}!",
                              color=discord.Color.dark_red())
        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)  # Moves to new channel
        await channel.connect(timeout=120.0, reconnect=True)
        await ctx.send(content=None, embed=embed)

    @commands.command(name="leave", brief="Disconnects from a voice channel", case_insensitive=True)
    @commands.cooldown(4, 30, commands.BucketType.user)  # Restricts spam
    async def disconnect_from_vc(self, ctx):
        voice_client = ctx.voice_client
        channel = ctx.message.author.voice.channel
        embed = discord.Embed(title="Disconnect", description=f"Balerion has left {channel}!",
                              color=discord.Color.dark_red())
        await voice_client.disconnect()
        await ctx.send(content=None, embed=embed)

    @commands.command(name="play", brief="Plays audio", case_insensitive=True)
    @commands.cooldown(4, 30, commands.BucketType.user)  # Restricts spam
    async def play_music(self, ctx, url):
        author = ctx.message.author
        voice_channel = author.voice_channel
        player = await voice_channel.create_ytdl_player(url)
        player.start()

    @commands.command(brief="Changes the player's volume", case_insensitive=True)
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send("Changed volume to {}%".format(volume))

    @commands.command(brief="Stops everything", case_insensitive=True)
    @commands.cooldown(4, 30, commands.BucketType.user)
    async def stop(self, ctx):
        """Stops the currently playing song and disconnects the bot from voice"""

        await ctx.voice_client.disconnect()

    @commands.command(case_insensitive=True, brief="Streams a song")
    @commands.cooldown(4, 30, commands.BucketType.user)  # Restricts spam
    async def stream(self, ctx, *, url):
        """Streams from a given url without pre-downloading a cache"""

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
            ctx.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(player.title))

    # @play.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("You are not connected to a voice channel.")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    ## Issue #25 - Add pause/resume commands.     
    @commands.command(name="pause", brief="Pauses music", case_insensitive=True) # Gives command description
    @commands.cooldown(4, 30, commands.BucketType.user) # Restricts Spam
    async def pause(self, ctx):
        """Pauses music"""

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send("Nothing to pause.")
    
    @commands.command(name="resume", brief="Resume music stream", case_insensitive=True) # Gives command description
    @commands.cooldown(4, 30, commands.BucketType.user) # Restricts Spam
    async def resume(self, ctx):
        """Resumes Music"""

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            return await ctx.send("Nothing to resume.")

def setup(bot):
    bot.add_cog(MusicCog(bot))
