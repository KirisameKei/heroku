import discord

async def on_message(client1, message):
    """
    HJKにメッセージが投稿された時用の関数"""

    if message.content.startswith("/vote"):
        await commands.vote(message)

    if message.content.startswith("/info "):
        await commands.info(client1, message)

    if message.content.startswith("/last_login "):
        await commands.last_login(message)

    if message.content.startswith("/break "):
        await commands.seichi_break(message)

    if message.content.startswith("/mcavatar "):
        await commands.mcavatar(client1, message)