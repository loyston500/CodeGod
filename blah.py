def hk_compiler(channel, message):
    # Garbage below test edit
    hk_response = await hk.run(blocks[b]["code"], blocks[b]["lang"])
    if len(hk_response["run_status"].get("output", "No Output")) <= 1950:
        if hk_response["compile_status"] == "OK":
            if hk_response["run_status"]["exit_code"] == "9":
                lang = "css"
                if hk_response["run_status"]["output"] == "":
                    output = "No Output"
                else:
                    output = hk_response["run_status"]["output"]
                react_with = "➰"
            elif hk_response["run_status"]["exit_code"] == "0":
                lang = "yaml"
                if hk_response["run_status"]["output"] == "":
                    output = "No Output"
                else:
                    output = hk_response["run_status"]["output"]
                react_with = "✅"
            else:
                lang = "http"
                output = hk_response["run_status"]["stderr"].replace(" ", "⠀")
                react_with = "⚠️"
        else:
            lang = "diff"
            output = "- " + (
                hk_response["compile_status"]
                .replace("\n", "\n- ")
                .replace("```", "`` ")
            )
            react_with = "❌"
        # mes represents the output message
        mes = await channel.send(
            f"```{lang}\n{output}```Msg ID: **{payload.message_id}**"
        )
        await mes.add_reaction(react_with)
        await mes.add_reaction("🗑️")

        def check(reaction, user):
            return (
                user == message.author
                and reaction.message.id == mes.id
                and str(reaction.emoji) == "🗑️"
            )

        try:
            reaction, user = await client.wait_for(
                "reaction_add", timeout=30.0, check=check
            )
        except asyncio.TimeoutError:
            await mes.clear_reaction("🗑️")
        else:
            await mes.delete()
    else:
        try:
            if hk_response["compile_status"] == "OK":
                if hk_response["run_status"]["exit_code"] == "0":
                    key = await hastebin.get_key(hk_response["run_status"]["output"])
                else:
                    key = await hastebin.get_key(hk_response["run_status"]["stderr"])
            else:
                key = await hastebin.get_key(hk_response["compile_status"])
            await channel.send(
                f"The output is too long. Check it out in http://hastebin.com/{key['key']}"
            )
        except Exception as err:
            await channel.send(err)
