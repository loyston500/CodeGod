import discord, aiohttp
from discord.ext import commands
from urllib.parse import quote
import asyncio


class StackSearch(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.url = (
            "https://api.stackexchange.com/search/advanced?site=stackoverflow.com&q="
        )

    async def fetch(self, query):
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url + query) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    raise Exception

    @commands.command(aliases=("s", "stack", "stksearch"))
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def stk(self, ctx, *, query):
        """
        USAGE:
        ```py
        stk|stack|s <query>
        ```
        ######
        DESCRIPTION:
        Search for your problems on stackoverflow.
        ######
        EXAMPLE:
        ```py
        cg.s python strings
        ```
        """
        result = await self.fetch(quote(query))
        length = len(result["items"])
        page_no = 0
        mes = await ctx.send(result["items"][0]["link"])
        await mes.add_reaction("<:arrowleft:762542689425555486>")
        await mes.add_reaction("<:arrowright:762542086788349964>")

        async def display(page_no):
            await mes.edit(
                content=f'{result["items"][page_no]["link"]} {page_no+1}/{length}'
            )

        def check(reaction, user):
            return reaction.message.id == mes.id and user == ctx.author

        while True:
            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add", check=check, timeout=20
                )
                emoji = str(reaction.emoji)
                if emoji == "<:arrowright:762542086788349964>" and page_no < length - 1:
                    page_no += 1
                    await display(page_no)
                elif emoji == "<:arrowleft:762542689425555486>" and page_no > 0:
                    page_no -= 1
                    await display(page_no)
                await reaction.remove(user)
            except asyncio.TimeoutError:
                await mes.clear_reactions()

    @stk.error
    async def message_back(self, ctx, error):
        if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
            await ctx.send(str(error))


def setup(client):
    client.add_cog(StackSearch(client))
