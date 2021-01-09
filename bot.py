import discord, asyncio
from discord.ext import commands
from random import choice

from modules.database import trigger_emojis
import data
from loader import load_extensions

# GETS THE TOKENS
from dotenv import load_dotenv
import os

load_dotenv()

if input("Start as (DEBUG, RELEASE)? ").lower() == "release":
    TOKEN = os.getenv("DISCORD_TOKEN")
    print("Successfully set to release.")
else:
    TOKEN = os.getenv("DISCORD_TOKEN_DEBUG")
    print("Successfully set to debug.")

intents = discord.Intents(messages=True, guilds=True, members=True, reactions=True)

client = commands.Bot(command_prefix="cg.", case_insensitive=True, intents=intents)
client.remove_command("help")

loaded = load_extensions(client)
if "cogs.owner" not in loaded:
    raise ImportError("Owner cog not loaded")
for file in loaded:
    print(f"Loaded {file}")


async def status_task():
    langs = (
        "python",
        "ruby",
        "C++",
        "C",
        "C#",
        "javascript",
        "java",
        "GO",
        "R",
        "perl",
        "PHP",
        "assembly",
        "objective-c",
        "haskell",
        "lua",
        "pascal",
        "prolog",
        "lisp",
        "scala",
        "scheme",
        "TCL",
        "D",
        "R",
        "ada",
        "bash",
        "elixir",
        "kotlin",
        "brainf***",
        "fortran",
        "rust",
        "clojure",
        "swift",
    )
    while True:
        await client.change_presence(
            activity=discord.Game(name="with " + choice(langs) + " codes!", type=0)
        )
        await asyncio.sleep(100)
        await client.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="for a ping!"
            )
        )
        await asyncio.sleep(30)


@client.event
async def on_ready():
    print(f"{client.user.name} has connected to Discord!")
    client.loop.create_task(status_task())


@client.event
async def on_message(message):
    if not message.author.bot:
        if client.user in message.mentions:
            await message.channel.send(
                f"Trigger emoji in this guild is set to {await trigger_emojis.get(message.guild.id,'▶️')}\nBot Prefix: `cg.`"
            )
        else:
            await client.process_commands(message)


client.run(TOKEN)
