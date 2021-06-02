from discord.ext import commands
import discord
import time 
import random

class Misc(commands.Cog):

    @commands.command(name='nyaa', help='Nyaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    async def nyaa(self, ctx):
        return await ctx.send("https://i.kym-cdn.com/photos/images/original/001/763/021/8ed.jpg")
    
    @commands.command(name='roll', help='Roll a value out of <side>')
    async def roll(self, ctx, side):
        if side.strip().isdigit():
            num = random.randint(1, int(side.strip()))
            return await ctx.send(f"Nyaa just rolled {num}." + " **Nyaa~**")
        
        return await ctx.send(f"{side} isn't a number dum dum." + " **Nyaa~**")
    
    @commands.command(name='mention', help='Get attention of <user>')
    async def mention(self, ctx, member:discord.User=None):
        if (member == ctx.message.author or member == None):
            await ctx.send(f"{ctx.message.author.mention} why you mention yourself ho?" + " **Nyaa~**") 
        else:
            for i in range(10):
                await ctx.send(f"Someone needs ur attention {member.mention}!" + " **Nyaa~**")
                time.sleep(1)
    
    @commands.command(name='slap', help='Slap a bitch')
    async def slap(self, ctx, member:discord.User=None, count="1"):
        type_of_slaps = ['bitch', 'back hand', 'drop kicked and', '360 no scope', '2 hand']
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send("No bully, you can only slap 5 times!" + " **Nyaa~**")
        for i in range(num_repeat):
            slap = type_of_slaps[random.randint(0, len(type_of_slaps) - 1)]
            if (member == ctx.message.author or member == None):
                await ctx.send(f"{ctx.message.author.mention} {slap} slapped themselves!" + " **Nyaa~**") 
            else:
                await ctx.send(f"{ctx.message.author.mention} just {slap} slapped {member.mention}!" + " **Nyaa~**")

    
    @commands.command(name='hug', help='Hug a bitch')
    async def hug(self, ctx, member:discord.User=None, count="1"):
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send("No bully, you can only hug 5 times!" + " **Nyaa~**")
        for i in range(num_repeat):
            if (member == ctx.message.author or member == None):
                await ctx.send(f"{ctx.message.author.mention}, self hugs are okay!" + " **Nyaa~**") 
            else:
                await ctx.send(f"{ctx.message.author.mention} just hugged {member.mention}!" + " **Nyaa~**")
    
    @commands.command(name='headpat', help='Head pat a bitch nyaa')
    async def headpat(self, ctx, member:discord.User=None, count="1"):
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send("No bully, you can only head pat 5 times!" + " **Nyaa~**")
        for i in range(num_repeat):
            if (member == ctx.message.author or member == None):
                await ctx.send(f"{ctx.message.author.mention}, you can't pat yourself!" + " **Nyaa~**") 
            else:
                s = f"{ctx.message.author.mention} just gave {member.mention} a head pat!" + " **Nyaa~**\n" + "https://media.tenor.com/images/67dc5a58a23461f3f449e8f46623b1df/tenor.gif"
                await ctx.send(s)
    
    @commands.command(name='kiss', help='Homie kiss nyaa')
    async def kiss(self, ctx, member:discord.User=None, count="1"):
        if not count.isdigit():
            count = "1"
        num_repeat = int(count)
        if num_repeat > 5:
            num_repeat = 5
            await ctx.send("No bully, you can only homie kiss 5 times!" + " **Nyaa~**")
        
        if (member == ctx.message.author or member == None):
            return await ctx.send(f"{ctx.message.author.mention}, you can't kiss yourself loner..." + " **Nyaa~**") 

        for i in range(num_repeat):
            s = f"{ctx.message.author.mention} just homie kissed {member.mention}!" + " **Nyaa~**\n" + "https://i.kym-cdn.com/entries/icons/facebook/000/030/971/Screen_Shot_2019-08-29_at_2.44.51_PM.jpg"
            await ctx.send(s)
    
