import discord
import asyncio
from discord import Colour, Embed
from discord.ext import commands
from configparser import ConfigParser

# Reading config
config = ConfigParser()
config.read('config.ini')

# Getting vars
token = config.get('Global', 'token')
prefix = config.get('Global', 'prefix')

# Setting activity
activity = discord.Game(name="!help")

# Defining Bot
bot = commands.Bot(command_prefix=prefix, activity=activity, status=discord.Status.online)
bot.remove_command("help")

# Loading extensions
initial_extensions = [
    "cogs.darkmoon"
]
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print('Bot connected to Discord!')


@bot.command(name="help")
async def help(ctx):
    pages = 4
    cur_page = 1
    contents = [
        f"""
        Shows information about the public beta and on the installation of the modpack.
        
        Syntax: 
        `!beta`
        
        Help Page {cur_page}/{pages}""",
        f"""
        Shows the rules. Read them carefully, because ***by playing on the server you automatically agree to them.*** 
                
        Syntax: 
        `!rules`
        
        Help Page {cur_page}/{pages}""",
        f"""
        Shows information on how to debug the modpack and ask for support in *#modpack-support*.
                
        Syntax: 
        `!debug`
        
        Help Page {cur_page}/{pages}""",
        f"""
        Shows information on how to claim land ingame.

        Syntax: 
        `!claiming`

        Help Page {cur_page}/{pages}"""
    ]
    titles = [
        "Public Beta / Modpack",
        "Rules",
        "Debugging / Modpack Support",
        "Claiming Land",
    ]
    embed = Embed(
        title=titles[cur_page-1],
        colour=Colour(0x71368a),
        description=contents[cur_page-1]
    )
    message = await ctx.send(embed=embed)

    await message.add_reaction("◀️")
    await message.add_reaction("▶️")

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            if str(reaction.emoji) == "▶️" and cur_page != pages:
                cur_page += 1
                embed = Embed(
                    title=titles[cur_page - 1],
                    colour=Colour(0x71368a),
                    description=contents[cur_page - 1]
                )
                message = await ctx.send(embed=embed)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                embed = Embed(
                    title=titles[cur_page - 1],
                    colour=Colour(0x71368a),
                    description=contents[cur_page - 1]
                )
                message = await ctx.send(embed=embed)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break


bot.run(token)