import discord
from discord.ext import commands
import asyncio


class CodeEditor(commands.Cog):
    def __init__(self, client):
        self.client = client

    def indent(self, string):
        return ("•" * (len(string) - len(s := string.lstrip()))) + s

    @commands.command(aliases=("e", "edit"), hidden=True)
    @commands.is_owner()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def editor(self, ctx, *, content):
        code = []
        lang = content + "\n"
        nl = "\n"
        code_message = await ctx.send("loading...")

        async def update():
            await code_message.edit(
                content=f"```{lang}{(nl.join(('|'+str(n+1)+'| '+self.indent(x)) for n,x in enumerate(code))) if code else 'nothing'}```"
            )

        await update()
        await code_message.add_reaction("📝")
        await code_message.add_reaction("✅")
        while True:
            try:
                resp = await self.client.wait_for(
                    "message",
                    check=(lambda message: message.author.id == ctx.author.id),
                    timeout=200,
                )
                fetched_code_message = await ctx.fetch_message(code_message.id)
                for re in fetched_code_message.reactions:
                    if (str(re.emoji) == "✅") and (
                        ctx.author in (await re.users().flatten())
                    ):
                        await code_message.edit(content=f"```{lang}{nl.join(code)}```")
                        await code_message.clear_reactions()
                        break
                    elif (str(re.emoji) == "📝") and (
                        ctx.author in (await re.users().flatten())
                    ):
                        await resp.delete()
                        code.extend(
                            [
                                x[1:] if x.startswith("/") else x
                                for x in resp.content.splitlines()
                            ]
                        )
                        await update()
                        break

            except asyncio.TimeoutError:
                await code_message.clear_reactions()
                break


class _CodeEditor(commands.Cog):  # dont fucking touch this
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=("e", "edit"), hidden=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def editor(self, ctx, *, content):
        code = []
        lang = content + "\n"
        nl = "\n"
        code_message = await ctx.send("loading...")

        async def update():
            await code_message.edit(
                content=f"```{lang}{(nl.join(('|'+str(n+1)+'| '+x) for n,x in enumerate(code))) if code else 'nothing'}```"
            )

        await update()
        await code_message.add_reaction("📝")
        await code_message.add_reaction("✅")
        while True:
            try:
                reaction, user = await self.client.wait_for(
                    "reaction_add",
                    check=(
                        lambda reaction, user: reaction.message.id == code_message.id
                        and user == ctx.author
                    ),
                    timeout=100,
                )
                emoji = str(reaction)
                if emoji == "📝":
                    while True:
                        try:  # dont edit this
                            resp = await self.client.wait_for(
                                "message",
                                check=(
                                    lambda message: message.author.id == ctx.author.id
                                ),
                                timeout=20,
                            )
                            await resp.delete()
                            code.append(resp.content)
                            await update()

                        except asyncio.TimeoutError:
                            break
                elif emoji == "✅":
                    return await code_message.clear_reactions()
            except asyncio.TimeoutError:
                await code_message.clear_reactions()


def setup(client):
    client.add_cog(CodeEditor(client))
