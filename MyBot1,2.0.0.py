import discord,random,re,datetime,json,time,math,os,asyncio,requests,bs4,ast,sys,traceback
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
#from discord import FFmpegPCMAudio
from discord import Embed#ここまでモジュールのインポート
from discord import Webhook, RequestsWebhookAdapter

try:
    import tokens
except ModuleNotFoundError:
    pass

import kyoutuu,kei_ex_server,iroha#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)

client1 = discord.Client()#魔理沙bot(メインで使用)

try:
    import tokens_ConoHa
except ModuleNotFoundError: #けいローカル or heroku
    try:
        path = r"C:\Users\hayab\tokens_Local.txt"
        with open(path, mode="r") as f:
            program_data_list = f.readlines()
            discord_bot_token_1 = program_data_list[0]
            discord_bot_token_4 = program_data_list[3]
            error_notice_webhook_url = program_data_list[4]
            where_from = program_data_list[4]
    except FileNotFoundError: #heroku
        discord_bot_token_1 = os.getenv("discord_bot_token_1")
        discord_bot_token_4 = os.getenv("zero_bot_token")
        error_notice_webhook_url = os.getenv("error_notice_webhook_url")
        where_from = os.getenv("where_from")
else: #ConoHa
    discord_bot_token_1 = tokens_ConoHa.discord_bot_token_1
    discord_bot_token_4 = tokens_ConoHa.discord_bot_token_4
    where_from = tokens_ConoHa.where_from


async def unexpected_error():
    """
    予期せぬエラーが起きたときの対処
    エラーメッセージ全文と発生時刻を通知"""

    now = datetime.datetime.now().strftime("%H:%M") #今何時？
    error_msg = f"```\n{traceback.format_exc()}```" #エラーメッセージ全文
    error_embed = discord.Embed(title="ERROR", description=error_msg, color=0xff0000)
    error_embed.set_footer(text=now)
    python_todo_list = client1.get_channel(636359382359080961)
    await python_todo_list.send(content="<@523303776120209408>", embed=error_embed)


@client1.event
async def on_ready():
    try:
        login_notice_ch = client1.get_channel(595072269483638785)
        await login_notice_ch.send(f"{client1.user.name}がログインしました(from:{where_from})")
        print(f"{client1.user.name}がログインしました")
    except:
        await unexpected_error()


@client1.event
async def on_message(message):
    if message.content == "/bot_stop":
        kei_ex_guild = client1.get_guild(585998962050203672)
        bot_stop_right_role = discord.utils.get(kei_ex_guild.roles, id=707570554462273537)
        if not bot_stop_right_role in message.author.roles:
            await message.channel.send("何様のつもり？")
            return

        now = datetime.datetime.now().strftime(r"%Y/%m/%d　%H:%M")
        stop_msg = f"{message.author.mention}により{client1.user.name}が停止させられました"
        stop_embed = discord.Embed(title="botが停止させられました", description=stop_msg, color=0xff0000)
        stop_embed.set_footer(text=now)
        python_todo_list = client1.get_channel(636359382359080961)
        await python_todo_list.send(content="<@523303776120209408>", embed=stop_embed)

        await client1.close()
    try:
        try:
            m = message.channel.send

            if message.author != client1.user:#DM対処
                if message.channel == message.author.dm_channel:
                    channel = client1.get_channel(639830406270681099)
                    dm_embed = discord.Embed(description=message.content)
                    dm_embed.set_author(name=message.author.name+"\n"+str(message.author.id),icon_url=message.author.avatar_url)
                    await channel.send(embed=dm_embed)
                    return

                if message.channel.id == 639830406270681099:
                    str_user_id = message.content[0:18]
                    content = message.content[18:]
                    p = re.compile(r"^[0-9]+$")
                    if p.fullmatch(str_user_id):
                        user_id = int(message.content[0:18])
                        try:
                            member = client1.get_user(user_id)
                            dm = await member.create_dm()
                            await dm.send(content)
                        except AttributeError:
                            await m("そのユーザーは見つかりませんでした。")

            #try:
                if message.content.startswith("="):
                    siki = message.content.replace("=", "")
                    kotae = eval(siki)
                    await message.channel.send(f"{kotae}")

                if message.guild.id == 585998962050203672:#けいの実験サーバ
                    await kei_ex_server.kei_ex_server(message,client1)#本体

                if message.guild.id == 604945424922574848:#いろは鯖
                    await iroha.iroha(message,client1)

            #except AttributeError:
            #    await message.channel.send("エラー")
        except RuntimeError:
            pass
    except:
        await unexpected_error()


#以下ログインと接続に必要、触るな
Entry = namedtuple("Entry", "client event token")
entries = [
    Entry(client=client1,event=asyncio.Event(),token=discord_bot_token_1)
]  

async def login():
    for e in entries:
        await e.client.login(e.token)

async def wrapped_connect(entry):
    try:
        await entry.client.connect()
    except Exception as e:
        await entry.client.close()
        print("We got an exception: ", e.__class__.__name__, e)
        entry.event.set()

async def check_close():
    futures = [e.event.wait() for e in entries]
    await asyncio.wait(futures)

loop = asyncio.get_event_loop()
loop.run_until_complete(login())
for entry in entries:
    loop.create_task(wrapped_connect(entry))
loop.run_until_complete(check_close())
loop.close()
