import discord
from discord_token import TOKEN
from commands.music import MusicNyaa
from commands.misc import MiscNyaa
from commands.queue import QueueNyaa
from commands.music_table import MusicTableNyaa
from commands.sound_effect import SoundEffectNyaa
from commands.hidden import HiddenNyaa
from custom_bot import CustomBot

import traceback

intents = discord.Intents().all()
prefix = "~"

bot = CustomBot(command_prefix=prefix, intents=intents)
bot.add_cog(MusicNyaa())
bot.add_cog(MusicTableNyaa())
bot.add_cog(QueueNyaa())
bot.add_cog(MiscNyaa())
bot.add_cog(SoundEffectNyaa())
bot.add_cog(HiddenNyaa())

@bot.event
async def on_ready():
    print("Bot ready")
    guild = bot.get_guild(293883764382367744)
    channel = discord.utils.get(guild.text_channels, name="bot-commands")
    await bot.change_presence(activity=discord.Game(name="depression"))
    await channel.send("Nyaa bot go **Nyaa~**")


@bot.event
async def on_command_error(ctx, err):
    print(err)
    traceback.print_exc()
    return await ctx.send(bot.format_string(f"Dum dum, {err}"))


if __name__ == "__main__" :
    bot.run(TOKEN)