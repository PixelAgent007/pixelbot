from discord import Colour, Embed
from discord.ext import commands
import discord
import asyncio
import json
from sqlite3 import connect
from random import randint
from discord_slash import cog_ext
from discord_slash.utils.manage_commands import create_option
from disrank.generator import Generator

class LevelCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    conn = connect("config/db/database.db", check_same_thread=False)
    c = conn.cursor()

    async def update_data(self, user):
        self.c.execute(f"SELECT EXISTS (SELECT 1 FROM exp WHERE UserID={user.id})")
        out = self.c.fetchone()
        exists = out[0]
        if exists == 0:
            self.c.execute(f"INSERT INTO exp (UserID, XP, CurXP, Level) VALUES({user.id}, 0, 0, 1)")
        self.conn.commit()
    
    async def add_experience(self, user):
        self.c.execute(f"SELECT CurXP FROM exp WHERE UserID = {user.id}")
        tupxp = self.c.fetchone()
        xp = tupxp[0]
        self.c.execute(f"SELECT Level FROM exp WHERE UserID = {user.id}")
        tuplvl = self.c.fetchone()
        lvl = tuplvl[0]
        newxp = int(lvl * 15)
        lvl5 = user.guild.get_role(870222636314144789)
        lvl10 = user.guild.get_role(864582399957794866)
        lvl15 = user.guild.get_role(870222736365088808)
        lvl20 = user.guild.get_role(870222859220434954)
        lvl35 = user.guild.get_role(870222947258859600)
        lvl50 = user.guild.get_role(870223127848812594)
        lvl75 = user.guild.get_role(870223219804749844)
        lvl100 = user.guild.get_role(849948038852247562)

        self.c.execute(f"UPDATE exp SET XP = XP + 1, CurXP = CurXP + 1 WHERE UserID = {user.id}")
        if newxp == xp:
            lvl += 1
            self.c.execute(f"UPDATE exp SET Level = Level + 1, CurXP = 0 WHERE UserID = {user.id}")
            embed = Embed(title="Level Up!", color=Colour(0x71368a), description=f"{user.mention} reached Level {lvl:,}, GG!")
            await self.channel.send(embed=embed)
            if lvl == 5:
                await user.add_roles(lvl5)
            elif lvl == 10:
                await user.add_roles(lvl10)
                await user.remove_roles(lvl5)
            elif lvl == 15:
                await user.add_roles(lvl15)
                await user.remove_roles(lvl10)
            elif lvl == 20:
                await user.add_roles(lvl20)
                await user.remove_roles(lvl15)
            elif lvl == 35:
                await user.add_roles(lvl35)
                await user.remove_roles(lvl20)
            elif lvl == 50:
                await user.add_roles(lvl50)
                await user.remove_roles(lvl35)
            elif lvl == 75:
                await user.add_roles(lvl75)
                await user.remove_roles(lvl50)
            elif lvl == 100:
                await user.add_roles(lvl100)
                await user.remove_roles(lvl75)
        self.conn.commit()

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

    @cog_ext.cog_slash(name="rank", description="Shows your level. If another member is specified as the first arg, his is shown", 
    options=[
        create_option(
            name="member", 
            description="Specify the member whose rank you want to know.", 
            option_type=6, 
            required=False
            )
        ], 
    guild_ids=[849223970598420480])
    async def show_rank(self, ctx, member: discord.Member = None):
        if not member:
            await self.update_data(ctx.author)
            self.c.execute(f"SELECT Level FROM exp WHERE UserID = {ctx.author.id}")
            tuplvl = self.c.fetchone()
            lvl = tuplvl[0]
            self.c.execute(f"SELECT CurXP FROM exp WHERE UserID = {ctx.author.id}")
            tupxp = self.c.fetchone()
            xp = tupxp[0]
            self.c.execute("SELECT UserID FROM exp ORDER BY XP DESC")
            members = self.c.fetchall()
            userid = tuple([ctx.author.id])
            index = members.index(userid)
            rank = int(index + 1)
            args = {
	            'bg_image' : 'https://www.technistone.com/color-range/image-slab/Starlight%20Black_SLAB_web.jpg',
	            'profile_image' : f'{ctx.author.avatar_url}',
	            'level' : lvl,
	            'current_xp' : xp,
	            'user_xp' : xp,
	            'next_xp' : int(lvl * 15),
	            'user_position' : rank,
	            'user_name' : f'{ctx.author.name}',
	            'user_status' : 'online',
            }
            rankcard = Generator().generate_profile(**args)
            file = discord.File(fp=rankcard, filename='rankcard.png')
            await ctx.send(file=file)
        if member:
            await self.update_data(member)
            self.c.execute(f"SELECT Level FROM exp WHERE UserID = {member.id}")
            tuplvl = self.c.fetchone()
            lvl = tuplvl[0]
            self.c.execute(f"SELECT CurXP FROM exp WHERE UserID = {member.id}")
            tupxp = self.c.fetchone()
            xp = tupxp[0]
            self.c.execute("SELECT UserID FROM exp ORDER BY XP DESC")
            members = self.c.fetchall()
            userid = tuple([member.id])
            index = members.index(userid)
            rank = int(index + 1)
            print(rank)
            args = {
	            'bg_image' : 'https://www.technistone.com/color-range/image-slab/Starlight%20Black_SLAB_web.jpg',
	            'profile_image' : f'{member.avatar_url}',
	            'level' : lvl,
	            'current_xp' : xp,
	            'user_xp' : xp,
	            'next_xp' : int(lvl * 15),
	            'user_position' : rank,
	            'user_name' : f'{member.name}',
	            'user_status' : 'online',
            }
            rankcard = Generator().generate_profile(**args)
            file = discord.File(fp=rankcard, filename='rankcard.png')
            await ctx.send(file=file)

def setup(bot):
    bot.add_cog(LevelCog(bot))