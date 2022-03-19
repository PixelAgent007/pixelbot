import discord
import os
import youtube_dl
from discord.ext import commands


class RickrollCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print("Registered Rickrolling Cog")

    @commands.command(name='rickroll')
    async def rickroll(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        author: discord.Member = ctx.message.author
        client = ctx.guild.voice_client
        if not client:
            if author.voice is None:
                raise commands.CommandError("You have to be in a voice channel.")
            else:
                channel = author.voice.channel
                client: discord.VoiceClient = await channel.connect()

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
        await ctx.message.delete()
        client.play(discord.FFmpegPCMAudio("rickroll.mp3"))

    @commands.command(name='pause')
    async def pause(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        await ctx.message.delete()
        for client in self.bot.voice_clients:
            client: discord.VoiceClient
            if client.is_playing():
                client.pause()

    @commands.command(name='resume')
    async def resume(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        for client in self.bot.voice_clients:
            client: discord.VoiceClient
            if client.is_paused():
                client.resume()

    @commands.command(name='stop')
    async def stop(self, ctx):
        if not ctx.author.id == self.bot.owner_id:
            return
        await ctx.message.delete()
        for client in self.bot.voice_clients:
            client: discord.VoiceClient
            if client.is_connected():
                await client.stop()


def setup(bot):
    bot.add_cog(RickrollCog(bot))
