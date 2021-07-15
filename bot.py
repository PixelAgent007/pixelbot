import asyncio
import discord
from discord import Colour, Embed
from discord.ext import commands
from configparser import ConfigParser
import json

# Setting activity
activity = discord.Game(name="!help for Help")

# Defining Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", activity=activity, status=discord.Status.online, intents=intents)
bot.remove_command("help")

# Reading config
with open('settings.json', 'r') as f:
    bot.config = json.load(f)

# Getting vars from config
token = bot.config["GLOBAL"]["TOKEN"]
prefix = bot.config["GLOBAL"]["PREFIX"]
bot.command_prefix = prefix

# Loading extensions
initial_extensions = [
    "cogs.darkmoonsmp",
    "cogs.rickrolling",
    "cogs.suggestions"
]
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


async def add_guild():
    if not "GUILDS" in bot.config:
            bot.config["GUILDS"] = {}
    for guild in bot.guilds:
        gid = str(guild.id)
        if gid not in bot.config["GUILDS"]:
            bot.config["GUILDS"][gid] = {
            "TOGGLED": "ON",
            "OUTPUT": None,
            "ID": "1"
            }
            print(f"Added new server to the config file ({guild.name})")
            with open('settings.json', 'w') as f:
                json.dump(bot.config, f, indent=2)


@bot.event
async def on_ready():
    print("Bot connected to Discord!")
    # await add_guild()


@bot.event
async def on_member_join(member):
    if member.guild.id == 849223970598420480:
        name = member.name
        role = member.guild.get_role()
        await member.add_roles(role)
        embed = Embed(title=f"Welcome, {name}!", colour=Colour(0x71368a), description="""
        Welcome to the Dark Moon SMP!
        
        Please read the `#rules` and if you want to join the beta server, check `#public-beta`. Have a great time!
        """)
        await member.send(embed=embed)

@bot.command(name="help")
async def help(ctx):
    cur_page = 1
    pages = 6
    contents = [
        f"""
        Shows information about the public beta and on the installation of the modpack.
        
        Syntax: 
        `!beta`
        
        Help Page 1/{pages}""",
        f"""
        Shows the rules. Read them carefully, because ***by playing on the server you automatically agree to them.*** 
                
        Syntax: 
        `!rules`
        
        Help Page 2/{pages}""",
        f"""
        Shows information on how to debug the modpack and ask for support in *#modpack-support*.
                
        Syntax: 
        `!debug`
        
        Help Page 3/{pages}""",
        f"""
        Shows information on how to claim land ingame.

        Syntax: 
        `!claiming`

        Help Page 4/{pages}""",
        f"""
        Make a suggestion in `#suggestions`. The bot will start asking you questions, that you just have to answer.

        Syntax: 
        `!suggest`

        Help Page 5/{pages}"""
    ]
    titles = [
        "Public Beta / Modpack",
        "Rules",
        "Debugging / Modpack Support",
        "Claiming Land"
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
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            elif str(reaction.emoji) == "◀️" and cur_page > 1:
                cur_page -= 1
                embed = Embed(
                    title=titles[cur_page - 1],
                    colour=Colour(0x71368a),
                    description=contents[cur_page - 1]
                )
                await message.edit(embed=embed)
                await message.remove_reaction(reaction, user)
            else:
                await message.remove_reaction(reaction, user)
        except asyncio.TimeoutError:
            await message.delete()
            break


bot.run(token)