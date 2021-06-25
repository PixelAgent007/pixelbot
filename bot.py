#!/usr/bin/env python3
from discord import Colour, Embed
from discord.ext import commands
from configparser import ConfigParser

# Reading config
config = ConfigParser()
config.read('config.ini')


TOKEN = "ODQ4ODE2OTE1NTc3MDQ1MDAy.YLSIWg.P8tG8F3hbAzfbNQLCk0mn0OdY9I"
# Defining Bot
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print('Bot connected to Discord!')


@bot.command(name='beta')
async def join_beta(ctx):
    embed = Embed(
        title="Public Beta",
        colour=Colour(0x71368a),
        description="**IP**: `play.minecraft-newlife.de`"
    )
    embed.add_field(name="**# Manual Installation**:", value="""
    Downloading and installing into the Minecraft Launcher. If you don't know how to install fabric modpacks, maybe try the Technic Method instead.

    Download Optifine Edition *(Worse Performance, but there are Shaders and Zoom)*:
    https://play.minecraft-newlife.de/index.php/s/nbG3CgEScKSktJE
    Download Sodium Edition *(Better FPS / Performance)*:
    https://play.minecraft-newlife.de/index.php/s/c5aNB5KjLdBbmzb
    """, inline=False)
    embed.add_field(name="**# Installation using Technic Launcher**", value="""
    If you don't want to install the modpack manually, you can install it using the Technic Launcher. 

    Head over to https://www.technicpack.net/download to download it. Even though it says something about installing, you have to keep the .exe file, because it starts the launcher. But, no worries. If you ever accidentally delete it, you can just redownload it. 

    Then, log in with your Mojang / Microsoft account. Head over to the Modpack Section, and search for *DarkMoonSMP*. Choose either the Optifine or Sodium Version, and click Install.
    """, inline=False)
    embed.add_field(name="**# Installation using MMC**", value="""
    *Note: This* ***requires*** *atleast MultiMC 5 Version 0.6.12. If your MMC is older, update using the update button or reinstall.*

    To install the Modpack into MMC, open up MMC and click *Add instance*, Head over to the technic section and search up DarkMoonSMP. Choose either the Sodium or Optifine Version, press Ok and wait for it to download,
    """, inline=False)
    embed.add_field(name="Help", value="If you need help installing the modpack, feel free to ask in `#modpack-support`", inline=False)
    return await ctx.send(embed=embed)


@bot.command(name='rules')
async def send_rules(ctx):
    embed = Embed(
        title="Public Beta Rules",
        colour=Colour(0x71368a),
        description=""
    )
    embed.add_field(name="Rule 1:", value="Behave. All other players are also **real** humans with **real** feelings.", inline=False)
    embed.add_field(name="Rule 2:", value="No lag machines. Building a lag machine = Ban", inline=False)
    embed.add_field(name="Rule 3:", value="If farms cause lag, they will be turned off by admins, if you dont turn them off yourself. **You will not be refunded any materials.**", inline=False)
    embed.add_field(name="Rule 4:", value="You wont be refunded anything caused by trolls, scams, raids etc.", inline=False)
    embed.add_field(name="Rule 5", value="**Set your render distance to 8!** It really helps with server lag and is a necessary step against lag.", inline=False)
    embed.add_field(name="Rule 6:", value="If you spawn camp, you get kicked and warned.", inline=False)
    embed.add_field(name="Rule 7:", value="If someone is X-Raying or hacking, they get banned for 7 days, then a month, then a year, and if they keep hacking they get perma-banned.", inline=False)
    return await ctx.send(embed=embed)


@bot.command(name='debug')
async def debug_steps(ctx):
    embed = Embed(
        title="Debugging Steps for the Modpack",
        colour=Colour(0x71368a),
        description="If the modpack crashes / doesn't start, please describe your problem using the following debug steps and post them in `#modpack-support`."
    )
    embed.add_field(name="Step 1", value="Describe the problem.", inline=False)
    embed.add_field(name="Step 2", value="Take screenshots and/or get logs.", inline=False)
    embed.add_field(name="Step 3", value="Post following info: *Launcher / Client used*, *OS with version* and *amount of RAM allocated (if you don't know, what that is, you can safely ignore it)*", inline=False)
    embed.add_field(name="This information", value="You can get this info by typing `!debug`", inline=False)
    return await ctx.send(embed=embed)

@bot.command(name='claiming')
async def claiming_help(ctx):
    embed = Embed(
            title="Claiming Land",
            colour=Colour(0x71368a),
            description="Claiming is done server-side using the Fabric-LanD Mod. You need a *golden hoe* to claim land. Every player has 500 blocks available to claim."
    )
    embed.add_field(name="Claim Land: ", value="Right-Click with a golden hoe, **OR** `/flan addClaim <x> <y> <z>`", inline=False)
    embed.add_field(name="Open up the claiming menu: ", value="`/flan claim`", inline=False)
    embed.add_field(name="Delete a claim: ", value="`/flan delete`", inline=False)
    embed.add_field(name="Delete all claims: ", value="`/flan deleteAll`", inline=False)
    embed.add_field(name="Trust a player: ", value="you can find it inside of the Menu", inline=False)
    return await ctx.send(embed=embed)


bot.run(TOKEN)
