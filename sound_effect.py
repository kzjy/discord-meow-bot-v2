from discord.ext import commands
import discord
from ytdl import ytdl, FFMPEG_OPTIONS
import traceback
import os

class SoundEffectTable():

    def __init__(self, txt):
        self.table = {}
        self.file = txt

        if not os.path.exists(self.file):
            f = open(self.file, 'w')
            f.close()
        
        self.load_sound_effect_info()

    def load_sound_effect_info(self):
        with open(self.file, 'r', encoding="utf-8") as f:
            for line in f:
                name, url = line.strip().split(",")
                self.table[name] = url

    def save_sound_effect_info(self):
        with open(self.file, 'w', encoding="utf-8") as f:
            for name in self.table:
                url = self.table.get(name, "")
                f.write("{},{}\n".format(name, url))
    

    def add_sound_effect(self, name, url):
        """
        Add sound effect to table, return true, msg on success and false, error message on fail
        """
        name, url = name.strip(),  url.strip()
        if name in self.table:
            return False, f"The id {name} already exists in the table"

        try:
            data = ytdl.extract_info(url, download=False)
            table.table[name] = url
            table.save_sound_effect_info()
        except Exception as e:
            traceback.print_exc()
            return False, "The sound effect is unavailable"

        return True, f"Sound effect {name} has been added"

    def remove_sound_effect(self, name):
        """
        Remove name from sound_effect table, return true, msg on success false, err on fail
        """
        if name not in self.table:
            return False, f"The name {name} does not exist in the sound_effect table"

        self.table.pop(name)
        return True, f"{name} has been removed from the table"
    
    def get_url(self, name):
        """
        Return the url of vid by name
        """
        return self.table.get(name, None)

    def __repr__(self):
        """
        Repr of self
        """
        s = "Sound Effect Table: \n"
        for name in self.table:
            s += f"    {name}\n"
        
        return s

class SoundEffect(commands.Cog):

    @commands.command(name='se', help='Play sound effect <name>')
    async def play_sound_effect(self, ctx):
        return await ctx.send(str(table) + "\n**Nyaa~**")
    
    @commands.command(name='se-list', help='List all available sound effects')
    async def list_sound_effect(self, ctx):
        return await ctx.send(str(table) + "\n**Nyaa~**")

    @commands.command(name='se-add', help='Add a sound effect <name> <link>')
    async def add_sound_effect(self, ctx, name, url):
        async with ctx.typing():
            success, msg = table.add_sound_effect(name, url)

        return await ctx.send(msg + " **Nyaa~**")

    @commands.command(name='se-remove', help='Remove a sound effect <name>')
    async def remove_sound_effect(self, ctx, name):
        success, msg = table.remove_music(name)
        return await ctx.send(msg + " **Nyaa~**")

table = SoundEffectTable('./sound_effect.txt')