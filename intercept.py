import discord
from utils.ytdl import ytdl
from music import FFMPEG_OPTIONS

class Intercept():

    def __init__(self, bot, prefix):
        self.bot = bot
        self.prefix = prefix

    async def intercept_dm(self, message):
        for func_name in [x for x in dir(self) if "custom_intercept_dm" in x]:
            if message.content[0] == self.prefix and message.content[1:] in func_name:
                func = getattr(Intercept, func_name)
                await func(self, message)


    async def custom_intercept_dm_rr(self, message):
        voice_client = None

        if len(self.bot.voice_clients) > 0:
            voice_client = self.bot.voice_clients[0]
        
        if voice_client is None:
            guild = self.bot.get_guild(293883764382367744)
            channel = discord.utils.get(guild.voice_channels, name="5 Step 1 Estranged Broders")
            voice_client = await channel.connect()

        if voice_client is not None:
            if voice_client.is_playing():
                voice_client.stop()
            
            info = ytdl.extract_info("https://www.youtube.com/watch?v=dQw4w9WgXcQ", download=False)
            URL = info['formats'][0]['url']
            voice_client.play(discord.FFmpegPCMAudio(URL, executable="./ffmpeg.exe", **FFMPEG_OPTIONS))
    
    async def custom_intercept_dm_cb(self, message):
        voice_client = None

        if len(self.bot.voice_clients) > 0:
            voice_client = self.bot.voice_clients[0]
        
        if voice_client is None:
            guild = self.bot.get_guild(293883764382367744)
            channel = discord.utils.get(guild.voice_channels, name="5 Step 1 Estranged Broders")
            voice_client = await channel.connect()

        if voice_client is not None and voice_client.is_playing():
            current_audio_source = voice_client.source

            def after(err):
                voice_client.stop()
                voice_client.play(current_audio_source)

            info = ytdl.extract_info("https://www.youtube.com/watch?v=1NprEtCBVKQ", download=False)
            URL = info['formats'][0]['url']
            new_audio_source = discord.FFmpegPCMAudio(URL, executable="./ffmpeg.exe", **FFMPEG_OPTIONS)
            voice_client.pause()
            voice_client.play(new_audio_source, after=after)


if __name__ == "__main__":
    i = Intercept(None)
    i.intercept(None)