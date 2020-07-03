import random

import discord

import commands

async def on_message(client1, message):
    if message.author.name == "MEE6":
        await anti_mee6(message)

    if message.content.startswith("/vote"):
        await commands.vote(message)

    if message.content.startswith("/info "):
        await commands.info(client1, message)

    if message.content.startswith("/last_login "):
        await commands.last_login(message)

    if message.content.startswith("/weather "):
        await commands.weather(message)

    if message.content.startswith("/break "):
        await commands.seichi_break(message)

    if message.content.startswith("/mcavatar "):
        await commands.mcavatar(client1, message)


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
        "kawaii"
    ]
    pict = random.choice(pict_list)
    img = open(pict, mode="rb").read()
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
