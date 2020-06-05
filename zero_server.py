import asyncio

import discord

async def zero_server_new_func(client1, client4, message):
    """
    機能追加申請用関数"""

    start_msg = "```\n機能追加の申請をします。\n各項目は全て1回の送信で書いてください。\n\
各項目は10分でタイムアウトします。\n備考などがない場合はなしと入力してください。\n\
複雑な場合はけいまたはdisneyresidentsに直接言っていただいても構いません。```"
    msg_list = [
        "この依頼内容を公開してよろしいですか？\n良い場合はyes、悪い場合はnoと入力してください\n\
__**特殊な理由がない限りyesにしてください。**__(noの場合けいのDMに送られるためログが埋もれて忘れ去られる可能性があります。)",
        "何をしたら？\n例：/seichiと入力したら、16時になったら等",
        "何をする？\n例：整地鯖役職を付与する、チャンネルにあるメッセージをすべて消去する等",
        "チャンネル、役職の指定は？\n例：Hypixl役職持ちが実行すると怒られる、<#665937884662202434>を消す等",
        "その他備考は？\n他に要求がある場合ここに書いてください。",
    ]
    reply_list = []
    send_msg_list = []

    def check1(m):#公開設定
        return m.author == message.author and m.channel == message.channel and m.content == "yes" or m.content == "no"
    def check2(m):#何をしたら？
        return m.author == message.author and m.channel == message.channel
    def check3(m):#何をする？
        return m.author == message.author and m.channel == message.channel
    def check4(m):#チャンネルや役職の指定は？
        return m.author == message.author and m.channel == message.channel
    def check5(m):#備考は？
        return m.author == message.author and m.channel == message.channel
    def check6(m):#これでいいですか？
        return m.author == message.author and m.channel == message.channel and m.content == "yes" or m.content == "no"

    check_list = [
        check1,
        check2,
        check3,
        check4,
        check5,
    ]

    flag = False
    start = await message.channel.send(start_msg)
    msg = await message.channel.send(msg_list[0])
    send_msg_list.append(msg)
    for i in range(len(msg_list)):
        try:
            reply = await client4.wait_for("message",check=check_list[i],timeout=600)
            reply_list.append(reply)
        except asyncio.TimeoutError:
            await message.channel.send("タイムアウトしました。最初からやり直してください。")
            await start.delete()
            for j in range(i+1):
                await send_msg_list[j].delete()
                try:
                    await reply_list[j].delete()
                except IndexError:
                    pass
            break
        else:
            try:
                send_msg = await message.channel.send(msg_list[i+1])
                send_msg_list.append(send_msg)
            except IndexError:
                flag = True
            
    if flag:
        embed = discord.Embed(title="これで申請してよろしいですか？",description="良ければyes、やり直すならnoと入力してください",color=0xfffffe)
        embed.add_field(name="やりたいこと",value=f"{reply_list[1].content}{reply_list[2].content}",inline=False)
        embed.add_field(name="条件の指定",value=reply_list[3].content)
        embed.add_field(name="備考",value=reply_list[4].content)
        if reply_list[0].content == "yes":
            koukai_hikoukai = "公開"
        else:
            koukai_hikoukai = "非公開"
        embed.add_field(name="公開設定",value=koukai_hikoukai,inline=False)
        await start.delete()
        for j in range(5):
            await send_msg_list[j].delete()
            await reply_list[j].delete()
        kakunin = await message.channel.send(embed=embed)
        try:
            reply = await client4.wait_for("message",check=check6,timeout=600)
        except asyncio.TimeoutError:
            await message.channel.send("タイムアウトしました。最初からやり直してください。")
            await kakunin.delete()
        else:
            if reply.content == "yes":
                embed = discord.Embed(title="依頼が届きました",color=0x00ff00)
                embed.add_field(name="やりたいこと",value=f"{reply_list[1].content}{reply_list[2].content}",inline=False)
                embed.add_field(name="条件の指定",value=reply_list[3].content)
                embed.add_field(name="備考",value=reply_list[4].content)
                embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                embed.set_footer(text=message.guild.name,icon_url=message.guild.icon_url)
                if reply_list[0].content == "no":#非公開なら
                    dm = await client4.get_user(523303776120209408).create_dm()
                    await reply.delete()
                    await dm.send(embed=embed)
                    await message.channel.send("依頼内容をけいのDMに送信しました。回答をお待ちください。\n疑問点がある、情報が不十分等の理由でDMを送らせていただく場合があります。")
                else:
                    guild_name = message.guild.name
                    await reply.delete()
                    notice_ch = client1.get_channel(636359382359080961)
                    await notice_ch.send(content=f"<@523303776120209408>{message.guild.name}の零botについての依頼です", embed=embed)
                    await message.channel.send("依頼内容をけいの実験サーバ「python開発やることリスト」に送信しました。回答をお待ちください。\n\
疑問点がある、情報が不十分等の理由でメンションやDMをさせていただく場合があります。")

            else:
                await message.channel.send("最初からやり直してください。")
                await kakunin.delete()
                await reply.delete()
