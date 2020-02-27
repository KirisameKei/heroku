import discord,random,re,datetime,json,time,math,os,asyncio,ast
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
            mcid = message.content.split()[1].replace("**","").replace("\\","")
            today_login_channel = client1.get_channel(682410834705907780)
            today_login_mcid_in_embed = await today_login_channel.fetch_message(682423757951991908)
            mcids = today_login_mcid_in_embed.embeds[0].description
            today_login_mcid_list = ast.literal_eval(mcids)
            if mcid in today_login_mcid_list:
                pass
            else:
                today_login_mcid_list.append(mcid)
                today_login_mcid_list = str(today_login_mcid_list)
                logined_mcid_embed = discord.Embed(description=today_login_mcid_list)
                await today_login_mcid_in_embed.edit(embed=logined_mcid_embed)
                await m("おはよー")

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
