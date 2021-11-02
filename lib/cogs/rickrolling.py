import discord
import os
import youtube_dl
from discord.ext import commands


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print("Registered Rickrolling Cog")

    @commands.command(name='rickroll')
    async def rickroll(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        await ctx.message.delete()
        author = ctx.message.author
        for vc in ctx.guild.voice_channels:
            for member in vc.members:
                if member == author:
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

    @commands.command(name='pause')
    async def pause(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        await ctx.message.delete()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_playing():
            voice.pause()
        else:
            await ctx.send("Currently no audio is playing.")

    @commands.command(name='resume')
    async def resume(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        await ctx.message.delete()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice.is_paused():
            voice.resume()
        else:
            await ctx.send("The audio is not paused.")

    @commands.command(name='stop')
    async def stop(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        await ctx.message.delete()
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        voice.stop()
        if voice.is_connected():
            await voice.disconnect()
        else:
            await ctx.send("The bot is not connected to a voice channel.")


def setup(bot):
    bot.add_cog(FunCog(bot))
