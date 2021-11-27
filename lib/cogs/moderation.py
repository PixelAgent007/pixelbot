from asyncio import sleep

import discord
import asyncio
import mysql.connector
import json

from discord import HTTPException
from discord.ext import commands, tasks
from datetime import datetime, timedelta


class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        with open('config/database.json', 'r') as f:
            self.dbcfg = json.load(f)
        self.conn = mysql.connector.connect(host=self.dbcfg["DB"]["HOST"], user=self.dbcfg["DB"]["USER"],
                                            password=self.dbcfg["DB"]["PASSWORD"], db=self.dbcfg["DB"]["DBNAME"],
                                            port=self.dbcfg["DB"]["PORT"])
        self.c = self.conn.cursor()
        self.yes = u"\u2705"  # White checkmark on green bg
        self.no = u"\u274C"  # Red cross
        print("Registered Moderation Cog")

    def convertTime(self, time):
        time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}
        secs = int(time[:-1]) * time_dict[time[-1]]
        endtime = datetime.utcnow() + timedelta(seconds=secs)
        return endtime.strftime("%Y-%m-%d %H:%M:%S")
    """
    @commands.command(name="mute")
    @commands.has_permissions(mute_members=True)
    async def mute(self, ctx, member: discord.Member, time=None):
        muted_role = discord.utils.get(ctx.guild.roles, id=864582175470649344)
        if not time:
            await member.add_roles(muted_role)
            notimeEmbed = discord.Embed(
                description=f"{self.yes} **{member.display_name}#{member.discriminator} was muted successfully.**",
                color=discord.Color.green())
            await ctx.send(embed=notimeEmbed)
        else:
            time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400, "w": 604800}
            secs = int(time[:-1]) * time_dict[time[-1]]
            if secs < 300:
                embed = discord.Embed(
                    description=f"{self.yes} **{member.display_name}#{member.discriminator} was muted for {secs} seconds.**",
                    color=discord.Color.green())
                await member.add_roles(muted_role)
                await ctx.send(embed=embed)
                await asyncio.sleep(secs)
                if muted_role in member.roles:
                    await member.remove_roles(muted_role)
                    embed = discord.Embed(
                        description=f"{self.yes} **{member.display_name}#{member.discriminator} was unmuted.**",
                        color=discord.Color.green())
                    await ctx.send(embed=embed)
                self.c.execute(f"SELECT EXISTS (SELECT 1 FROM mutes WHERE UserID={member.id})")
                out = self.c.fetchone()
                exists = out[0]
                if exists == 1:
                    self.c.execute(f"DELETE FROM mutes WHERE UserID={member.id}")
            else:
                endtime = self.convertTime(time)
                self.c.execute(f"INSERT INTO mutes (UserID, EndTime) VALUES({member.id}, '{endtime}')")
                await member.add_roles(muted_role)
                embed = discord.Embed(
                    description=f"{self.yes} **{member.display_name}#{member.discriminator} was muted until {endtime} UTC.**",
                    color=discord.Color.green())
                await ctx.send(embed=embed)
        self.conn.commit()

    @tasks.loop(seconds=1.0)
    async def auto_unmute(self):
        for guild in self.bot.guilds:
            for member in guild.members:
                self.c.execute(f"SELECT EXISTS (SELECT 1 FROM mutes WHERE UserID={member.id})")
                out = self.c.fetchone()
                exists = out[0]
                if exists == 1:
                    self.c.execute(f"SELECT EndTime FROM mutes WHERE UserID={member.id}")
                    endtime = self.c.fetchone()
                    if datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") == str(endtime[0]).replace("_", " "):
                        self.c.execute(f"DELETE FROM mutes WHERE UserID={member.id}")

    @commands.command(name="unmute")
    @commands.has_permissions(mute_members=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, id=864582175470649344)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            embed = discord.Embed(description=f"{self.yes} **{member.display_name}#{member.discriminator} was unmuted.**",
                                  color=discord.Color.green())
            await ctx.send(embed=embed)
        self.c.execute(f"SELECT EXISTS (SELECT 1 FROM mutes WHERE UserID={member.id})")
        out = self.c.fetchone()
        exists = out[0]
        if exists == 1:
            self.c.execute(f"DELETE FROM mutes WHERE UserID={member.id}")
    """

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.kick(user=member, reason=reason)
        embed = discord.Embed(description=f"{self.yes} **{member.display_name}#{member.discriminator} was kicked.**",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await ctx.guild.ban(user=member, reason=reason)
        embed = discord.Embed(description=f"{self.yes} **{member.display_name}#{member.discriminator} was banned.**",
                              color=discord.Color.green())
        await ctx.send(embed=embed)

    @commands.command(name="purge")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, amount=10):
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)
        if amount == 1:
            embed = discord.Embed(description=f"{self.yes} **1 message was deleted.**", color=discord.Color.green())
        else:
            embed = discord.Embed(description=f"{self.yes} **{amount} messages were deleted.**", color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=3)

    @commands.Cog.listener()
    async def on_ready(self):
        for guild in self.bot.guilds:
            i = 0
            guild: discord.Guild
            for role in guild.roles:
                role: discord.Role
                if role.name == "Muted":
                    i += 1
                    await self.set_muted_role(role, guild)
            if i == 0:
                mutedRole = await guild.create_role(name="Muted")
                await self.set_muted_role(mutedRole, guild)

    async def set_muted_role(self, role: discord.Role, guild: discord.Guild):
        for channel in guild.text_channels:
            await channel.set_permissions(role, speak=False, send_messages=False, read_message_history=True, read_messages=False)
        err = False
        i = 1
        while not err:
            try:
                await role.edit(position=i + 1)
                await sleep(2)
            except HTTPException as e:
                err = True
                print(e)
                pass


def setup(bot):
    bot.add_cog(ModerationCog(bot))
