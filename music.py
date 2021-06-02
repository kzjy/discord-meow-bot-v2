from discord.ext import commands
import discord
from ytdl import ytdl, FFMPEG_OPTIONS
import traceback
import os

class MusicTable():

    def __init__(self, txt):
        self.table = {}
        self.file = txt

        if not os.path.exists(self.file):
            f = open(self.file, 'w')
            f.close()
        
        self.load_music_info()

    def load_music_info(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                category, name, title, url = line.strip().split(",")
                self.table[name] = {"url": url, "category": category, "title": title}

    def save_music_info(self):
        with open(self.file, 'w', encoding="utf-8") as f:
            for name in self.table:
                url, category, title = self.table[name]["url"], self.table[name]["category"], self.table[name]["title"]
                f.write("{},{},{},{}\n".format(category, name, title, url))
    

    def add_music(self, category, name, url):
        """
        Add music to music table, return true, msg on success and false, error message on fail
        """
        name, category, url = name.strip(), category.strip(), url.strip()
        if name in self.table:
            return False, "The id {} already exists in the table".format(name)

        try:
            data = ytdl.extract_info(url, download=False)
            self.table[name] = {"url": url, "category": category, "title": data['title']}
            table.save_music_info()
        except Exception as e:
            traceback.print_exc()
            return False, "The video is unavailable"

        return True, "{}: {} has been added".format(name, data['title'])

    def remove_music(self, name):
        """
        Remove name from music table, return true, msg on success false, err on fail
        """
        if name not in self.table:
            return False, "The name {} does not exist in the music table".format(name)

        self.table.pop(name)
        return True, "{} has been removed from the table"
    
    def get_url(self, name):
        """
        Return the url of vid by name
        """
        return self.table.get(name, None)

    def __repr__(self):
        """
        Repr of self
        """
        s = "Music Table: \n"
        music_by_category = {}
        for name in self.table:
            category, title = self.table[name]["category"],  self.table[name]["title"] 
            if category not in music_by_category:
                music_by_category[category] = []
            
            music_by_category[category].append((name, title))
        
        for category in music_by_category:
            s += category + "\n"
            for music in music_by_category[category]:
                s += "    {}: {}\n".format(music[0], music[1])
        
        return s


class Music(commands.Cog):

    @commands.command(name='list', help='List all music in music table')
    async def list_music(self, ctx):
        return await ctx.send(str(table) + "\n**Nyaa~**")

    @commands.command(name='add', help='Add <name> <category> <url> to music table')
    async def add_music(self, ctx, name, category, url):
        async with ctx.typing():
            success, msg = table.add_music(category, name, url)

        return await ctx.send(msg + " **Nyaa~**")

    @commands.command(name='remove', help='Remove <name> in music table')
    async def remove_music(self, ctx, name):
        success, msg = table.remove_music(name)
        return await ctx.send(msg + " **Nyaa~**")

    @commands.command(name='play', help='Play <name>')
    async def play(self, ctx, name):
        url = table.get_url(name)
        if url is None:
            return await ctx.send("The name {} does not exist in the music table".format(name) + " **Nyaa~**")

        if not ctx.message.author.voice:
            return await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name) + " **Nyaa~**")        

        async with ctx.typing():
            info = ytdl.extract_info(table.table[name]['url'], download=False)
            URL = info['formats'][0]['url']

        voice_client = ctx.guild.voice_client

        if voice_client == None:
            channel = ctx.message.author.voice.channel
            voice_client = await channel.connect()
        
        if voice_client.is_playing():
            voice_client.stop()

        voice_client.play(discord.FFmpegPCMAudio(URL, executable="./ffmpeg.exe", **FFMPEG_OPTIONS))
        await ctx.send('**Now playing:** {}'.format(name) + " **Nyaa~**")
        

    @commands.command(name='pause', help='This command pauses the song')
    async def pause(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client is not None and voice_client.is_playing():
            voice_client.pause()
            return await ctx.send("Paused" + " **Nyaa~**")
        
        return await ctx.send("The bot is not playing anything at the moment." + " **Nyaa~**")
        
    @commands.command(name='resume', help='Resumes the song')
    async def resume(self,ctx):
        voice_client = ctx.guild.voice_client
        if voice_client is not None and voice_client.is_paused():
            voice_client.pause()
            return await ctx.send("Resumed" + " **Nyaa~**")
      
        return await ctx.send("The bot was not playing anything before this. Use play_song command" + " **Nyaa~**")

    @commands.command(name='stop', help='Stops the song')
    async def stop(self, ctx):
        voice_client = ctx.guild.voice_client
        if voice_client is not None and voice_client.is_playing():
            voice_client.stop()
            return await ctx.send("Stopped" + " **Nyaa~**")
       
        return await ctx.send("The bot is not playing anything at the moment." + " **Nyaa~**")

    @commands.command(name='join', help='Tells the bot to join the voice channel' )
    async def join(self, ctx):
        if not ctx.message.author.voice:
            return await ctx.send("{} is not connected to a voice channel".format(ctx.message.author.name) + " **Nyaa~**")
        else:
            channel = ctx.message.author.voice.channel
        return await channel.connect()

    @commands.command(name='leave', help='To make the bot leave the voice channel')
    async def leave(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_connected():
            return await voice_client.disconnect()
        else:
            return await ctx.send("The bot is not connected to a voice channel." + " **Nyaa~**")


table = MusicTable('./music.txt')