import discord,random,re,datetime,json,time,math,os,asyncio,ast,requests,bs4
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用

import kyoutuu#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

async def iroha(message,client1):
    m = message.channel.send
    await kyoutuu.itibu_kyoutuu_greeting(message)

    await kyoutuu.itibu_kyoutuu_thank(message)

        if message.content.startswith(":skull:"):
            message_list = ["悲しい","ドンマイ","気をしっかり","えぇ"]
            send = random.choice(message_list)
            await m(send)
        if message.content.startswith(":medal:"):
            await m("おめ")

    if message.content.startswith("/vote "):
        poll_list = message.content.split(" ")
        del poll_list[0]#/pollを消す
        poll_header = poll_list[0]
        del poll_list[0]#投票の題名を消す
        if len(poll_list) > 9:
            await m("候補が多すぎます！9個以下にしてください。")
            return

        poll_description = ""
        for i in range(len(poll_list)):
            poll_description += str(i+1)+":"+poll_list[i]+"\n"

        poll_embed = discord.Embed(title=poll_header,description=poll_description)
    
        msg = await m(embed=poll_embed)

        reaction_list = [
            "\N{DIGIT ONE}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT TWO}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT THREE}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT FOUR}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT FIVE}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT SIX}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT SEVEN}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT EIGHT}\N{COMBINING ENCLOSING KEYCAP}",
            "\N{DIGIT NINE}\N{COMBINING ENCLOSING KEYCAP}"
        ]
        for i in range(len(poll_list)):
            await msg.add_reaction(reaction_list[i])


def change_mcid_to_uuid(mcid):
    url = f"https://api.mojang.com/users/profiles/minecraft/{mcid}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = str(bs4.BeautifulSoup(res.text, "html.parser"))
        uuid = soup.split(",")[0][7:][:-1]#JSON文字列から無理やりUUIDを取得
        return uuid

    except requests.exceptions.HTTPError:
        uuid = None
        return uuid


def change_uuid_to_mcid(uuid):
    try:
        url = f"https://sessionserver.mojang.com/session/minecraft/profile/{uuid}"
        res = requests.get(url)
        res.raise_for_status()
        soup = str(bs4.BeautifulSoup(res.text, "html.parser"))
        path = r"mcid.json"
        f = open(path,mode="w")
        f.write(soup)
        f.close()
        with open(path) as f:
            jf = json.load(f)
            mcid = jf["name"]
            mcid = mcid.replace("_",r"\_")
            return mcid

    except requests.exceptions.HTTPError:
        return None


async def total_login(client1,uuid):
    total_login_record_channel = client1.get_channel(682732532567113789)
    flag = False
    async for msg in total_login_record_channel.history():
        uuid_days = await total_login_record_channel.fetch_message(msg.id)
        if uuid_days.content.startswith(uuid):
            days = int(uuid_days.content.split(" ")[1])
            days = days + 1
            await total_login_record_channel.send(f"{uuid} {days}")
            await uuid_days.delete()
            flag = True
            break
    if not flag:
        await total_login_record_channel.send(f"{uuid} 1")


async def series_login(client1,login_uuid):
    series_login_record_channel = client1.get_channel(682732441479544918)
    today = datetime.date.today()
    flag = False
    async for msg in series_login_record_channel.history():
        today_uuid_days = await series_login_record_channel.fetch_message(msg.id)
        record_uuid = today_uuid_days.content.split(" ")[1]
        days = int(today_uuid_days.content.split(" ")[2])
        if record_uuid == login_uuid:
            days = days + 1
            await series_login_record_channel.send(f"{today} {login_uuid} {days}")
            await today_uuid_days.delete()
            flag = True
            break
    if not flag:
        await series_login_record_channel.send(f"{today} {login_uuid} 1")


async def login_rankings(client1,uuid):
    total_login_record_channel = client1.get_channel(682732532567113789)
    total_dic = {}
    async for total in total_login_record_channel.history():
        uuid_days = await total_login_record_channel.fetch_message(total.id)
        uuid = uuid_days.content.split(" ")[0]
        days = uuid_days.content.split(" ")[1]
        mcid = change_uuid_to_mcid(uuid)
        if mcid is None:
            mcid = "ERROR"
        total_dic[f"{mcid}"] = int(days)

    total_ranking = ""
    for i in range(len(total_dic)):
        total_max = max(total_dic,key=total_dic.get)
        total_ranking += f"{i}位：{total_max},{total_dic[total_max]}日\n"
        del total_dic[total_max]

    total_embed = discord.Embed(title="通算ログインランキング(仮)",description=total_ranking)
    await client1.get_channel(605030288640311306).send(embed=total_embed)