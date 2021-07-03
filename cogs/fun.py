import discord
import os
import youtube_dl
from configparser import ConfigParser

from discord.ext import commands

# Reading config
config = ConfigParser().read('config.ini')


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def rickroll(self, ctx):
        author = ctx.message.author.name
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                if member.name == author:
                    await vc.connect()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.message.guild)
        if not os.path.isfile("rickroll.mp3"):
            url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, "rickroll.mp3")
        voice.play(discord.FFmpegPCMAudio("rickroll.mp3"))


def setup(bot):
    bot.add_cog(FunCog(bot))
