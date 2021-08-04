from discord import Colour, Embed
from discord.ext import commands, tasks
import discord
import asyncio
from sqlite3 import connect
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
import re
from datetime import datetime, timedelta

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    conn = connect("config/db/database.db", check_same_thread=False)
    c = conn.cursor()

    def convertTime(self, time):
        time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}
        secs = int(time[:-1]) * time_dict[time[-1]]
        endtime = datetime.utcnow() + timedelta(seconds=secs)
        return endtime.strftime("%Y-%m-%d %H:%M:%S")


    @commands.command(name="mute")
    @commands.has_role(870219761475276800)
    async def mute(self, ctx, member: discord.Member, time=None):
        muted_role = discord.utils.get(ctx.guild.roles, id=864582175470649344)
        if not time:
            await member.add_roles(muted_role)
            notimeEmbed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted successfully.**", color=discord.Color.green())
            await ctx.send(embed=notimeEmbed)
        else:
            endtime = self.convertTime(time)
            self.c.execute(f"INSERT INTO Mutes (UserID, EndTime) VALUES({member.id}, {endtime})")
            await member.add_roles(muted_role)
            embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted until {endtime} UTC.**", color=discord.Color.green())
            await ctx.send(embed=embed)
        if time:
            time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}
            secs = int(time[:-1]) * time_dict[time[-1]]
            if secs > 300:
                embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted for {secs} seconds.**", color=discord.Color.green())
                await member.add_roles(muted_role)
                await asyncio.sleep(secs)
                if muted_role in member.roles:
                    await member.remove_roles(muted_role)
                    embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was unmuted.**", color=discord.Color.green())
                    await ctx.send(embed=embed)
                self.c.execute(f"SELECT EXISTS (SELECT 1 FROM Mutes WHERE UserID={member.id})")
                out = self.c.fetchone()
                exists = out[0]
                if exists == 1:
                    self.c.execute(f"DELETE FROM Mutes WHERE UserID={member.id}")
        self.conn.commit()


    @tasks.loop(seconds=1.0)
    async def auto_unmute(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                self.c.execute(f"SELECT EXISTS (SELECT 1 FROM Mutes WHERE UserID={member.id})")
                out = self.c.fetchone()
                exists = out[0]
                if exists == 1:
                    self.c.execute(f"SELECT EndTime FROM Mutes WHERE UserID={member.id}")
                    endtime = self.c.fetchone()
                    if datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") == endtime[0]:
                        self.c.execute(f"DELETE FROM Mutes WHERE UserID={member.id}")
                 

    @commands.command(name="unmute")
    @commands.has_role(870219761475276800)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, id=864582175470649344)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was unmuted.**", color=discord.Color.green())
            await ctx.send(embed=embed)
        self.c.execute(f"SELECT EXISTS (SELECT 1 FROM Mutes WHERE UserID={member.id})")
        out = self.c.fetchone()
        exists = out[0]
        if exists == 1:
            self.c.execute(f"DELETE FROM Mutes WHERE UserID={member.id}")


    @commands.command(name="kick")
    @commands.has_role(849949389178535947)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)
        embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was kicked.**", color=discord.Color.green())
        await ctx.send(embed=embed)

        
    @commands.command(name="ban")
    @commands.has_role(849949389178535947)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)
        embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was banned.**", color=discord.Color.green())
        await ctx.send(embed=embed)


    @commands.command(name="unban")
    @commands.has_role(849949389178535947)
    async def unban(self, ctx, member, *, reason=None):
        member = await self.bot.fetch_user(int(member))
        await ctx.guild.unban(member, reason=reason)
        embed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was unbanned.**", color=discord.Color.green())
        await ctx.send(embed=embed)


    @commands.command(name="purge")
    @commands.has_role(849949389178535947)
    async def purge(self, ctx, amount=10):
        await ctx.channel.purge(limit=amount)
        embed = discord.Embed(description=f"✅ **{amount} messages were deleted.**", color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=15)

def setup(bot):
    bot.add_cog(ModerationCog(bot))