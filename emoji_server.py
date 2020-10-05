import discord

async def emoji_update(client1, before, after):
    """
    絵文字のアップデートを監視する"""

    defferent = list(set(before) ^ set(after))
    notice_ch = client1.get_channel(762654494987124756)

    if defferent == []: #名前の変更なら
        embed = discord.Embed(
            title="絵文字名前変更",
            description="どの絵文字か分かりませんが名前が変更されました",
            color=0x00ffff
        )
        await notice_ch.send(embed=embed)
    else:
        if len(before) < len(after): #作成なら
            emoji = client1.get_emoji(defferent[0].id)
            emoji_name = emoji.name.replace("_", "\_")
            user = client.get_user(emoji.user.id)
            embed = discord.Embed(
                title="絵文字作成",
                description=f"{user}により:{emoji_name}:({emoji})が作成されました",
                color=0x00ff00
            )
            await notice_ch.send(embed=embed)

        elif len(before) > len(after): #削除なら
            emoji_name = defferent[0].name.replace("_", "\_")
            embed = discord.Embed(
                title="絵文字削除",
                description=f":{emoji_name}:が削除されました",
                color=0xff0000
            )
            await notice_ch.send(embed=embed)