from discord import Colour, Embed
from discord.ext import commands
import discord
import asyncio
from sqlite3 import connect
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import SlashCommandPermissionType
import re

time_regex = re.compile("(?:(\d{1,5})(h|s|m|d))+?")
time_dict = {"h": 3600, "s": 1, "m": 60, "d": 86400}

class TimeConverter(commands.Converter):
    async def convert(self, ctx, argument):
        args = argument.lower()
        matches = re.findall(time_regex, args)
        time = 0
        for key, value in matches:
            try:
                time += time_dict[value] * float(key)
            except KeyError:
                raise commands.BadArgument(
                    f"{value} is an invalid time key! h|m|s|d are valid arguments"
                )
            except ValueError:
                raise commands.BadArgument(f"{key} is not a number!")
        return round(time)

class ModerationCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    conn = connect("config/db/database.db", check_same_thread=False)
    c = conn.cursor()


    @cog_ext.cog_slash(name="mute",
            description="Mute a member.",
            permissions={
                849223970598420480: [
                    create_permission(849956089989955584, SlashCommandPermissionType.ROLE, True)
                ]
            },
            options=[
                create_option(
                    name="member",
                    description="Specify the member to mute.",
                    option_type=6,
                    required=True
                ),
                create_option(
                    name="time",
                    description="Specify the time how long to mute the member.",
                    option_type=3,
                    required=False
                )
            ]
    )
    async def mute(self, ctx, member: discord.Member, time: TimeConverter=None):
        muted_role = discord.utils.get(ctx.guild.roles, id=864582175470649344)

        if not time:
            await member.add_roles(muted_role)
            notimeEmbed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted successfully.**", color=discord.Color.green())
            await ctx.send(embed=notimeEmbed)
        else:
            minutes, seconds = divmod(time, 60)
            hours, minutes = divmod(minutes, 60)
            if int(hours):
                await member.add_roles(muted_role)
                hrEmbed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted for {hours} hours, {minutes} minutes and {seconds} seconds.**", color=discord.Color.green())
                await ctx.send(embed=hrEmbed)
            elif int(minutes):
                await member.add_roles(muted_role)
                minEmbed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted for {minutes} minutes and {seconds} seconds.**", color=discord.Color.green())
                await ctx.send(embed=minEmbed)
            elif int(seconds):
                await member.add_roles(muted_role)
                secEmbed = discord.Embed(description=f"✅ **{member.display_name}#{member.discriminator} was muted for {seconds} seconds.**", color=discord.Color.green())
                await ctx.send(embed=secEmbed)
        if time and time < 300:
            await member.add_roles(muted_role)
            await asyncio.sleep(time)

            if muted_role in member.roles:
                await member.remove_roles(muted_role)
                embed = discord.Embed(description=f"**{member.display_name}#{member.discriminator} was unmuted.**", color=discord.Color.green())
                await ctx.send(embed=embed)

            self.c.execute(f"SELECT EXISTS (SELECT 1 FROM mutes WHERE UserID={member.id})")
            out = self.c.fetchone()
            exists = out[0]
            if exists == 1:
                self.c.execute(f"DELETE FROM exp WHERE UserID={member.id}")
        self.conn.commit()

    @cog_ext.cog_slash(name="unmute",
            description="Unmute a member.",
            permissions={
                849223970598420480: [
                    create_permission(849956089989955584, SlashCommandPermissionType.ROLE, True)
                ]
            },
            options=[
                create_option(
                    name="member",
                    description="Specify the member to mute.",
                    option_type=6,
                    required=True
                )
            ]
    )
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, id=864582175470649344)
        if muted_role in member.roles:
            await member.remove_roles(muted_role)
            embed = discord.Embed(description=f"**{member.display_name}#{member.discriminator} was unmuted.**", color=discord.Color.green())
            await ctx.send(embed=embed)
        self.c.execute(f"SELECT EXISTS (SELECT 1 FROM mutes WHERE UserID={member.id})")
        out = self.c.fetchone()
        exists = out[0]
        if exists == 1:
            self.c.execute(f"DELETE FROM exp WHERE UserID={member.id}")

def setup(bot):
    bot.add_cog(ModerationCog(bot))