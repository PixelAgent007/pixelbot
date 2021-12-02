import discord
from discord.ext import commands
from discord import utils, Colour
import mysql.connector
from discord_slash import cog_ext
import asyncio
import json


class SuggestionsCog(commands.Cog):

    def __init__(self, bot):
        self.bot: commands.Bot = bot
        with open('config/database.json', 'r') as f:
            self.dbcfg = json.load(f)
        self.conn = mysql.connector.connect(host=self.dbcfg["DB"]["HOST"], user=self.dbcfg["DB"]["USER"], password=self.dbcfg["DB"]["PASSWORD"], db=self.dbcfg["DB"]["DBNAME"], port=self.dbcfg["DB"]["PORT"])
        self.c = self.conn.cursor()
        print("Registered Suggestions Cog")

    @cog_ext.cog_slash(name="suggest", description="Suggest something. Type /suggest and answer the bots questions.",
                       guild_ids=[906804682452779058])
    async def suggest(self, ctx):
        author = ctx.author
        time = discord.Embed(title=f'Time', description=f'You ran out of time, please try again!', footer=f'Suggestion by: {author.name} • Suggestions by DerpDays', color=0xFF4C4C)
        briefembed = discord.Embed(title=f'Suggest', description=f'Please enter the Name of the mod/datapack you want to suggest!', footer=f'Suggestion by: {author.name} • Suggestions by DerpDays', color=Colour(0x71368a))
        explainembed = discord.Embed(title=f'Suggest', description=f'Please explain your suggestion in futher detail, and provide links etc!', footer=f'Suggestion by: {author.name} • Suggestions by DerpDays', color=Colour(0x71368a))

        self.c.execute(f"SELECT isEnabled FROM suggestionSettings WHERE GuildID={ctx.guild.id}")
        enabled = self.c.fetchone()[0]

        if enabled == "true":

            self.c.execute(f"SELECT tmpID FROM suggestionSettings WHERE GuildID={ctx.guild.id}")
            id = self.c.fetchone()[0]

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

            embed = discord.Embed(title=f'Suggestion ID: {id}', colour=Colour(0x71368a))
            embed.add_field(name=f'Datapack / Mod Name: ', value=f'{brief.content}')
            embed.add_field(name=f'Detailed Explanation: ', value=f'{explain.content}')
            embed.set_footer(text=f'Suggestion by: {author.name} • Suggestions by DerpDays')

            try:
                self.c.execute(f"SELECT outputChannel FROM suggestionSettings WHERE GuildID={ctx.guild.id}")
                channel: discord.TextChannel = discord.utils.get(ctx.guild.text_channels, id=int(self.c.fetchone()[0]))
                msg = await channel.send(embed=embed)
            except Exception as e:
                await ctx.send(e)
                return
            await msg.add_reaction(u"\u2705") # White checkmark on green bg
            await msg.add_reaction(u"\u274C") # Red cross

            self.c.execute(f"UPDATE suggestionSettings SET tmpID = {int(id) + 1} WHERE GuildID={ctx.guild.id}")

def setup(bot):
    bot.add_cog(SuggestionsCog(bot))
