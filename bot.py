#    Pixel Bot by PixelAgent007
#    Simple discord bot built with discord.py for QOL and Moderation purposes.
#    Copyright (C) 2021  Oskar Manhart
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import asyncio
import discord
from discord import Colour, Embed
from discord.ext import commands
from discord.utils import get
from discord_slash import SlashCommand
import json

# Setting activity
activity = discord.Game(name="/help for Help")

# Defining Bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="", activity=activity, status=discord.Status.online, intents=intents, owner_id=487247155741065229)
bot.remove_command("help")
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

# Reading config
with open('config/settings.json', 'r') as f:
    bot.config = json.load(f)

# Getting vars from config
token = bot.config["GLOBAL"]["TOKEN"]
prefix = bot.config["GLOBAL"]["PREFIX"]
bot.command_prefix = prefix

# Loading extensions
initial_extensions = [
    "lib.cogs.serverinfo",
    "lib.cogs.help",
    "lib.cogs.suggestions",
    "lib.cogs.moderation",
    "lib.cogs.rickrolling",
    "lib.cogs.leveling"
]
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

@bot.event
async def on_ready():
    print("Bot connected to Discord!")

@bot.event
async def on_member_join(member):
    if member.guild.id == 849223970598420480 and not member.bot:
        name = member.name
        role = member.guild.get_role(864783434151624704)
        await member.add_roles(role)
        embed = Embed(title=f"Welcome, {name}!", colour=Colour(0x71368a), description="""
        Welcome to the Dark Moon SMP!
        
        Please read the `#rules` and if you want to join the official server, check `#server` on how to join. Have a great time!
        """)
        await member.send(embed=embed)
    if member.guild.id == 849223970598420480 and member.bot:
        role = member.guild.get_role(850837927642005524)
        await member.add_roles(role)


bot.run(token)