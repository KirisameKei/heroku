import discord

import commands

async def on_message(client1, message):
    """
    メッセージを受け取る関数"""

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

    if message.content.startswith("/random "):
        await commands.random_(message)