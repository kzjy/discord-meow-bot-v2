from discord.ext import commands
import discord
import asyncio
from data_class.table import MusicTable, SoundEffectTable
from data_class.music import Music
from ytdl_utils.ytdl import fetch_audio_source, fetch_data, ytdl

class CustomBot(commands.Bot):

    def __init__(self, *args, **kwargs):
        super(CustomBot, self).__init__(*args, **kwargs)
        self.queue = [] 
        self.loop_queue = False

        self.music_table = MusicTable("./music.txt")
        self.se_table = SoundEffectTable("./sound_effect.txt")

    def format_queue(self):
        s = "**Currently queued:**\n"
        for i, music in enumerate(self.queue):
            title = music.title.replace('*', '\*').replace('_', '\_')
            s += f"      {i + 1}: {title}\n"
        
        s += "\n"
        return s
    
    def format_string(self, string):
        if string[-1] == "\n":
            return string + "**Nyaa ~ **"
        return string + " **Nyaa ~ **"
    
    def parse_message_content(self, msg):
        split_space = msg.strip().split(" ")[1:]
        
        # Either in current table or youtube link
        if len(split_space) == 1:
            # Fetch youtube link and return music object
            if "youtube.com" in split_space[0]:
                url = split_space[0].strip()
                data = fetch_data(url)
                if data is None:
                    return None
                
                music = Music(".", "temp", data["title"], url)
                return music
            
            # Get music object from table
            if split_space[0] in self.music_table.table:
                music = self.music_table.get(split_space[0])
                return music
        
       
        arg = " ".join(split_space)
        data = ytdl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        if data is None:
            return None
        music = Music(".", "temp", data['title'], data["webpage_url"])

        return music            


    def play_next(self):
        """"
        Get the next song, assumes bot is already playing and is in a voice client
        """
        voice_client = self.get_guild(293883764382367744).voice_client

        if voice_client is None or voice_client.is_playing():
            return
        
        # No more songs in the queue
        if len(self.queue) == 0:
            guild = self.get_guild(293883764382367744)
            channel = discord.utils.get(guild.text_channels, name="bot-commands")
            asyncio.run_coroutine_threadsafe(channel.send(self.format_string(f"There is nothing to play in the queue right now.")), self.loop)
            return
        
        item = self.queue.pop(0)

        if isinstance(item, Music):

            # Next song will be the same one
            if self.loop_queue:
                self.queue.append(item)
        
            audio_source = fetch_audio_source(item.url)
            if audio_source is None:
                print(f"Error playing {item.title}")
                self.play_next()

            else:
                guild = self.get_guild(293883764382367744)
                channel = discord.utils.get(guild.text_channels, name="bot-commands")
                asyncio.run_coroutine_threadsafe(channel.send(self.format_string(f"**Playing**: {item.title}")), self.loop)
                voice_client.play(audio_source, after=lambda err: self.play_next())
        
        else:
        
            voice_client.play(item, after=lambda err: self.play_next())
