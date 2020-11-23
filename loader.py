import discord
from discord.ext import commands

from glob import glob


def load_extensions(client):
    loaded = []
    files = glob("cogs/*.py")
    if files == []:
        raise ImportError("No cogs to load")
    for file in files:
        if not file.endswith("__init__.py"):
            try:
                file_clean = file.replace("/", ".").replace("\\", ".")[:-3]
                client.load_extension(file_clean)
                loaded.append(file_clean)
            except discord.ext.commands.errors.ExtensionAlreadyLoaded:
                pass
    return loaded
