from discord import Colour, Embed
from discord.ext import commands
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option, create_choice

class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="debug")
    async def debug_steps(self, ctx):
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

    @cog_ext.cog_slash(name="modpack", description="Shows info on how to install the mods.", 
        options=[
            create_option(
                name="type",
                description="Technic | MultiMC | Manual",
                option_type=3,
                required=True
             )
             ])
    async def modpack_info(self, ctx, type: str):
        mmcEmbed = Embed(title="Modpack Installation using MultiMC", colour=Colour(0x71368a), description="**IP**: `darkmoonsmp.duckdns.org:25635`")
        mmcEmbed.add_field(name="**# Installation using MMC**", value="""
        *Note: This* ***requires*** *at least MultiMC 5 Version 0.6.12. If your MMC is older, update using the update button or reinstall.*

        To install the Modpack into MMC, open up MMC and click *Add instance*, Head over to the technic section and 
        search up DarkMoonSMP. Choose either the Sodium or Optifine Version, press Ok and wait for it to download, 
        """, inline=False)

        manualEmbed = Embed(title="Manual Installation of the Modpack", colour=Colour(0x71368a), description="**IP**: `darkmoonsmp.duckdns.org:25635`")
        manualEmbed.add_field(name="**# Manual Installation**:", value="""Downloading and installing into the Minecraft 
        Launcher. If you don't know how to install fabric modpacks, maybe try the Technic Method instead. 

        Download Optifine Edition *(Worse Performance, but there are Shaders and Zoom)*:
        http://play.minecraft-newlife.de/darkmoonsmp/Dark%20Moon%20SMP%20Modpack%20(Optifine).zip
        Download Sodium Edition *(Better FPS / Performance)*:
        http://play.minecraft-newlife.de/darkmoonsmp/Dark%20Moon%20SMP%20Modpack%20(Sodium).zip
        """, inline=False)
        technicEmbed = Embed(title="Modpack Installation using Technic Launcher", colour=Colour(0x71368a), description="**IP**: `darkmoonsmp.duckdns.org:25635`")
        technicEmbed.add_field(name="**# Installation using Technic Launcher**", value="""
        If you don't want to install the modpack manually, you can install it using the Technic Launcher. 

        Head over to https://www.technicpack.net/download to download it. Even though it says something about installing, 
        you have to keep the .exe file, because it starts the launcher. But, no worries. If you ever accidentally delete 
        it, you can just redownload it. 

        Then, log in with your Mojang / Microsoft account. Head over to the Modpack Section, and search for *DarkMoonSMP*. 
        Choose either the Optifine or Sodium Version, and click Install.
        """, inline=False)
        manualEmbed.add_field(name="Help", value="If you need help installing the modpack, feel free to ask in `#modpack-support`", inline=False)
        mmcEmbed.add_field(name="Help", value="If you need help installing the modpack, feel free to ask in `#modpack-support`", inline=False)
        technicEmbed.add_field(name="Help", value="If you need help installing the modpack, feel free to ask in `#modpack-support`", inline=False)

        if type.lower == "mmc" or "multimc":
            embed = mmcEmbed
        elif type.lower == "technic" or "techniclauncher":
            embed = technicEmbed
        elif type.lower == "manual" or "fabric":
            embed = manualEmbed

        return await ctx.send(embed=embed)

    @cog_ext.cog_slash(name="ignrules", description="Shows Rules for the minecraft server.")
    async def send_rules(self, ctx):
        embed = Embed(
            title="Ingame Rules",
            colour=Colour(0x71368a),
            description=""
        )
        embed.add_field(name="Rule 1:", value="Behave. All other players are also **real** humans with **real** feelings.", inline=False)
        embed.add_field(name="Rule 2:", value="No lag machines. Building a lag machine = Ban", inline=False)
        embed.add_field(name="Rule 3:", value="If farms cause lag, they will be turned off by admins, if you dont turn them off yourself. **You will not be refunded any materials.**", inline=False)
        embed.add_field(name="Rule 4:", value="You wont be refunded anything caused by trolls, scams, raids etc.", inline=False)
        embed.add_field(name="Rule 5", value="**Set your render distance to 8!** It really helps with server lag and is a necessary step against lag.", inline=False)
        embed.add_field(name="Rule 6:", value="If you spawn camp, you get kicked and warned.", inline=False)
        embed.add_field(name="Rule 7:", value="If someone is X-Raying or hacking, they get banned for 7 days. If they keep hacking then they get banned for a month, then a year, and if they still keep hacking they get perma-banned.", inline=False)
        return await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(InfoCog(bot))
