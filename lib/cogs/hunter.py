import json
import discord

from discord.ext import commands, tasks

with open('config/config.json', 'r') as f:
    config = json.load(f)


class HunterCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("Registered yogd hunting Cog")

    @commands.command(name="check")
    async def check(self, ctx):
        await ctx.message.delete()
        member = self.bot.get_guild(906804682452779058).get_member(config["memberID"])
        name = member.name + "#" + member.discriminator
        channel = self.bot.get_guild(906804682452779058).get_channel(906804682452779062)
        if not config["name"] == name:
            with open('config.json', 'w') as f:
                config["name"] = name
                config["names"].append(name)
                json.dump(config, f, indent=4)
                embed = discord.Embed(title="He did it again!", description=f"New Name: {name}",
                                      color=discord.Color.red())
                await channel.send(content=f"@here", allowed_mentions=discord.AllowedMentions(everyone=True))
                await channel.send(embed=embed)

    @tasks.loop(hours=1)
    async def check(self):
        member = self.bot.get_guild(906804682452779058).get_member(config["memberID"])
        name = member.name + "#" + member.discriminator
        channel = self.bot.get_guild(906804682452779058).get_channel(906804682452779062)
        if not config["name"] == name:
            with open('config.json', 'w') as f:
                config["name"] = name
                config["names"].append(name)
                json.dump(config, f, indent=4)
                embed = discord.Embed(title="He did it again!", description=f"New Name: {name}",
                                      color=discord.Color.red())
                await channel.send(content=f"@here", allowed_mentions=discord.AllowedMentions(everyone=True))
                await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(HunterCog(bot))
