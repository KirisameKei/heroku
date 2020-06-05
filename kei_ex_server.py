import discord

import kyoutuu#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)

async def kei_ex_server(message,client1):
    m = message.channel.send
    await kyoutuu.itibu_kyoutuu_daily_ranking(message)

    if message.content == "/marichan_invite":
        dm = await message.author.create_dm()
        marichan_inviter_role = discord.utils.get(message.guild.roles,id=663542711290429446)
        await message.author.add_roles(marichan_inviter_role)
        await message.delete()
        await m("コマンド漏洩防止のためメッセージを削除しました。")
        await dm.send("https://discordapp.com/api/oauth2/authorize?client_id=594052349140402179&permissions=338783443&scope=bot")
        await m(f"{message.author.mention}\nDMに招待リンクを送信しました。(管理者権限を持っているサーバに導入できます)")