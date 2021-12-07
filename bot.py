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

import json
import discord
import mysql.connector
from discord_slash import SlashCommand
from discord.ext import commands

# Defining Bot
intents = discord.Intents.all()
activity = discord.Game(name="on the Dark Moon SMP")

bot = commands.Bot(command_prefix="", activity=activity, status=discord.Status.online, intents=intents,
                   owner_id=487247155741065229)
slash = SlashCommand(bot, sync_commands=True, sync_on_cog_reload=True)

# Removing default help command
bot.remove_command("help")

# Loading DB
with open('config/database.json', 'r') as f:
    dbcfg = json.load(f)

conn = mysql.connector.connect(host=dbcfg["DB"]["HOST"], user=dbcfg["DB"]["USER"], password=dbcfg["DB"]["PASSWORD"],
                               db=dbcfg["DB"]["DBNAME"], port=dbcfg["DB"]["PORT"])
c = conn.cursor()
c.execute(f"SELECT Token FROM globalSettings")
token = c.fetchone()[0]
c.execute(f"SELECT Prefix FROM globalSettings")
prefix = c.fetchone()[0]

# Getting vars from config
bot.command_prefix = prefix

# Loading extensions
initial_extensions = [
    "lib.cogs.suggestions",
    "lib.cogs.moderation",
    "lib.cogs.darkmoon",
    #"lib.cogs.leveling",
    "lib.cogs.utils",
    "lib.cogs.rickrolling"
]
if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.event
async def on_ready():
    print("Bot connected to Discord!")


bot.run(token)
