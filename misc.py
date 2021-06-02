from discord.ext import commands
import discord
import time 
import random

class Misc(commands.Cog):

    @commands.command(name='nyaa', help='Nyaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
    async def nyaa(self, ctx):
        return await ctx.send("https://i.kym-cdn.com/photos/images/original/001/763/021/8ed.jpg")
    
    @commands.command(name='slap', help='Slap a bitch')
    async def slap(self, ctx, member:discord.User=None):
        if (member == ctx.message.author or member == None):
            await ctx.send(f"{ctx.message.author.mention} slapped themselves!" + " **Nyaa~**") 
        else:
            await ctx.send(f"{ctx.message.author.mention} just bitch slapped {member.mention}!" + " **Nyaa~**")

    @commands.command(name='mention', help='Get attention of <user>')
    async def mention(self, ctx, member:discord.User=None):
        if (member == ctx.message.author or member == None):
            await ctx.send(f"{ctx.message.author.mention} why you mention yourself ho?" + " **Nyaa~**") 
        else:
            for i in range(10):
                await ctx.send(f"Someone needs ur attention {member.mention}!" + " **Nyaa~**")
                time.sleep(1)
    
    @commands.command(name='roll', help='Roll a value out of <side>')
    async def roll(self, ctx, side):
        if side.strip().isdigit():
            num = random.randint(1, int(side.strip()))
            return await ctx.send(f"Nyaa just rolled {num}." + " **Nyaa~**")
        
        return await ctx.send(f"{side} isn't a number dum dum." + " **Nyaa~**")
    
    @commands.command(name='hug', help='Hug a bitch')
    async def hug(self, ctx, member:discord.User=None):
        if (member == ctx.message.author or member == None):
            await ctx.send(f"{ctx.message.author.mention}, self hugs are okay!" + " **Nyaa~**") 
        else:
            await ctx.send(f"{ctx.message.author.mention} just hugged {member.mention}!" + " **Nyaa~**")
    
    @commands.command(name='headpat', help='Head pat a bitch nyaa')
    async def headpat(self, ctx, member:discord.User=None):
        if (member == ctx.message.author or member == None):
            await ctx.send(f"{ctx.message.author.mention}, you can't pat yourself!" + " **Nyaa~**") 
        else:
            await ctx.send(f"{ctx.message.author.mention} just gave {member.mention} a head pat!" + " **Nyaa~**")
            await ctx.send("https://media.tenor.com/images/67dc5a58a23461f3f449e8f46623b1df/tenor.gif")
    
    
    
