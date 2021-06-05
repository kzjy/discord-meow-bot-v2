from discord.ext import commands
import discord
import time 
import asyncio
import random

class MiscNyaa(commands.Cog):

    @commands.command(name='nyaa', help='Nyaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    async def nyaa(self, ctx):
        return await ctx.send("https://i.kym-cdn.com/photos/images/original/001/763/021/8ed.jpg")
    
    @commands.command(name='roll', help='Roll a value out of <side>')
    async def roll(self, ctx, side):
        if side.strip().isdigit():
            num = random.randint(1, int(side.strip()))
            return await ctx.send(ctx.bot.format_string(f"Nyaa just rolled {num}."))
        
        return await ctx.send(ctx.bot.format_string(f"{side} isn't a number dum dum."))
    
    @commands.command(name='mention', help='Get attention of <user>')
    async def mention(self, ctx, member:discord.User=None):
        if (member == ctx.message.author or member == None):
            await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention} why you mention yourself ho?")) 
        else:
            for i in range(10):
                await ctx.send(ctx.bot.format_string(f"Someone needs ur attention {member.mention}!"))
                time.sleep(1)
    
    @commands.command(name='slap', help='Slap a bitch')
    async def slap(self, ctx, member:discord.User=None, count="1"):
        type_of_slaps = ['bitch', 'back hand', 'drop kicked and', '360 no scope', '2 hand']
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send(ctx.bot.format_string("No bully, you can only slap 5 times!"))
        for i in range(num_repeat):
            slap = type_of_slaps[random.randint(0, len(type_of_slaps) - 1)]
            if (member == ctx.message.author or member == None):
                await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention} {slap} slapped themselves!")) 
            else:
                await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention} just {slap} slapped {member.mention}!"))

    
    @commands.command(name='hug', help='Hug a bitch')
    async def hug(self, ctx, member:discord.User=None, count="1"):
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send(ctx.bot.format_string("No bully, you can only hug 5 times!"))
        for i in range(num_repeat):
            if (member == ctx.message.author or member == None):
                await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention}, self hugs are okay!")) 
            else:
                await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention} just hugged {member.mention}!"))
    
    @commands.command(name='headpat', help='Head pat a bitch nyaa')
    async def headpat(self, ctx, member:discord.User=None, count="1"):
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send(ctx.bot.format_string("No bully, you can only head pat 5 times!"))
        for i in range(num_repeat):
            if (member == ctx.message.author or member == None):
                await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention}, you can't pat yourself!")) 
            else:
                s = f"{ctx.message.author.mention} just gave {member.mention} a head pat!"
                await ctx.send(ctx.bot.format_string(s))
                await ctx.send("https://media.tenor.com/images/67dc5a58a23461f3f449e8f46623b1df/tenor.gif")
                      
    
    @commands.command(name='kiss', help='Homie kiss nyaa')
    async def kiss(self, ctx, member:discord.User=None, count="1"):
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send(ctx.bot.format_string("No bully, you can only homie kiss 5 times!"))
        
        if (member == ctx.message.author or member == None):
            return await ctx.send(ctx.bot.format_string(f"{ctx.message.author.mention}, you can't kiss yourself loner...")) 

        for i in range(num_repeat):
            s = f"{ctx.message.author.mention} just homie kissed {member.mention}!" 
            await ctx.send(ctx.bot.format_string(s))
            await ctx.send("https://i.kym-cdn.com/entries/icons/facebook/000/030/971/Screen_Shot_2019-08-29_at_2.44.51_PM.jpg")
            
    
    # @commands.command(name="me", help="Visualization of me coding the bot")
    # async def meirl(self, ctx):
    #     await ctx.send("https://www.youtube.com/watch?v=31HfP81oWDI\n")
    #     # return await ctx.send(ctx.bot.format_string("\n"))
    

    @commands.command(name="page", help="test123")
    async def page(self, ctx):
        embed1 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 1")
        embed2 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 2")
        embed3 = discord.Embed(color=ctx.author.color).add_field(name="Example", value="Page 3")
        embeds = [embed1, embed2, embed3]
        pages = len(embeds)
        cur_page = 1
        message = await ctx.send(embed=embeds[cur_page])

        await message.add_reaction("◀️")
        await message.add_reaction("▶️")

        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
            # This makes sure nobody except the command sender can interact with the "menu"

        while True:
            try:
                reaction, user = await ctx.bot.wait_for("reaction_add", timeout=15, check=check)
                # waiting for a reaction to be added - times out after x seconds, 60 in this
                # example

                if str(reaction.emoji) == "▶️" and cur_page != pages:
                    cur_page += 1
                    await message.edit(embed=embeds[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                elif str(reaction.emoji) == "◀️" and cur_page > 1:
                    cur_page -= 1
                    await message.edit(embed=embeds[cur_page - 1])
                    await message.remove_reaction(reaction, user)

                else:
                    await message.remove_reaction(reaction, user)
                    # removes reactions if the user tries to go forward on the last page or
                    # backwards on the first page
            except asyncio.TimeoutError:
                await message.delete()
                break
                # ending the loop if user doesn't react after x seconds