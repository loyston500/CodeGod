import regex as re

codeblock_pattern = re.compile(r"""```((?!```)[\s\S])*```""")


def codeblock_extract(m):
    matches = []
    while (search := codeblock_pattern.search(m)) != None:
        match = search.group()
        matches.append(match)
        m = m.replace(match, "", 1)
    return matches


def codeblock(msg):
    if msg.count("```") % 2 == 0:
        # rex=re.findall(r"```[a-z]*\n[\s\S]*?```",msg)
        rex = codeblock_extract(msg)
        blocks = []
        inputs = []
        for x in rex:
            x = x[3:-3]
            if x.startswith("input\n"):
                inputs.append(x[6:].rstrip())
            elif not x.startswith("\n"):
                p = x.find("\n")
                blocks.append({"lang": x[:p], "code": x[p + 1 :].rstrip()})
            else:
                raise Exception(f"No language set for code block {len(blocks)+1}")
        return blocks, inputs
    else:
        raise Exception("Invalid codeblock syntax")


def argparse(mes):
    mes = re.findall(r'[^\s"]+|"[^"]*"', mes)
    i = 0
    length = len(mes)
    flags = set()
    params = {}
    inputs = []
    try:
        while i < length:
            if mes[i].startswith("--"):
                flags.add(mes[i][2:])
            elif mes[i].startswith("-"):
                params[mes[i][1:]] = mes[i + 1].replace('"', "")
                i += 1
            elif mes[i].startswith('"') and mes[i].endswith('"'):
                inputs.append(mes[i][1:-1])
            else:
                inputs.append(mes[i])
            i += 1
    except IndexError:
        raise Exception("Invalid Syntax")
    return params, inputs, flags
