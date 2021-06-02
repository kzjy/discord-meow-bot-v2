from discord.ext import commands
import discord
import os
import nacl.secret
from discord_token import TOKEN
from utils.ytdl import ytdl
from commands.music import Music, FFMPEG_OPTIONS
from commands.misc import Misc
from commands.sound_effect import SoundEffect
from commands.hidden import Hidden
from intercept import Intercept

intents = discord.Intents().all()
prefix = "~"
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.add_cog(Music())
bot.add_cog(Misc())
bot.add_cog(SoundEffect())
bot.add_cog(Hidden())


@bot.event
async def on_ready():
    print("Bot ready")
    guild = bot.get_guild(293883764382367744)
    channel = discord.utils.get(guild.text_channels, name="bot-commands")
    await channel.send("Nyaa bot go **Nyaa~**")


@bot.event
async def on_command_error(ctx, err):
    return await ctx.send(f"Dum dum, {err}" + " **Nyaa~**")


if __name__ == "__main__" :
    bot.run(TOKEN)