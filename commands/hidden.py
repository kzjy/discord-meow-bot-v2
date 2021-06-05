from discord.ext import commands
import discord
from ytdl_utils.ytdl import fetch_audio_source, ytdl, FFMPEG_OPTIONS

class HiddenNyaa(commands.Cog):

    async def interrupt_play_link(self, ctx, link):
        voice_client = ctx.bot.get_guild(293883764382367744).voice_client

        if voice_client is None:
            guild = ctx.bot.get_guild(293883764382367744)
            channel = discord.utils.get(guild.voice_channels, name="5 Step 1 Estranged Broders")
            voice_client = await channel.connect()

        if voice_client is not None:
            current_audio_source = voice_client.source
            # if voice_client.is_playing():
            #     current_audio_source = voice_client.source
            #     voice_client.stop()

            def after(err):
                if current_audio_source is None:
                    ctx.bot.play_next()
                else:
                    voice_client.play(current_audio_source, after=lambda err: ctx.bot.play_next())

            
            new_audio_source = fetch_audio_source(link)
            if new_audio_source is not None:
                voice_client.pause()
                voice_client.play(new_audio_source, after=after)

    @commands.command(name='rr', hidden=True)
    async def rr(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")


    @commands.command(name="cb", hidden=True)
    async def cb(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=1NprEtCBVKQ")
    
    @commands.command(name="jeff", hidden=True)
    async def jeff(self, ctx):
        await self.interrupt_play_link(ctx, "https://www.youtube.com/watch?v=_nce9A5S5uM")