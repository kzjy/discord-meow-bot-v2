from discord.ext import commands
import discord
from utils.ytdl import ytdl, FFMPEG_OPTIONS
import traceback
import os


class Hidden(commands.Cog):

    async def interrupt_play_link(self, ctx, link):
        voice_client = ctx.bot.get_guild(293883764382367744).voice_client

        if voice_client is None:
            guild = ctx.bot.get_guild(293883764382367744)
            channel = discord.utils.get(guild.voice_channels, name="5 Step 1 Estranged Broders")
            voice_client = await channel.connect()

        if voice_client is not None and voice_client.is_playing():
            current_audio_source = voice_client.source

            def after(err):
                voice_client.stop()
                voice_client.play(current_audio_source)
            
            URL = None
            try:
                info = ytdl.extract_info(link, download=False)
                URL = info['formats'][0]['url']
            except Exception:
                pass
            
            if URL is not None:
                new_audio_source = discord.FFmpegPCMAudio(URL, executable="./ffmpeg.exe", **FFMPEG_OPTIONS)
                voice_client.pause()
                voice_client.play(new_audio_source, after=after)

    @commands.command(name='rr', hidden=True)
    async def rr(self, ctx):
        if ctx.guild is None:
            voice_client = ctx.bot.get_guild(293883764382367744).voice_client
            
            if voice_client is None:
                guild = ctx.bot.get_guild(293883764382367744)
                channel = discord.utils.get(guild.voice_channels, name="5 Step 1 Estranged Broders")
                voice_client = await channel.connect()

            if voice_client is not None:
                if voice_client.is_playing():
                    voice_client.stop()
                
                info = ytdl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
                URL = info['formats'][0]['url']
                voice_client.play(discord.FFmpegPCMAudio(URL, executable="./ffmpeg.exe", **FFMPEG_OPTIONS))

    @commands.command(name="cb", hidden=True)
    async def cb(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=1NprEtCBVKQ")
    
    @commands.command(name="jeff", hidden=True)
    async def jeff(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=_nce9A5S5uM")