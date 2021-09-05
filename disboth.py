import asyncio
import datetime
import json
import os
import random
import re
import traceback
from collections import namedtuple

import aiohttp
import discord
import requests
from discord.ext import tasks

import common
import emoji_server
import iroha
import iroha_MC
import muhou
import noname
import kei_server
import plugin_server

intents = discord.Intents.all()
client1 = discord.Client(intents=intents)
client2 = discord.Client(intents=intents)
os.chdir(os.path.dirname(os.path.abspath(__file__)))

discord_bot_token_1 = os.getenv("discord_bot_token_1")
discord_bot_token_2 = os.getenv("discord_bot_token_2")
where_from = os.getenv("where_from")
error_notice_webhook_url = os.getenv("error_notice_webhook")


def unexpected_error():
    """
    予期せぬエラーが起きたときの対処
    エラーメッセージ全文と発生時刻を通知"""

    now = datetime.datetime.now().strftime("%H:%M") #今何時？
    error_msg = f"```\n{traceback.format_exc()}```" #エラーメッセージ全文
    error_content = {
        "content": "<@523303776120209408>", #けいにメンション
        "avatar_url": "https://cdn.discordapp.com/attachments/644880761081561111/703088291066675261/warning.png",
        "embeds": [ #エラー内容・発生時間まとめ
            {
                "title": "エラーが発生しました",
                "description": error_msg,
                "color": 0xff0000,
                "footer": {
                    "text": now
                }
            }
        ]
    }
    requests.post(error_notice_webhook_url, json.dumps(error_content), headers={"Content-Type": "application/json"}) #エラーメッセをウェブフックに投稿


@client1.event
async def on_ready():
    try:
        login_notice_ch = client1.get_channel(595072269483638785)
        await login_notice_ch.send(f"{client1.user.name}がログインしました(from: {where_from})")
        print(f"{client1.user.name}がログインしました")
    except:
        unexpected_error()


@client2.event
async def on_ready():
    try:
        login_notice_ch = client2.get_channel(595072339545292804)
        await login_notice_ch.send(f"{client2.user.name}がログインしました(from: {where_from})")
        print(f"{client2.user.name}がログインしました")
    except:
        unexpected_error()


@client1.event
async def on_guild_join(guild):
    try:
        member_embed = discord.Embed(title="╋", description=f"{client1.user.name}が{guild.name}に参加しました", color=0xfffffe)
        member_embed.set_author(name=client1.user.name, icon_url=client1.user.avatar_url_as(format="png"))
        member_embed.set_footer(text=guild.name, icon_url=guild.icon_url_as(format="png"))
        join_leave_notice_ch = client1.get_channel(709307324170240079)
        await join_leave_notice_ch.send(embed=member_embed)

    except:
        unexpected_error()

@client1.event
async def on_guild_remove(guild):
    try:
        member_embed = discord.Embed(title="━", description=f"{client1.user.name}が{guild.name}から脱退しました", color=0xff0000)
        member_embed.set_author(name=client1.user.name, icon_url=client1.user.avatar_url_as(format="png"))
        member_embed.set_footer(text=guild.name, icon_url=guild.icon_url_as(format="png"))
        join_leave_notice_ch = client1.get_channel(709307324170240079)
        await join_leave_notice_ch.send(embed=member_embed)
    except:
        unexpected_error()


@client2.event
async def on_guild_join(guild):
    try:
        member_embed = discord.Embed(title="╋", description=f"{client2.user.name}が{guild.name}に参加しました", color=0xfffffe)
        member_embed.set_author(name=client2.user.name, icon_url=client2.user.avatar_url_as(format="png"))
        member_embed.set_footer(text=guild.name, icon_url=guild.icon_url_as(format="png"))
        join_leave_notice_ch = client2.get_channel(709307324170240079)
        await join_leave_notice_ch.send(embed=member_embed)
    except:
        unexpected_error()


@client2.event
async def on_guild_remove(guild):
    try:
        member_embed = discord.Embed(title="━", description=f"{client2.user.name}が{guild.name}から脱退しました", color=0xff0000)
        member_embed.set_author(name=client2.user.name, icon_url=client2.user.avatar_url_as(format="png"))
        member_embed.set_footer(text=guild.name, icon_url=guild.icon_url_as(format="png"))
        join_leave_notice_ch = client2.get_channel(709307324170240079)
        await join_leave_notice_ch.send(embed=member_embed)
    except:
        unexpected_error()


