import discord
from discord.ext import commands
from discord import utils, Colour
from discord.ext.commands import has_permissions
import asyncio
import json

class Suggest(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="suggest")
    @commands.guild_only()
    async def suggest(self, ctx):
        if self.bot.config["GUILDS"][str(ctx.guild.id)]["TOGGLED"] == "OFF":
            await ctx.send("Suggestions currently aren't open!")
            return

        author = ctx.author
        time = discord.Embed(title=f'Time', description=f'You ran out of time, please try again!', footer=f'Suggestion by: {author.name} • Suggestions by DerpDays', color=0xFF4C4C)
        briefembed = discord.Embed(title=f'Suggest', description=f'Please enter the Name of the mod/datapack you want to suggest!', footer=f'Suggestion by: {author.name} • Suggestions by DerpDays', color=Colour(0x71368a))
        explainembed = discord.Embed(title=f'Suggest', description=f'Please explain your suggestion in futher detail, and provide links etc!', footer=f'Suggestion by: {author.name} • Suggestions by DerpDays', color=Colour(0x71368a))
        await ctx.message.delete()

        if self.bot.config["GUILDS"][str(ctx.guild.id)]["TOGGLED"] == "ON":

            def check(m):
                return True if m.channel.id == ctx.channel.id and m.author.id == author.id else False

            msg = await ctx.send(f'Please reply to the following {author.mention}!')

            await ctx.send(embed=briefembed)
            try:
                brief = await self.bot.wait_for('message', check=check, timeout=300)
            except asyncio.TimeoutError:
                timemsg = await ctx.send(embed=time)
                await asyncio.sleep(30)
                await timemsg.delete()
                await msg.delete()
                return

            await msg.delete()
            await ctx.send(embed=explainembed)
            try:
                explain = await self.bot.wait_for('message', check=check, timeout=300)
            except asyncio.TimeoutError:
                timemsg = await ctx.send(embed=time)
                await asyncio.sleep(30)
                await timemsg.delete()
                return

            embed = discord.Embed(title=f'Suggestion ID: {self.bot.config["GUILDS"][str(ctx.guild.id)]["ID"]}', colour=Colour(0x71368a))
            embed.add_field(name=f'Brief Explanation: ', value=f'{brief.content}')
            embed.add_field(name=f'Detailed Explanation: ', value=f'{explain.content}')
            embed.set_footer(text=f'Suggestion by: {author.name} • Suggestion by DerpDays')

            try:
                channel = discord.utils.get(ctx.guild.text_channels, id=int(self.bot.config["GUILDS"][str(ctx.guild.id)]["OUTPUT"]))
                msg = await channel.send(embed=embed)
            except:
                await ctx.send(embed=discord.Embed(title=f'Suggest', description=f'Sending your suggestion failed. This could be because the owner didnt set the output properly or your suggestion exceeded 2,000 Chars. To configure the bot properly do {ctx.prefix}suggestsettings', color=0xff4c4c))
                return
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")

            id = self.bot.config["GUILDS"][str(ctx.guild.id)]["ID"]
            newid = int(id) + 1
            self.bot.config["GUILDS"][str(ctx.guild.id)]["ID"] = str(newid)
            with open('config/settings.json', 'w') as f:
                json.dump(self.bot.config, f, indent=2)

def setup(bot):
    bot.add_cog(Suggest(bot))
