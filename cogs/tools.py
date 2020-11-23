import discord, aiohttp
from discord.ext import commands
from modules.parse import argparse


class Tools(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=("embed", "embeds"))
    async def emb(self, ctx, *, content):
        """
        USAGE:
        ```py
        embed|emb [t|title] [c|color] [u|url] [a|author] [f|footer] [name1] [value1] [name2] [value2] ... {--inline}
        ```
        ######
        DESCRIPTION:
        Creates an embed.
        ######
        EXAMPLE:
        ```py
        cg.emb -t "Hello" -c 0xF742DD -f "the footer" -d "[click here](https://google.com/)" -a "the author" -u "https://google.com/" "name1" "value1" "name2" "value2" --inline
        ```
        """
        params, inputs, flags = argparse(content)
        embed = discord.Embed(
            title=params.get("title") or params.get("t"),
            description=params.get("description") or params.get("d"),
            color=(
                0x000000
                if (color := (params.get("color") or params.get("c"))) == None
                else int(color, int(params.get("b") or 16))
            ),
            url=params.get("url") or params.get("u"),
        )
        embed.set_author(name=params.get("author") or params.get("a"))
        embed.set_footer(text=params.get("footer") or params.get("f"))
        inline = "inline" in flags

        for name, value in zip(inputs[::2], inputs[1::2]):
            embed.add_field(name=name, value=value, inline=inline)
        await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Tools(client))
