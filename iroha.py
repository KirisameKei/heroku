import commands

async def on_message(client1, message):
    """
    いろは鯖(MC)にメッセージが投稿されたときに呼び出される関数"""

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