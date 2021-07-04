import discord
import os
import youtube_dl
from configparser import ConfigParser

from discord.ext import commands

# Reading config
config = ConfigParser().read('config.ini')


class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def playurl(self, ctx, url: str):
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
        except PermissionError:
            await ctx.send("Wait for the current playing music to end or use the 'stop' command")
            return

        author = ctx.message.author.name
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                if member.name == author:
                    await vc.connect()

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
                if not file == "rickroll.mp3":
                    os.rename(file, "song.mp3")
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.play(discord.FFmpegPCMAudio("song.mp3"))

    @commands.command()
    async def pause(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command()
    async def resume(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @commands.command()
    async def stop(self, ctx):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


def setup(bot):
    bot.add_cog(MusicCog(bot))