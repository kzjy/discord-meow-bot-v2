from discord.ext import commands
import discord
from asyncio import TimeoutError
from math import ceil
from ytdl_utils.ytdl import fetch_data, fetch_audio_source

class SoundEffectNyaa(commands.Cog):

    def create_embed_list(self, ctx, names):
        num_se_per_page = 12
        list_of_embeds = []
        for i in range(0, len(names), num_se_per_page):
            last_index = min(i + num_se_per_page, len(names))
            embed = discord.Embed(color=ctx.author.color, title="Sound Effects", description=f"List of stored sound effects")
            for name in names[i:last_index]:
                embed.add_field(name=name, value="\u200b", inline=True)
                embed.set_footer(text=f"Page {i//num_se_per_page + 1} of {ceil(len(names) /num_se_per_page)}")
            
            list_of_embeds.append(embed)
        
        if len(names) == 0:
            list_of_embeds.append(discord.Embed(color=ctx.author.color, title="Sound Effects", description=f"List of stored sound effects"))
        
        return list_of_embeds


    @commands.command(name='se', help='Play sound effect <name>')
    async def play_sound_effect(self, ctx, name):
        url = ctx.bot.se_table.get_url(name)

        if url is None:
            return await ctx.send(ctx.bot.format_string(f"The name {name} does not exist in the music table"))

        if not ctx.message.author.voice:
            return await ctx.send(ctx.bot.format_string(f"{ctx.message.author.name} is not connected to a voice channel"))   

        data = fetch_data(url)
        if data is None:
            return await ctx.send(ctx.bot.format_string("The sound effect is unavailable"))

        if data['duration'] > 30:
            return await ctx.send(ctx.bot.format_string("Sound effects should be < 30 seconds!"))
        
        voice_client = ctx.guild.voice_client
        
        current_audio_source = None
        was_playing = voice_client.is_playing()
        if voice_client.is_playing():
            current_audio_source = voice_client.source
            voice_client.pause()
        
        if current_audio_source is not None:
            ctx.bot.queue.insert(0, current_audio_source)

        new_audio_source = fetch_audio_source(url)
        if new_audio_source is not None:
            ctx.bot.queue.insert(0, new_audio_source)

        await ctx.send(ctx.bot.format_string(f'Playing sound effect: {name}'))

        if was_playing:
            voice_client.stop()
        else:
            ctx.bot.play_next()
    
    @commands.command(name='se-list', help='List all available sound effects')
    async def list_sound_effect(self, ctx):

        list_of_embeds = self.create_embed_list(ctx, list(ctx.bot.se_table.table.keys()))
        
        current_page = 0
        num_pages = len(list_of_embeds)

        message = await ctx.send(embed=list_of_embeds[current_page])

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]

        while True:
            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", timeout=15, check=check)

                if str(reaction.emoji) == "▶️" and current_page < num_pages - 1:
                    current_page += 1
                    
                elif str(reaction.emoji) == "◀️" and current_page > 0:
                    current_page -= 1     

                await message.edit(embed=list_of_embeds[current_page])
                await message.remove_reaction(reaction, user)

            except TimeoutError:
                break
        
        return await message.clear_reactions()

    @commands.command(name='se-add', help='Add a sound effect <name> <link>')
    async def add_sound_effect(self, ctx, name, url):
        with ctx.typing():
            success, msg = ctx.bot.se_table.add_sound_effect(name, url)

        return await ctx.send(ctx.bot.format_string(msg))

    @commands.command(name='se-remove', help='Remove a sound effect <name>')
    async def remove_sound_effect(self, ctx, name):
        success, msg = ctx.bot.se_table.remove_sound_effect(name)
        return await ctx.send(ctx.bot.format_string(msg))
