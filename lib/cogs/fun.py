import random

from discord.ext import commands


class FunCog(commands.Cog):
    def __init__(self, bot):
        self.bot: commands.Bot = bot
        print("Registered Fun Cog")

    @commands.command(name='8ball')
    async def _8ball(self, ctx, *, question):
        ball_predicts = ("It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.",
                         "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.",
                         "Signs point to yes.", "Reply hazy, try again.", "Ask again later.",
                         "Better not tell you now.", "Cannot predict now.", "Concentrate and ask again.",
                         "Don't count on it.", "My reply is no.", "My sources say no.", "Outlook not so good.",
                         "Very doubtful.")
        if question.endswith("?"):
            if question.strip() == "?":
                prediction = "That's not a question, that's a question sign..."
            elif "love" in question.lower():  # :tr:
                prediction = random.choice(ball_predicts[-5:])
            else:
                prediction = random.choice(ball_predicts)
        else:
            prediction = "That's not a question..."
        await ctx.send(f'Question: {question}\nThe ***:8ball:BALL*** says: {prediction}')

    @commands.command(name="flip", aliases=("coinflip", "flipcoin"))
    async def flip(self, ctx):
        await ctx.send(f"-Flip!-\nIt landed on {random.choice(('heads', 'tails'))}!")


def setup(bot):
    bot.add_cog(FunCog(bot))

