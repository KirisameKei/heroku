import discord,random,re,datetime,json,time,math,os,asyncio,ast,requests,bs4
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用

import kyoutuu#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)

async def iroha(message,client1):
    m = message.channel.send

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