from discord.ext import commands
import discord
from asyncio import TimeoutError
from ytdl_utils.ytdl import fetch_data, fetch_audio_source

class SoundEffectNyaa(commands.Cog):

    def create_category_embed_list(self, ctx, category_dict):
        num_categories = len(category_dict.keys())
        list_of_embeds = []
        for i, key in enumerate(category_dict):
            category, list_of_music = key, category_dict[key]
            embed = discord.Embed(color=ctx.author.color, title=f"Category: {category}", description=f"List of stored sound effects under this category")
            for music in list_of_music:
                embed.add_field(name=music.name, value=f"Length: 00:{music.duration:02d}", inline=False)
            
            embed.set_footer(text=f"Page {i + 1} of {num_categories}")
            list_of_embeds.append(embed)
        
        if num_categories == 0:
            list_of_embeds.append(discord.Embed(color=ctx.author.color, title="None", description=f"List of stored sound effects under this category"))
        
        return list_of_embeds


    @commands.command(name='se', help='Play sound effect <name>')
    async def play_sound_effect(self, ctx, name):
        url = ctx.bot.se_table.get_url(name)

        if url is None:
            return await ctx.send(ctx.bot.format_string(f"The name {name} does not exist in the sound effect table"))

        if not ctx.message.author.voice:
            return await ctx.send(ctx.bot.format_string(f"{ctx.message.author.name} is not connected to a voice channel"))   

        data = fetch_data(url)
        if data is None:
            return await ctx.send(ctx.bot.format_string("The sound effect is unavailable"))

        if data['duration'] > 30:
            return await ctx.send(ctx.bot.format_string("Sound effects should be < 30 seconds!"))
        
        voice_client = ctx.guild.voice_client

        if voice_client == None:
            channel = ctx.message.author.voice.channel
            voice_client = await channel.connect()
        
        current_audio_source = None
        was_playing = voice_client.is_playing()

        if voice_client.is_playing():
            current_audio_source = voice_client.source
            voice_client.pause()
        
        if current_audio_source is not None:
            ctx.bot.queue.insert(0, current_audio_source)

        new_audio_source = fetch_audio_source(url)
  
        msg = ctx.bot.format_string(f'Playing sound effect: {name}')
        msg = await ctx.send(msg)


        if was_playing:
            voice_client.source = new_audio_source
        else:
            ctx.bot.queue.insert(0, new_audio_source)
            ctx.bot.play_next()
    
    @commands.command(name='se-list', help='List all available sound effects')
    async def list_sound_effect(self, ctx):
        category_dict = ctx.bot.se_table.get_paginated_category()
        list_of_embeds = self.create_category_embed_list(ctx, category_dict)
        
        current_page = 0
        num_pages = len(list_of_embeds)

        message = await ctx.send(embed=list_of_embeds[current_page])

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"] and reaction.message.id == message.id

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

    @commands.command(name='se-add', help='Add a sound effect <category> <name> <url>')
    async def add_sound_effect(self, ctx, category, name, url):
        async with ctx.typing():
            success, msg = ctx.bot.se_table.add_sound_effect(category, name, url)

        return await ctx.send(ctx.bot.format_string(msg))

    @commands.command(name='se-remove', help='Remove a sound effect <name>')
    async def remove_sound_effect(self, ctx, name):
        success, msg = ctx.bot.se_table.remove_sound_effect(name)
        return await ctx.send(ctx.bot.format_string(msg))