@client1.event
async def on_member_join(member):
    try:
        when_from = (member.created_at + datetime.timedelta(hours=9)).strftime(r"%Y/%m/%d　%H:%M")
        member_embed = discord.Embed(title="╋", description=f"{member.mention}が{member.guild.name}に参加しました\n{when_from}からのdiscordユーザー", color=0xfffffe)
        member_embed.set_author(name=member.name, icon_url=member.avatar_url)
        member_embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        join_leave_notice_ch = client1.get_channel(709307324170240079)
        await join_leave_notice_ch.send(embed=member_embed)
    except:
        unexpected_error()


@client1.event
async def on_member_remove(member):
    try:
        member_embed = discord.Embed(title="━", description=f"{member.mention}が{member.guild.name}から脱退しました", color=0xff0000)
        member_embed.set_author(name=member.name, icon_url=member.avatar_url)
        member_embed.set_footer(text=member.guild.name, icon_url=member.guild.icon_url)
        join_leave_notice_ch = client1.get_channel(709307324170240079)
        await join_leave_notice_ch.send(embed=member_embed)
    except:
        unexpected_error()


@client1.event
async def on_message(message):
    if message.content == "/bot_stop":
        kei_ex_guild = client1.get_guild(585998962050203672)
        bot_stop_right_role = discord.utils.get(kei_ex_guild.roles, id=707570554462273537)
        if not bot_stop_right_role in message.author.roles:
            await message.channel.send("何様のつもり？")
            return

        await client1.close()
        now = datetime.datetime.now().strftime(r"%Y年%m月%d日　%H:%M")
        stop_msg = f"{message.author.mention}により{client1.user.name}が停止させられました"
        main_content = {
            "username": "BOT STOP",
            "avatar_url": "https://cdn.discordapp.com/attachments/644880761081561111/703088291066675261/warning.png",
            "content": "<@523303776120209408>",
            "embeds": [
                {
                    "title": "botが停止させられました",
                    "description": stop_msg,
                    "color": 0xff0000,
                    "footer": {
                        "text": now
                    }
                }
            ]
        }
        requests.post(error_notice_webhook_url, json.dumps(main_content), headers={"Content-Type": "application/json"}) #エラーメッセをウェブフックに投稿

    try:
        try:
            if message.content.startswith("#") or message.content.startswith("//") or (message.content.startswith(r"/\*") and message.content.endswith(r"\*/")):
                return

            if message.author != client1.user:
                if message.channel == message.author.dm_channel:
                    await dm(client1, message)

            if message.guild is None:
                return

            if re.compile(r"https://(ptb.|canary.|)discord(app|).com/channels/").search(message.content):
                url_filter = re.split(r"https://(ptb.|canary.|)discord(app|).com/channels/", message.content)
                for url in url_filter:
                    if re.search(r"\d+/\d+/\d+", url):
                        await common.quote_message(client1, message, url) #メッセリンク展開用関数

            if message.content == "/help":
                await common.help(message)

            if message.content == "/new_func":
                await common.new_function(client1, message)

            if message.content == "/bug_report":
                await common.bug_report(client1, message)

            if message.content == "少し放置" or message.content == "学校終わって三条":
                await common.end_reaction(message)

            if client1.user in message.mentions:
                if not message.author.bot:
                    await common.mention(message, where_from)

            if message.author.id == 159985870458322944:
                await message.add_reaction("\U0001F595")

            form_list = [
                "/report",
                "/failure",
                "/idea",
                "/opinion",
                "/donation",
                "/inquiry",
                "/formal",
                "/informal",
                "/form"
            ]
            if message.content in form_list:
                await common.form_link(message)

            if "おはよう" in message.content or\
            "こんにちは" in message.content or\
            "こんばんは" in message.content or\
            "おやすみ" in message.content or\
            "ありがとう" in message.content:
                await common.greeting(message)

            if message.guild.id == 585998962050203672: #けい鯖
                await kei_server.on_message(client1, message)

            elif message.guild.id == 604945424922574848: #いろは鯖(MC)
                await iroha_MC.on_message(client1, message)

            elif message.guild.id == 587909823665012757: #無法地帯
                await muhou.on_message(client1, message)

            elif message.guild.id == 673838958303641620: #のねむ鯖
                await noname.on_message(client1, message)

            elif message.guild.id == 735632039050477649: #絵文字鯖
                await emoji_server.on_message(client1, message)

            elif message.guild.id == 876143248471621652: #いろは鯖
                await iroha.on_message(client1, message)

        except (RuntimeError, aiohttp.client_exceptions.ServerDisconnectedError):
            pass
        except discord.errors.Forbidden:
            await message.channel.send("権限がありません")
    except:
        unexpected_error()


