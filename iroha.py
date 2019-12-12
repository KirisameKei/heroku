import discord,random,re,datetime,json,time,math,os,asyncio
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用

import server_log,kyoutuu,kei_ex_server,muhou,iroha#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

async def iroha(message,client1):
    m = message.channel.send
    await kyoutuu.itibu_kyoutuu_greeting(message)

    await kyoutuu.itibu_kyoutuu_thank(message)

    if message.channel.id == 605401823561383937:
        if not message.author.id == 606668660853178399:
            return
        if message.content.endswith("joined the server**"):
            await m("おはよー")
        if message.content.startswith(":skull:"):
            message_list = ["悲しい","ドンマイ","気をしっかり","えぇ"]
            send = random.choice(message_list)
            await m(send)
