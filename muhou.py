import discord,random,re,datetime,json,time,math,os,asyncio
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用

import server_log,kyoutuu,kei_ex_server,muhou#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト
client1 = discord.Client()

async def muhou(message):
    m = message.channel.send
    await kyoutuu.itibu_kyoutuu_greeting(message)

    await kyoutuu.itibu_kyoutuu_thank(message)

    await kyoutuu.itibu_kyoutuu_mention(message,client1)

    if message.author.id == 159985870458322944 or message.author.id == 365975655608745985:
        anti_message_list = [
            ":middle_finger:",
            "少し静かにしていただけますか？",
            "ちょっと黙っててもらっていいですか？",
            "お引き取りください",
            "f*ck",
            "たいそうにぎやかなご様子でいらっしゃいますところまことに恐縮でございますが、ご逝去あそばしていただければ幸甚に存じます"
        ]
        choice = random.choice(anti_message_list)
        await m(message.author.mention+choice)