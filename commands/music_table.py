from discord.ext import commands
import discord
from asyncio import TimeoutError

class MusicTableNyaa(commands.Cog):

    def create_category_embed_list(self, ctx, category_dict):
        num_categories = len(category_dict.keys())
        list_of_embeds = []
        for i, key in enumerate(category_dict):
            category, list_of_music = key, category_dict[key]
            embed = discord.Embed(color=ctx.author.color, title=f"Category: {category}", description=f"List of stored music under this category")
            # embed.add_field(name="\u200b", value="\u200b")
            for music in list_of_music:
                display_name = f"{music.name}: {music.title}"
                # value = music.url
                embed.add_field(name=music.title, value=music.name, inline=False)
                embed.set_footer(text=f"Page {i + 1} of {num_categories}")
            
            list_of_embeds.append(embed)
        
        if num_categories == 0:
            list_of_embeds.append(discord.Embed(color=ctx.author.color, title="None", description=f"List of stored music under this category"))
        
        return list_of_embeds
        

    @commands.command(name='table-list', help='List all music in music table')
    async def list_music(self, ctx):
        category_dict = ctx.bot.music_table.get_paginated_category()
        list_of_embeds = self.create_category_embed_list(ctx, category_dict)
        
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

    @commands.command(name='table-add', help='Add <name> <category> <url> to music table')
    async def add_music(self, ctx, name, category, url):
        with ctx.typing():
            success, msg = ctx.bot.music_table.add_music(category, name, url)

        return await ctx.send(ctx.bot.format_string(msg))

    @commands.command(name='table-remove', help='Remove <name> in music table')
    async def remove_music(self, ctx, name):
        success, msg = ctx.bot.music_table.remove_music(name)
        return await ctx.send(ctx.bot.format_string(msg))