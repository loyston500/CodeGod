import discord, asyncio
from discord.ext import commands
from ordered_set import OrderedSet
from base64 import b64decode
from io import BytesIO
from functools import partial

from modules import compiler
from modules import parse
from modules.database import trigger_emojis
import data

rt = compiler.RexTesterCompiler()
hastebin = compiler.HasteBinApi()
tio = compiler.TioRunCompiler()

class CodeExecutorOnReact(commands.Cog):
    def __init__(self, client):
        self.client = client

    def process_base64_image(self, image):
        # file_bytes = BytesIO()
        # file_bytes.write(b64decode(image))
        file_bytes = BytesIO(b64decode(image))
        file_bytes.seek(0)
        return file_bytes

    @commands.command(name="exec", aliases=("executor","eval"))
    async def _exec(self, ctx):
        """
        USAGE:
        ```py
        * [-c] [-l] [--clean] [--forcebin]
        ```
        ######
        DESCRIPTION:
        `-c` -> sets the compiler API. Valid value is `tio`
        `-l` -> sets the language (for tio check out the supported ones) . This is only needed if are using `-c` parameter.
        `--clean` -> excludes the embed from the output. Better if you are going to copy the output.
        `--forcebin` -> sends the output to the bin even if it's less than 2000 chars.
        ######
        TAKING INPUTS:
        If you want to pass the inputs you can do that by writing your input inside another code block with the lable set to `input`.
        This code block should be in the same message along with the main code block.
        The position of these code blocks doesn't matter.
        ######
        NOTE:
        Rextester is the default compiler so `-c` and `-l` are not needed.
        Separate inputs by newline, no need to put each input in a separate code block.
        Don't worry if you have multiple code bocks in the same message, the bot will ask you which one to execute.
        You can also write the text outside the code blocks as usual, the bot will not consider those for anything at all.
        ######
        EXAMPLE 1:
        --clean ```py
        print('Hello World!')
        ```
        ######
        EXAMPLE 2:
        -c tio -l python3 ```py
        print('Hello World!')
        ```
        """

    @commands.command(aliases=("languages", "language", "langs"))
    async def lang(self, ctx):
        """
        language list (rextester):
        `ada`
        `go`
        `pas`, `pascal`
        `lua`
        `vbnet`
        `erl`
        `tcl`
        `scheme`
        `elixir`
        `py2`
        `sql`
        `assembly`, `nasm`
        `cs`
        `m`
        `perl`, `pl`
        `clj`, `clojure`
        `f90`, `fortran`
        `vcpp`
        `bash`, `sh`
        `prolog`
        `rb`, `ruby`
        `rs`, `rust`
        `scala`
        `swift`
        `kotlin`, `kt`
        `cpp`
        `bf`, `brainfk`, `brainfuck`
        `clangpp`
        `objectivec`
        `java`
        `r`
        `d`
        `php`
        `haskell`, `hs`
        `ml`
        `py`, `python`
        `lisp`
        `fs`
        `clang`
        `vc`
        `javascript`, `js`, `node`, `nodejs`
        `c`
        ######
        language list (tio):
        [click here](https://pastebin.pl/view/9133a479)
        """

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reactor = self.client.get_user(payload.user_id)
        if reactor.bot:
            return
        if str(payload.emoji) == (
            emoji := trigger_emojis.get(payload.guild_id, "▶️")
        ):
            channel = self.client.get_channel(payload.channel_id)
            #if not channel.guild.me.guild_permissions.text.manage_messages:
                #return await channel.send("**permission to manage messages is not given**")
            # Checks for cooldowns
            if payload.user_id in data.cooldown:
                warn = await channel.send(
                    f"{reactor.mention}, you ran the code just now please wait for few seconds :)"
                )
                await asyncio.sleep(6)
                await warn.delete()
                return
            message = await channel.fetch_message(payload.message_id)
            try:
                blocks, inputs = parse.codeblock(message.content)
                if blocks == []:  # basically exits if there is no code blocks
                    return
                else:
                    try:  # a simple spell, but this will make it work even if the manage message perms is not given.
                        await message.clear_reaction(emoji)
                    except:
                        pass
                    arg_params, arg_inputs, arg_flags = parse.argparse(
                        message.content[: message.content.find("```")]
                    )
            except Exception as err:
                await channel.send(f"Cannot parse the message. Reason:\n{err}")
            else:
                await message.add_reaction("<a:RunningCode:749252623449718834>")
                if (blocks_len := len(blocks)) > 1:
                    # ask representes the message which asks the user to selects the codeblock to execute
                    ask_number = await channel.send(
                        f"Seems like the message has more than one code blocks. Enter number from **1** to **{blocks_len}** to run a certain code block."
                    )

                    def check(reply):
                        if reply.content.isdigit():
                            return (
                                reactor == reply.author
                                and int(reply.content) <= blocks_len
                            )
                        else:
                            return False

                    try:
                        ask_number_reply = await self.client.wait_for(
                            "message", check=check, timeout=20
                        )
                    except asyncio.TimeoutError:
                        await ask_number.delete()
                        b = 0
                    else:
                        b = int(ask_number_reply.content) - 1
                        await ask_number.delete()
                        try:  # here too
                            await ask_number_reply.delete()
                        except:
                            pass
                else:
                    b = 0
                try:
                    data.cooldown.add(payload.user_id)
                    if "c" not in arg_params:
                        rt_response, error_exist, stats = await rt.run(
                            blocks[b]["code"], blocks[b]["lang"], "\n".join(inputs)
                        )
                    elif arg_params["c"] == "tio":
                        if "l" in arg_params:
                            rt_response, error_exist, stats = await tio.run(
                                blocks[b]["code"], arg_params["l"], "\n".join(inputs)
                            )
                        else:
                            raise Exception("A language needs to be set.")
                    else:
                        raise Exception("Invalid compiler name.")

                except Exception as err:
                    data.cooldown.remove(payload.user_id)
                    mes = await channel.send(err)
                    try:  # here too
                        await message.clear_reaction(
                            "<a:RunningCode:749252623449718834>"
                        )
                    except:
                        pass
                    await asyncio.sleep(6)
                    await mes.delete()
                else:
                    output = rt_response["Result"] + ("\n") + rt_response["Errors"]
                    react_with, color = (
                        "<:tickmark:764878083106144358>",
                        0x00BA9C,
                    )  # 0x24FF65

                    if error_exist:
                        react_with, color = "<:warningq:764877977778389023>", 0xFFCF24
                    if output == "\n":
                        output, react_with = "NO OUTPUT", "❓"

                    if len(output) <= 1950 and ("forcebin" not in arg_flags):
                        content = f"```{arg_params.get('h','css')}\n{output.replace('```','`` ')}```"
                    else:
                        try:
                            key = await hastebin.get_key(output[:10000])
                        except:
                            content = f"```{arg_params.get('h','css')}\n{output[:1950].replace('```','`` ')}```"
                            stats = (
                                stats
                                + ".\nHastebin didn't respond so the output was trimmed and sent here itself."
                            )
                        else:
                            content = f"The output is too long.{' Check it out in http://hastebin.com/'+key.get('key', 'error') if 'key' in key else ''}"

                    # Sends Images if the response contains it
                    files = None
                    if blocks[b]["lang"] in {"m", "r"}:
                        if rt_response["Files"] != []:
                            rt_response["Files"] = OrderedSet(rt_response["Files"])
                            files = []
                            for n, base64_image in enumerate(rt_response["Files"][:10]):
                                function_process = partial(
                                    self.process_base64_image, base64_image
                                )
                                file_bytes = await self.client.loop.run_in_executor(
                                    None, function_process
                                )
                                files.append(
                                    discord.File(
                                        filename=f"image{n+1}.png", fp=file_bytes
                                    )
                                )
                    if "clean" in arg_flags:
                        mes = await channel.send(content=f"{reactor.mention}" + content, files=files)
                    else:
                        embed = discord.Embed(
                            title="Jump to message",
                            url=message.jump_url,
                            color=color,
                            description=content,
                        )
                        embed.set_footer(text=stats + f" @{reactor.name}")
                        mes = await channel.send(embed=embed, files=files)
                    try:
                        await message.clear_reaction(
                            "<a:RunningCode:749252623449718834>"
                        )
                    except:
                        pass
                    await mes.add_reaction(react_with)
                    await asyncio.sleep(3.5)
                    await mes.add_reaction("🗑️")
                    data.cooldown.remove(payload.user_id)

                    def check(reaction, user):
                        return (
                            reactor == user
                            and reaction.message.id == mes.id
                            and str(reaction.emoji) == "🗑️"
                        )

                    try:
                        await self.client.wait_for(
                            "reaction_add", timeout=30.0, check=check
                        )
                    except asyncio.TimeoutError:
                        await mes.clear_reaction("🗑️")
                    else:
                        await mes.delete()


def setup(client):
    client.add_cog(CodeExecutorOnReact(client))
