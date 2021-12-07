import discord
from discord.ext import commands
from discord.ext.commands import Context


class UtilitiesCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        self.yes = u"\u2705"  # White checkmark on green bg
        self.no = u"\u274C"  # Red cross
        self.error_embed = discord.Embed(title=f"{self.no} Syntax Error", description="", color=discord.Color.red())
        print("Registered Utilities Cog")

    @commands.command(name='vote')
    async def vote_reactions(self, ctx: Context, count: int=None, message_id: int=None):
        if count is None and message_id is None:
            await ctx.message.delete()
            self.error_embed.description = f"{ctx.author.mention}\n**Syntax**: !vote <Number of Reactions> <Message ID>"
            await ctx.send(embed=self.error_embed, delete_after=5)
            return

        if count is None or count == 0 or count > 10 or count < 0:
            await ctx.message.delete()
            self.error_embed.description = f"{ctx.author.mention}\nPlease specify the amount of reactions to add! (Max. 10)"
            await ctx.send(embed=self.error_embed, delete_after=5)
            return

        if message_id is None or message_id == 0:
            await ctx.message.delete()
            self.error_embed.description = f"{ctx.author.mention}\nPlease specify a valid MessageID from a message in this channel."
            await ctx.send(embed=self.error_embed, delete_after=5)
            return

        try:
            message: discord.Message = await ctx.channel.fetch_message(message_id)
        except Exception as ignore:
            await ctx.send(f"{ctx.author.mention} Couldn't get message", delete_after=5)
            error = discord.Embed(title=f"{self.no} Something went wrong", description="Couldn't get message. Please check if the MessageID is valid.", color=discord.Color.red())
            await ctx.send(embed=error, delete_after=5)
            return

        if message.author != ctx.author:
            await ctx.message.delete()
            error = discord.Embed(title=f"{self.no} Permission Error",
                                  description="You may only add reactions to your own messages!",
                                  color=discord.Color.red())
            await ctx.send(embed=error, delete_after=5)
            return

        if count >= 1:
            await message.add_reaction("1️⃣")
            pass
        if count >= 2:
            await message.add_reaction("2️⃣")
            pass
        if count >= 3:
            await message.add_reaction("3️⃣")
            pass
        if count >= 4:
            await message.add_reaction("4️⃣")
            pass
        if count >= 5:
            await message.add_reaction("5️⃣")
            pass
        if count >= 6:
            await message.add_reaction("6️⃣")
            pass
        if count >= 7:
            await message.add_reaction("7️⃣")
            pass
        if count >= 8:
            await message.add_reaction("8️⃣")
            pass
        if count >= 9:
            await message.add_reaction("9️⃣")
            pass
        if count == 10:
            await message.add_reaction("🔟")

        await ctx.message.delete()
        embed = discord.Embed(description=f"{self.yes} **Added reactions successfully.**",
                              color=discord.Color.green())
        await ctx.send(embed=embed, delete_after=5)


def setup(bot):
    bot.add_cog(UtilitiesCog(bot))
