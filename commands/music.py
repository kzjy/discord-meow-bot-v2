from discord.ext import commands
from ytdl_utils.ytdl import fetch_audio_source, fetch_data
from data_class.music import Music
import discord

class MusicNyaa(commands.Cog):
    
    @commands.command(name="loop", help="Toggle loop music in the current queue")
    async def loop(self, ctx):
        ctx.bot.loop_queue = not ctx.bot.loop_queue
        s = "Now looping queue" if ctx.bot.loop_queue else "Loop queue turned off"
        return await ctx.send(ctx.bot.format_string(s))

    @commands.command(name='play', help='Play <name/url/search term> immediately, play from queue if nothing is given')
    async def play(self, ctx):
        if not ctx.message.author.voice:
            return await ctx.send(ctx.bot.format_string(f"{ctx.message.author.name} is not connected to a voice channel"))

        
        msg = ctx.message.content.strip().split(" ")

        # Get voice client
        voice_client = ctx.guild.voice_client
        if voice_client == None:
            channel = ctx.message.author.voice.channel
            voice_client = await channel.connect()
        
        if len(msg) > 1: # Some argument given, get music from 
            async with ctx.typing():
                music = ctx.bot.parse_message_content(ctx.message.content)
            audio_source = fetch_audio_source(music.url)

            if audio_source is None:
                return await ctx.send(ctx.bot.format_string(f"The video is no longer available."))
            
            await ctx.send(ctx.bot.format_string(f"**Playing**: {music.title}"))
        
            if voice_client.is_playing():
                voice_client.source = audio_source
            else:
                ctx.bot.queue.insert(0, audio_source)
                ctx.bot.play_next()

        else: # Play something from queue
            if voice_client.is_playing():
                voice_client.stop()
            else:
                ctx.bot.play_next()
            
    @commands.command(name='pause', help='Pause current music')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client is not None and voice_client.is_playing():
            voice_client.pause()
            return await ctx.send(ctx.bot.format_string("Paused"))
        
        return await ctx.send(ctx.bot.format_string("The bot is not playing anything at the moment."))
        
    @commands.command(name='resume', help='Resume current music')
    async def resume(self,ctx):
        voice_client = ctx.guild.voice_client
        if voice_client is not None and voice_client.is_paused():
            voice_client.resume()
            return await ctx.send(ctx.bot.format_string("Resumed"))
      
        return await ctx.send(ctx.bot.format_string("The bot was not playing anything before."))

    @commands.command(name='skip', help='Skip current music')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client is not None and voice_client.is_playing():
            voice_client.stop()
            return await ctx.send(ctx.bot.format_string("Skipped"))
       
        return await ctx.send(ctx.bot.format_string("The bot is not playing anything at the moment."))

    @commands.command(name='join', help='Tells the bot to join the voice channel' )
    async def join(self, ctx):
        if not ctx.message.author.voice:
            return await ctx.send(ctx.bot.format_string(f"{ctx.message.author.name} is not connected to a voice channel"))

        channel = ctx.message.author.voice.channel
        await channel.connect()
        return await ctx.send(ctx.bot.format_string(f"Connected to {channel}"))

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
            return await ctx.send(ctx.bot.format_string(f"Disconnected"))
        else:
            return await ctx.send(ctx.bot.format_string("The bot is not connected to a voice channel."))
