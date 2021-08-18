import random

import commands

async def on_message(client1, message):
    if message.author.name == "MEE6":
        await anti_mee6(message)

    if message.content.startswith("/vote"):
        await commands.vote(message)

    elif message.content.startswith("/info "):
        await commands.info(client1, message)

    elif message.content.startswith("/last_login "):
        await commands.last_login(message)

    elif message.content.startswith("/weather "):
        await commands.weather(message)

    elif message.content.startswith("/break "):
        await commands.seichi_break(message)

    elif message.content.startswith("/build "):
        await commands.seichi_build(message)

    elif message.content.startswith("/mcavatar "):
        await commands.mcavatar(client1, message)

    elif message.content.startswith("/random "):
        await commands.random_(message)

    elif message.content.startswith("/stack_eval "):
        await commands.stack_eval64(message)

    elif message.content.startswith("/stack_eval64 "):
        await commands.stack_eval64(message)

    elif message.content.startswith("/stack_eval16 "):
        await commands.stack_eval16(message)

    elif message.content.startswith("/stack_eval1 "):
        await commands.stack_eval1(message)


async def change_guild_icon(client1):
    guild = client1.get_guild(587909823665012757)
    pict_list = [
        "kero.png",
        "rem.png",
        "anan_1919.png",
        "poop.png",
        "who.jpg",
        "anzu_pic1.jpg",
        "anzu_pic2.jpg",
        "puha_RIM.jpg",
        "kawaii.png"
    ]
    pict = random.choice(pict_list)
    img = open(f"./pictures/{pict}", mode="rb").read()
    await guild.edit(icon=img)


async def anti_mee6(message):
    anti_message_list = [
        ":middle_finger:",
        "少し静かにしていただけますか？",
        "ちょっと黙っててもらっていいですか？",
        "お引き取りください",
        "f*ck",
        "たいそうにぎやかなご様子でいらっしゃいますところまことに恐縮でございますが、ご逝去あそばしていただければ幸甚に存じます"
    ]
    await message.channel.send(f"{message.author.mention}\n{random.choice(anti_message_list)}")
