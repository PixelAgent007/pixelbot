from discord import Colour, Embed
from discord.ext import commands
import discord
import asyncio
import json
from db import db
from random import randint

class LevelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def update_data(self, user):
        if not db.record("SELECT EXISTS (SELECT 1 FROM exp WHERE UserID=?))", user.id) == True:
            db.execute("INSERT INTO exp (UserID, XP, Level) VALUES(?, 0, 1)", user.id)
    
    async def add_experience(self, user):
        xp = int(db.record("SELECT XP FROM exp WHERE UserID = ?", user.id))
        lvl = int(db.record("SELECT Level FROM exp WHERE UserID = ?", user.id))
        xp_to_add = randint(10, 20)
        new_lvl = int(((xp+xp_to_add)//42) ** 0.55)

        db.execute("UPDATE exp SET XP = XP + ?, Level = ? WHERE UserID = ?", xp_to_add, new_lvl, user.id)
        if new_lvl > lvl:
            embed = Embed(title="Level Up!", color=Colour(0x71368a), description=f"{user.mention} reached Level {new_lvl:,}, GG!")
            await self.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        if not member.bot:
            await self.update_data(member)

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            await self.update_data(message.author)
            await self.add_experience(message.author)

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = discord.utils.get(self.bot.guilds, id=849223970598420480)
        self.channel = discord.utils.get(self.guild.text_channels, id=865541313717731389)

        for member in self.guild.members:
            if not member.bot:
                await self.update_data(member)


def setup(bot):
    bot.add_cog(LevelCog(bot))