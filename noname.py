import random

import discord

async def on_message(client1, message):
    """
    メッセージを受け取る関数"""

    if not message.channel.id == 731808696358666291:
        return

    if message.content == "/join":
        kikaku_role = discord.utils.get(message.guild.roles, id=731882691049554062)
        await message.author.add_roles(kikaku_role)
        await message.channel.send(f"{message.author.display_name}さんが参加しました")

    if message.content == "/test":
        await noname_kikaku(client1)


async def noname_kikaku(client1):
    """
    企画"""

    guild = client1.get_guild(673838958303641620)
    kikaku_role = discord.utils.get(guild.roles, id=731882691049554062)
    kikaku_ch = client1.get_channel(731808696358666291)
    try:
        tousen_list = random.sample(kikaku_role.members, 2)
    except ValueError:
        await kikaku_ch.send("人数不足により抽選不成立")
        return

    description = f"椎名: {tousen_list[0].mention}\n頭　: {tousen_list[1].mention}"
    embed = discord.Embed(title=":tada:当選者:tada:", description=description, color=0xffff00)
    await kikaku_ch.send(embed=embed)
