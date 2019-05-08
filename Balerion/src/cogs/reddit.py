import praw
from discord.ext import commands


class RedditCog(commands.Cog, name='Reddit Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="reddit")
    async def hot(self, ctx):
        reddit = praw.Reddit('Balerion')  # Initialize PRAW
        print("Read Only:", reddit.read_only)  # Output: False
        # continued from code above
        # assume you have a Reddit instance bound to variable `reddit`
        subreddit = reddit.subreddit('learnpython')

        print(subreddit.display_name)
        print(subreddit.title)
        print(subreddit.description)
        for submission in subreddit.hot(limit=10):
            print(submission.title)  # Output: the submission's title
            print(submission.score)  # Output: the submission's score
            print(submission.id)  # Output: the submission's ID
            print(submission.url)  # Output: the URL the submission points to
            # or the submission's URL if it's a self post


def setup(bot):
    bot.add_cog(RedditCog(bot))
