import discord,random,re,datetime,json,time,math,os,asyncio,requests,bs4,ast
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート/name

import kyoutuu#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import my_guild_role_dic,message_list,channel_dic#このbotを動かすのに必要な辞書とリスト

async def kei_ex_server(message,client1):
    m = message.channel.send
    await kyoutuu.itibu_kyoutuu_daily_ranking(message)
    await my_server_commands(message,client1,m)

    if message.channel.id == 603832801036468244:
        if message.content.endswith("ん") or message.content.endswith("ン"):
            choice = random.choice(message_list.siritori_nn)
            await m(choice)

    if message.content == "魔理ちゃんのことが大好きです":
        if message.author.name == "けい":
            await m("私も好きだぜ///")
        else:
            await m("ごめんな、私はけいさんのことが好きなんだぜ・・・")

    if message.content == "/marichan_invite":
        if not message.channel.id in channel_dic.my_guild_allow_command_channel:
            await m(f"{message.author.mention}\nここで実行しないでください！\nコマンド漏洩防止のためメッセージを削除します。")
            await message.delete()
            return
        dm = await message.author.create_dm()
        marichan_inviter_role = discord.utils.get(message.guild.roles,id=663542711290429446)
        await message.author.add_roles(marichan_inviter_role)
        await message.delete()
        await m("コマンド漏洩防止のためメッセージを削除しました。")
        await dm.send("https://discordapp.com/api/oauth2/authorize?client_id=594052349140402179&permissions=338783443&scope=bot")
        await m(f"{message.author.mention}\nDMに招待リンクを送信しました。(管理者権限を持っているサーバに導入できます)")


async def my_server_commands(message,client1,m):

    if message.content.startswith("/vote ") or message.content.startswith("/mcavatar "):
        if not message.channel.id in channel_dic.my_guild_allow_command_channel:
            await m("ここで実行しないでください！")
            return

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

        if message.content.startswith("/mcavatar "):
            mcid = message.content.replace("/mcavatar ","")
            await m(f"http://avatar.minecraft.jp/{mcid}/minecraft/m.png")