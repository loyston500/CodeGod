import discord, asyncio
from time import monotonic
from discord.ext import commands
from random import choice
from modules.database import trigger_emojis
import data

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def ping(self, ctx):
        """
        DESCRIPTION:
        Pings the bot.
        """
        before = monotonic()
        mes = await ctx.send("```diff\nbot_latency = ...\nlatency = ...```")
        after = monotonic()
        _latency = (after - before) * 1000
        _bot_latency = self.client.latency * 1000
        await mes.edit(
            content=f"```diff\n{'+' if _bot_latency<=300 else '-'} bot_latency = {round(_bot_latency,1)}ms\n{'+' if _latency<=300 else '-'} latency = {round(_latency,1)}ms```"
        )

    @commands.command(description="Gives the invite link")
    async def invite(self, ctx):
        """
        DESCRIPTION:
        Gives the invite link.
        """
        embed = discord.Embed(
            title="CLICK HERE TO INVITE",
            url="https://discord.com/api/oauth2/authorize?client_id=748051917061619724&permissions=391232&scope=bot",
        )
        embed.set_footer(text=f"Thanks for inviting CodeGod {choice('🧡💛💚💙🖤')}")
        await ctx.send(embed=embed)

    @commands.command(aliases=("server", "guild"))
    async def support(self, ctx):
        """
        DESCRIPTION:
        Gives the link of the support server.
        """
        await ctx.send("https://discord.gg/Z7QAsPzCk3")

    @commands.command(aliases=("info",), hidden=True)
    async def about(self, ctx):
        """
        ABOUT:
        A smart bot that compiles code.
        ######
        INVITE:
        [Click Here](https://discord.com/api/oauth2/authorize?client_id=748051917061619724&permissions=391232&scope=bot)
        ######
        SUPPORT SERVER:
        [Click Here](https://discord.gg/Z7QAsPzCk3)
        ######
        TOP.GG:
        [Click Here](https://top.gg/bot/748051917061619724)
        ######
        WEBSITE:
        [Click Here](https://loyston500.github.io/codegod) (in develoment)
        ######
        DONATE:
        You can donate us using [patreon](https://www.patreon.com/LoystonLive)
        ######
        DEV:
        LoystonLive#7925
        """

    @commands.command(pass_context=True, description="Set trigger emoji [ADMIN ONLY]")
    @commands.has_permissions(administrator=True)
    async def setemoji(self, ctx):
        """
        DESCRIPTION:
        Sets the trigger emoji. [ADMIN ONLY]
        """
        mes = await ctx.send("Please react this message with the emoji you want to use")

        def check(reaction, user):
            return user == ctx.message.author and (reaction.message.id == mes.id)

        try:
            reaction, user = await self.client.wait_for(
                "reaction_add", timeout=30.0, check=check
            )
        except asyncio.TimeoutError:
            await mes.edit(content="You did not react within 30s")
            await asyncio.sleep(6)
            await mes.delete()
        else:
            try:
                if trigger_emojis.exists(ctx.message.guild.id):
                    trigger_emojis.update(ctx.message.guild.id, str(reaction.emoji))
                else:
                    trigger_emojis.insert(ctx.message.guild.id, str(reaction.emoji))
            except Exception as err:
                await ctx.send(f"Fatal error. {err}")
            else:
                await mes.edit(content=f"Emoji set to {reaction.emoji} successfully")
            await reaction.remove(user)
                

    @setemoji.error
    async def command_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            await ctx.send("**You don't have permission to use this command**")
        else:
            raise error


def setup(client):
    client.add_cog(Misc(client))