@client2.event
async def on_message(message):
    if client2.user in message.mentions:
        if not message.author.bot:
            await common.mention(message, where_from)


@client1.event
async def on_raw_reaction_add(payload):
    try:
        if payload.guild_id == 585998962050203672: #けい鯖
            await kei_server.on_raw_reaction_add(client1, payload)

        if payload.guild_id == 576813939816398849: #プラグイン鯖
            await plugin_server.on_raw_reaction_add(client1, payload)

    except:
        unexpected_error()


@tasks.loop(seconds=60)
async def jms_notice():
    try:
        await client1.wait_until_ready()
        now = datetime.datetime.now()

        if now.hour == 9 and now.minute == 10:
            await kei_server.jms_notice(client1)

    except:
        unexpected_error()

jms_notice.start()


@tasks.loop(seconds=60)
async def shiritori_reset():
    try:
        await client1.wait_until_ready()
        now = datetime.datetime.now()

        if now.weekday() == 6 and now.hour == 3 and now.minute == 0:
            await kei_server.shiritori_reset(client1)

    except:
        unexpected_error()

shiritori_reset.start()


@tasks.loop(seconds=60)
async def change_guild_icon():
    try:
        await client1.wait_until_ready()
        now = datetime.datetime.now()

        if now.hour == 12 and now.minute == 0:
            await muhou.change_guild_icon(client1)

    except:
        unexpected_error()

change_guild_icon.start()


@tasks.loop(seconds=60)
async def marichan_birthday():
    try:
        await client1.wait_until_ready()
        now = datetime.datetime.now()

        if now.month == 6 and now.day == 28 and now.hour == 0 and now.minute == 0:
            await kei_server.marichan_birthday(client1)

        if now.month == 6 and now.day == 28 and now.hour == 23 and now.minute == 59:
            await kei_server.marichan_birthday_finish(client1)

    except:
        unexpected_error()

marichan_birthday.start()


@tasks.loop(seconds=60)
async def kei_get_war():
    try:
        await client1.wait_until_ready()
        now = datetime.datetime.now()

        if now.hour == 23 and now.minute == 55:
            await kei_server.kei_get_war(client1)

    except:
        unexpected_error()

kei_get_war.start()


@tasks.loop(seconds=30)
async def change_status():
    try:
        await client1.wait_until_ready()

        presense_list = [
            "members",
            "channels",
            "guilds",
            "https://discord.gg/nrvMKBT",
            "某MEE6より優秀"
        ]
        presense = random.choice(presense_list)
        if presense == "members":
            l = []
            for guild in client1.guilds:
                for mem in guild.members:
                    if not mem.id in l:
                        l.append(mem.id)
            presense = f"{len(l)}人を監視中"

        if presense == "channels":
            i = 0
            for guild in client1.guilds:
                for ch in guild.channels:
                    i += 1
            presense = f"{i}チャンネルを監視中"

        if presense == "guilds":
            presense = f"{len(client1.guilds)}サーバを監視中"

        game = discord.Game(presense)
        try:
            await client1.change_presence(status=discord.Status.online, activity=game)
        except ConnectionResetError:
            pass

    except:
        unexpected_error()

change_status.start()


@tasks.loop(seconds=60)
async def tenko():
    try:
        await client1.wait_until_ready()
        now = datetime.datetime.now()

        if now.weekday() in (5, 6):
            if now.hour == 7 and now.minute == 20:
                await kei_server.tenko(client1, "10", "朝")
            if now.hour == 7 and now.minute == 25:
                await kei_server.tenko(client1, "5", "朝")
        else:
            if now.hour == 6 and now.minute == 50:
                await kei_server.tenko(client1, "10", "朝")
            if now.hour == 6 and now.minute == 55:
                await kei_server.tenko(client1, "5", "朝")

        if now.hour == 19 and now.minute == 50:
            await kei_server.tenko(client1, "10", "帰校")

        if now.hour == 19 and now.minute == 55:
            await kei_server.tenko(client1, "5", "帰校")

    except:
        unexpected_error()
tenko.start()


async def dm(client1, message):
    if message.author.bot:
        return

    send_ch = client1.get_channel(639830406270681099)
    dm_embed = discord.Embed(description=message.content)
    dm_embed.set_author(name=f"{message.author.name}\n{message.author.id}", icon_url=message.author.avatar_url_as(format="png"))
    await send_ch.send(embed=dm_embed)


#以下ログインに必要
#触るな
Entry = namedtuple("Entry", "client event token")
entries = [
    Entry(client=client1, event=asyncio.Event(), token=discord_bot_token_1),
    Entry(client=client2, event=asyncio.Event(), token=discord_bot_token_2)
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
