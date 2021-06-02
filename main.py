from discord.ext import commands
import discord
import os
import nacl.secret
from discord_token import TOKEN
from utils.ytdl import ytdl
from commands.music import Music, FFMPEG_OPTIONS
from commands.misc import Misc
from commands.sound_effect import SoundEffect
from intercept import Intercept

intents = discord.Intents().all()
prefix = "~"
bot = commands.Bot(command_prefix=prefix, intents=intents)
bot.add_cog(Music())
bot.add_cog(Misc())

bot_intercept = Intercept(bot, prefix)

@bot.event
async def on_ready():
    print("Bot ready")
    guild = bot.get_guild(293883764382367744)
    channel = discord.utils.get(guild.text_channels, name="bot-commands")
    await channel.send("Nyaa bot go **Nyaa~**")


@bot.event
async def on_command_error(ctx, err):
    return await ctx.send(f"Dum dum, {err}" + " **Nyaa~**")

@bot.event
async def on_message(message):
    if message.guild is None:
        await bot_intercept.intercept_dm(message)
    else:
        if prefix in message.content:
            print(message.author, message.content)
        await bot.process_commands(message)


if __name__ == "__main__" :
    bot.run(TOKEN)