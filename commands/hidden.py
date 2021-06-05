from discord.ext import commands
import discord
from ytdl_utils.ytdl import fetch_audio_source

class HiddenNyaa(commands.Cog):

    async def interrupt_play_link(self, ctx, link):
        voice_client = ctx.bot.get_guild(293883764382367744).voice_client

        if voice_client is None:
            guild = ctx.bot.get_guild(293883764382367744)
            channel = discord.utils.get(guild.voice_channels, name="5 Step 1 Estranged Broders")
            voice_client = await channel.connect()

        current_audio_source = None
        if voice_client.is_playing():
            current_audio_source = voice_client.source
        
        if current_audio_source is not None:
            ctx.bot.queue.insert(0, current_audio_source)

        new_audio_source = fetch_audio_source(link)
        if new_audio_source is not None:
            voice_client.source = new_audio_source

    @commands.command(name='rr', hidden=True)
    async def rr(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")

    @commands.command(name="cb", hidden=True)
    async def cb(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=1NprEtCBVKQ")
    
    @commands.command(name="jeff", hidden=True)
    async def jeff(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=_nce9A5S5uM")