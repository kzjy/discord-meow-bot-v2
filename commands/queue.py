from data_class.music import Music
from discord.ext import commands
import discord
from asyncio import TimeoutError
from math import ceil

class QueueNyaa(commands.Cog):

    def create_embed_list(self, ctx, queue):
        queue = [x for x in queue if isinstance(x, Music)]
        num_songs_per_page = 5
        list_of_embeds = []
        for i in range(0, len(queue), num_songs_per_page):
            last_index = min(i + num_songs_per_page, len(queue))
            embed = discord.Embed(color=ctx.author.color, title="Currently Queued", description=f"List of currently queued music")
            for j in range(len(queue[i:last_index])):
                music = queue[i * num_songs_per_page + j]
                minute, seconds = music.duration // 60, music.duration % 60
                embed.add_field(name=f"{i * num_songs_per_page + j + 1} : {music.title}", value=f"Length: {minute}:{seconds:02d}", inline=False)
                embed.set_footer(text=f"Page {i//num_songs_per_page + 1} of {ceil(len(queue) /num_songs_per_page)}")
            
            list_of_embeds.append(embed)
        
        if len(queue) == 0:
            list_of_embeds.append(discord.Embed(color=ctx.author.color, title="Currently Queued", description=f"List of currently queued music"))
        
        return list_of_embeds

    @commands.command(name="add", help="Add <name/url/search terms> to queue.")
    async def add_queue(self, ctx):

        # Get music object from name or url
        async with ctx.typing():
            music = ctx.bot.parse_message_content(ctx.message.content)

        if music is not None:
            ctx.bot.queue.append(music)
            await ctx.send(ctx.bot.format_string(f"{music.title} added to queue."))
            s = ctx.bot.format_queue()
            return await self.queue(ctx)
        
        return await ctx.send(ctx.bot.format_string(f"Sowwiee I don't know what {ctx.message.content[5:]} means."))

    
    @commands.command(name="remove", help="Remove <position> from current queue")
    async def remove_queue(self, ctx, position):
        if not position.isdigit():
            return await ctx.send(ctx.bot.format_string(f"{position} isn't a valid integer."))
        
        position = int(position) - 1
        if position < 0 or position > len(ctx.bot.queue) - 1:
            return await ctx.send(ctx.bot.format_string(f"{position + 1} isn't a valid entry in the queue."))

        music = ctx.bot.queue.pop(position)
        return await ctx.send(ctx.bot.format_string(f"{music.title} has been removed from the queue."))

    @commands.command(name="queue", help="Check current queue")
    async def queue(self, ctx):

        list_of_embeds = self.create_embed_list(ctx, list(ctx.bot.queue))
        
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