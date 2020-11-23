import discord
from discord.ext import commands

from modules import compiler
from modules.parse import argparse

rt = compiler.TioRunCompiler()


class RegexExecutor(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=("re", "reg"))
    @commands.cooldown(1, 3.5, commands.BucketType.user)
    async def regex(self, ctx, *, content):
        """
        USAGE:
        ```py
        regex|re <input1> <input1> <input3 only if sub> <--match|split|find|flit|sub> [--source] [--dm]
        ```
        ######
        DESCRIPTION:
        Helps to test regex easily.
        ######
        EXAMPLE:
        ```py
        cg.re "69" "694206912369" --flit --source
        ```
        """
        params, inputs, flags = argparse(content)
        if True:
            if "split" in flags:
                code = f"import re\nprint(re.split(r'{inputs[0]}','{inputs[1]}'))"
                lang = "python3"
            elif ("findall" in flags) or ("find" in flags):
                code = f"import re\nprint(re.findall(r'{inputs[0]}','{inputs[1]}'))"
                lang = "python3"
            elif "sub" in flags:
                code = f"import re\nprint(re.sub(r'{inputs[0]}','{inputs[1]}','{inputs[2]}'))"
                lang = "python3"
            elif "flit" in flags:
                code = f"import re\nprint('Split: ',re.split(r'{inputs[0]}','{inputs[1]}'))\nprint('Find: ',re.findall(r'{inputs[0]}','{inputs[1]}'))"
                lang = "python3"
            elif "match" in flags:
                code = (
                    'if("'
                    + inputs[1]
                    + '"=~/'
                    + inputs[0]
                    + '/){\nprint "+ Match Found\\n";\n}\nelse{\nprint "- Match not Found\\n";\n}'
                )
                lang = "perl"
        if "source" in flags:
            await ctx.send(f"```{lang}\n{code}```")
        else:
            response = (await rt.run(code, lang, ""))[0]
            await ctx.send(
                "```diff\n" + response["Result"] + ("\n") + response["Errors"] + "```"
            )


def setup(client):
    client.add_cog(RegexExecutor(client))
