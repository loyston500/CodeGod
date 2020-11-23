import discord
from discord.ext import commands
from glob import glob
from dotenv import load_dotenv

from modules.parse import argparse
from modules.fun_art import CodeGod_Rainbow_Mono9
from loader import load_extensions

import os


class Owner(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True, aliases=("owner", "get"))
    @commands.is_owner()
    async def su(self, ctx, *, content):
        params, inputs, flags = argparse(content)
        try:

            if "s" in params:
                await ctx.send(f"sh: ```css\n{os.popen(params['s']).read()}```")

            if "i" in params:
                if params["i"] == "--all":
                    loaded = load_extensions(self.client)
                    await ctx.send(
                        "install: ```diff\nSuccessfully installed"
                        + ("\n+ ".join(loaded))
                        + "```"
                    )
                else:
                    self.client.load_extension(params["i"])
                    await ctx.send(
                        f"install: ```css\nsuccessfully installed '{params['i']}'```"
                    )

            if "update" in flags:  # this one is flag xD
                output = os.popen(
                    "git pull"
                ).read()
                await ctx.send(f"```css\n{output}```")

            if "r" in params:
                cog_name = params["r"]
                if not cog_name.startswith("cogs."):
                    cog_name = "cogs." + cog_name
                self.client.reload_extension(cog_name)
                await ctx.send(f"reload: ```css\nsuccessfully reloaded '{cog_name}'```")

            if "ex" in params:
                exec(params["ex"])
                await ctx.send("ex: ```css\nexecution success```")

            if "ev" in params:
                result = eval(params["ev"])
                await ctx.send(f"ex: ```css\n{result}```")

        except Exception as error:
            await ctx.send(f"error: ```css\n{error}```")


def setup(client):
    client.add_cog(Owner(client))
    print(CodeGod_Rainbow_Mono9)
