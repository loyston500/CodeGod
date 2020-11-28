import discord
from discord.ext import commands

from modules.parse import argparse
from modules.compiler import RexTesterCompiler
from modules.database import trigger_emojis
import data

class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def help(self, ctx, arg=None):
        embed = discord.Embed(color=ctx.author.color)
        embed.set_author(name="HELP")
        if arg:
            for command in self.client.commands:
                if ((str(command) == arg) or (arg in command.aliases)) and (command.help != None):
                    for field in command.help.split("######"):
                        name, value = field.strip().split(":", 1)
                        embed.add_field(name=name.strip(), value=value.strip(), inline=False)
                    embed.set_footer(text=f"Requested by {ctx.author.name}")
                    break

        else:
            embed.add_field(
                name="USAGE", value="```py\nhelp <command>```", inline=False
            )
            embed.add_field(
                name="COMMAND LIST",
                value=", ".join(
                    f"`{command}`"
                    for command in self.client.commands
                    if not command.hidden
                ),
                inline=False,
            )
            embed.add_field(
                name="CODE EXECUTOR",
                value=f"To run a code simply write a message with at least one code block. Make sure you lable it with valid language. Then react your message with {await trigger_emojis.get(ctx.guild.id,'▶️')}. Boom! your code will be executed asap.\nFor additional help, run `cg.help <exec|eval|executor>`",
                inline=False,
            )
            embed.add_field(
                name="LANGUAGES",
                value="To get a list of all valid languages run\n```py\ncg.help <langs|languages|lang>```",
                inline=False,
            )
            embed.add_field(
                name="ABOUT",
                value="Run ```py\ncg.help <about|info>``` to get info about the bot."
            )
            embed.set_footer(text=f"Requested by {ctx.author.name}")

        return await ctx.send(embed=embed)


def setup(client):
    client.add_cog(Help(client))
