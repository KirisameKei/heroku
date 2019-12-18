import discord,random,re,datetime,json,time,math,os,asyncio
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用

import server_log,kyoutuu,kei_ex_server,muhou#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

now = datetime.datetime.now()
client1 = discord.Client()

async def kanzen_kyoutuu_message_link(message,client1):
    m = message.channel.send
    #メッセージURL先を表示する
    if message.content.startswith("https://discordapp.com/channels/"):
        await expand(message,client1,client4)


async def itibu_kyoutuu_greeting(message):#あいさつ
    m = message.channel.send
    if message.author.bot:
        return
    if "おはよう" in message.content:
        if now.hour >= 5 and now.hour <= 10:
            await m("おはようございます、**__"+message.author.name+"__**さん！")
        else:
            await m("今おはよう！？")
    if "こんにちは" in message.content:
        if now.hour >= 9 and now.hour <= 17:
            await m("こんにちは、**__"+message.author.name+"__**さん！")
        else:
            await m("今こんにちは！？")
    if "こんばんは" in message.content:
        if now.hour >= 18 and now.hour <= 23:
            await m("こんばんは、**__"+message.author.name+"__**さん！")
        else:
            await m("今こんばんは！？")


async def itibu_kyoutuu_thank(message):#お礼
    m = message.channel.send
    if message.author.bot:
        return    
    if "ありがとう" in message.content:
        kouho = [
            "ありナス！",
            "いえいえ～",
            "どういたしまして！",
            "気にしないで～",
            ":eggplant:"
        ]
        send = random.choice(kouho)
        await m(send)

async def itibu_kyoutuu_mention(message,client1):#メンション対応
    m = message.channel.send
    if message.author.bot:
        return
    if  client1.user in message.mentions:
        await m("おいゴラァ")
        await m("やめろ")
        await m("てめぇ常識持ってんのか？")
        await m("誰にメンション飛ばしたと思ってるんだ")
