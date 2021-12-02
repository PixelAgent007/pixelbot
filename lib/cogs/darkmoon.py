import asyncio

from discord import Colour, Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from discord import TextChannel
import discord


class DarkmoonCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Registered Darkmoon Cog")

    @cog_ext.cog_slash(name="debug", description="Shows help on how to debug the modpack.",
                       guild_ids=[906804682452779058])
    async def debug_steps(self, ctx):
        debugChannel: TextChannel = discord.utils.get(ctx.guild.text_channels, id=906922845404274689)
        embed = Embed(
            title="Debugging Steps for the Modpack",
            colour=Colour(0x71368a),
            description=f"If the modpack crashes / doesn't start, please describe your problem using the following debug steps and post them in {debugChannel.mention}."
        )
        embed.add_field(name="Step 1", value="Describe the problem.", inline=False)
        embed.add_field(name="Step 2", value="Take screenshots and/or get logs.", inline=False)
        embed.add_field(name="Step 3",
                        value="Post following info: *Launcher / Client used*, *OS with version* and *amount of RAM allocated (if you don't know, what that is, you can safely ignore it)*",
                        inline=False)
        embed.add_field(name="This information", value="You can get this info by typing `/debug`", inline=False)
        return await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="server", description="Shows important information like IP, Server version etc.",
                       guild_ids=[906804682452779058])
    async def serverinfo(self, ctx):
        serverChannel: TextChannel = discord.utils.get(ctx.guild.text_channels, id=906824675525537823)
        embed = Embed(
            title="Server Info",
            colour=Colour(0x71368a),
            description=f"Check {serverChannel.mention} on how to install the modpack"
        )
        embed.add_field(name="IP:", value="mc.oskar.global", inline=False)
        embed.add_field(name="Version:", value="1.17.1 - Fabric", inline=False)
        embed.add_field(name="Implemented Datapacks *(currently outdated)*:",
                        value="https://docs.google.com/document/d/1OhRB2pyAqVy8mNCKSw0AZkHZu6eRu0BUYEYrFr3OoHw/edit?usp=sharing",
                        inline=False)
        embed.add_field(name="This information", value="You can get this info by typing `/server`", inline=False)
        return await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="modpack", description="Shows info on how to install the mods.",
                       options=[
                           create_option(
                               name="type",
                               description="Technic | MultiMC | Manual",
                               option_type=3,
                               required=True
                           )
                       ], guild_ids=[906804682452779058])
    async def modpack_info(self, ctx, type: str):
        debugChannel: TextChannel = discord.utils.get(ctx.guild.text_channels, id=906922845404274689)
        mmcEmbed = Embed(title="Modpack Installation using MultiMC", colour=Colour(0x71368a),
                         description="**IP**: `mc.oskar.global`")
        mmcEmbed.add_field(name="**# Installation using MMC**", value="""
        *Note: This* ***requires*** *at least MultiMC 5 Version 0.6.12. If your MMC is older, update using the update button or reinstall.*

        To install the Modpack into MMC, open up MMC and click *Add instance*, Head over to the technic section and 
        search up *DarkMoonSMP*. Click on the top result, press Ok and wait for it to download.
        """, inline=False)

        manualEmbed = Embed(title="Manual Installation of the Modpack", colour=Colour(0x71368a),
                            description="**IP**: `mc.oskar.global`")
        manualEmbed.add_field(name="**# Manual Installation**:", value="""Downloading and installing into the Minecraft 
        Launcher. If you don't know how to install fabric modpacks, maybe try the Technic Method instead. 

        Download:
        https://bit.ly/3ke4xPq
        """, inline=False)
        technicEmbed = Embed(title="Modpack Installation using Technic Launcher", colour=Colour(0x71368a),
                             description="**IP**: `mc.oskar.global`")
        technicEmbed.add_field(name="**# Installation using Technic Launcher**", value="""
        If you don't want to install the modpack manually, you can install it using the Technic Launcher. 

        Head over to https://www.technicpack.net/download to download it. Even though it says something about installing, 
        you have to keep the .exe / .jar file, because it starts the launcher. But, no worries. If you ever accidentally delete 
        it, you can just redownload it. 

        Then, log in with your Mojang / Microsoft account. Head over to the Modpack Section, and search for *DarkMoonSMP*, click on the top search result and click Install.
        """, inline=False)
        manualEmbed.add_field(name="Help",
                              value=f"If you need help installing the modpack, feel free to ask in {debugChannel.mention}",
                              inline=False)
        mmcEmbed.add_field(name="Help",
                           value=f"If you need help installing the modpack, feel free to ask in {debugChannel.mention}",
                           inline=False)
        technicEmbed.add_field(name="Help",
                               value=f"If you need help installing the modpack, feel free to ask in {debugChannel.mention}",
                               inline=False)

        if type.lower() == "mmc":
            await ctx.send(embed=mmcEmbed)
        elif type.lower() == "technic":
            await ctx.send(embed=technicEmbed)
        elif type.lower() == "manual":
            await ctx.send(embed=manualEmbed)

        return True

    @cog_ext.cog_slash(name="ignrules", description="Shows rules for the minecraft server",
                       guild_ids=[906804682452779058])
    async def send_rules(self, ctx):
        embed = Embed(
            title="Ingame Rules",
            colour=Colour(0x71368a),
            description=""
        )
        embed.add_field(name="Rule 1:", value="No lag machines. Lag machines will result in a immediate ban. Also, don't try it. The server will instantly restart.", inline=False)
        embed.add_field(name="Rule 2:",
                        value="No hacking, this includes X-Raying, Baritone, Duping, Fly-Hacks, Speedhacks, Mobradars, Killaura **and lagswitching.**",
                        inline=False)
        embed.add_field(name="Rule 3:",
                        value="If farms cause lag, they will be removed by admins, if you don't turn them off yourself. **You will not be refunded any materials.**",
                        inline=False)
        embed.add_field(name="Rule 4:",
                        value="Be nice. Killing other players for no reason is forbidden, but you won't be refunded anything.",
                        inline=False)
        embed.add_field(name="Rule 5",
                        value="**Set your render distance to a maximum of 10!** It really helps with server lag and is a necessary step against lag.",
                        inline=False)
        embed.add_field(name="Rule 6:", value="If you spawn camp, you get kicked and warned.", inline=False)
        embed.add_field(name="Note:",
                        value="Punishments may vary depending on the situation, but general punishments include kicks, bans, tempbans and **inventory / playerdata wipes**. It is also possible that a mod / admin will watch you if they think you're doing something suspicious. Please also note that bases may removed incase of duping.",
                        inline=False)
        return await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="pingyogd", description="Ping the co-owner",
                       guild_ids=[906804682452779058])
    async def mass_ping_yogd(self, ctx):
        if not ctx.author.id == 487247155741065229:
            return False
        member: discord.Member = discord.utils.get(ctx.guild.members, id=685771268988993548)

        for i in range(10):
            await ctx.send(f"{member.mention}")
            await asyncio.sleep(0.1)
        return True

    @cog_ext.cog_slash(name="pinggod", description="Ping le owner",
                       guild_ids=[906804682452779058])
    async def mass_ping_me(self, ctx):
        if not ctx.author.id == 487247155741065229:
            return False
        member: discord.Member = discord.utils.get(ctx.guild.members, id=487247155741065229)

        for i in range(10):
            await ctx.send(f"{member.mention}")
            await asyncio.sleep(0.1)
        return True


def setup(bot):
    bot.add_cog(DarkmoonCog(bot))
