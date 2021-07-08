import asyncio
import discord
from discord import Colour, Embed, Member
from discord.ext import commands
from configparser import ConfigParser

# Reading config
config = ConfigParser()
config.read("config.ini")

# Getting vars
token = config.get('Global', 'token')
prefix = config.get('Global', 'prefix')
players = {}

# Setting activity
activity = discord.Game(name="!help")

# Defining Bot
bot = commands.Bot(command_prefix=prefix, activity=activity, status=discord.Status.online)
bot.remove_command("help")

# Loading extensions
initial_extensions = [
    "cogs.darkmoon",
    "cogs.fun",
    "cogs.music"
]
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Bot connected to Discord!")
    # Role on Reaction -- Currently disabled
    '''
    channel = bot.get_channel(862411238351831060)
    embed = Embed(title="Special Roles", colour=Colour(0x71368a), description="React to this message with the specified emoji to get a specific role.")
    embed.add_field(name="Announcement Pings", value="React with 🏓(`:ping_pong:`) to get the Role.", inline=True)
    oldmsg = await channel.history().get()
    await oldmsg.delete()
    msg = await channel.send(embed=embed)
    role = discord.utils.get(channel.guild.roles, name="Announcement Ping")
    while True:
        reaction, user = await bot.wait_for('reaction_add')
        user: Member
        if reaction.emoji == "🏓":
            await user.add_roles(user, role)
    '''



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

        Help Page 4/{pages}"""
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