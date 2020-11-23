import discord, aiohttp
from discord.ext import commands
from modules.parse import argparse
import random


class Puzzle(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.puzzles = []
        self.url = "https://raw.githubusercontent.com/vineetjohn/daily-coding-problem/master/README.md"

    async def update(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                if response.status == 200:
                    return await response.content.read()
                else:
                    raise Exception("unknown error")

    @commands.command(aliases=("puz", "p"))
    async def puzzle(self, ctx, arg="random"):
        """
        USAGE:
        ```py
        p|puzzle [number|word to search for]
        ```
        ######
        DESCRIPTION:
        Get some coding related puzzles.
        ######
        EXAMPLE:
        ```py
        cg.p 42
        ```
        """
        if self.puzzles == []:
            self.puzzles = (await self.update()).decode().split("---\n\n")

        if arg == "random":
            await ctx.send(
                (puz := random.choice(self.puzzles))[: puz.rfind("[")].strip().rstrip()
            )

        else:
            try:
                num = int(arg)
            except:
                if (
                    len(
                        puz := tuple(
                            x for x in self.puzzles if arg.lower() in x.lower()
                        )
                    )
                    > 0
                ):
                    await ctx.send(
                        (puz := random.choice(puz))[: puz.rfind("[")].strip().rstrip()
                    )
                    # i was lazy so i made this ^ in least possible changes
                else:
                    await ctx.send("no match found.")
            else:
                if num > len(self.puzzles):
                    await ctx.send("that's too high.")
                    return
                await ctx.send(
                    (puz := self.puzzles[num])[: puz.rfind("[")].strip().rstrip()
                )


def setup(client):
    client.add_cog(Puzzle(client))
