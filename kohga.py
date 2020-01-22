import discord,random,re,datetime,json,time,math,os,asyncio
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

async def kohga(message,client1,m):
    if message.channel.id == :#チャンネルIDを入力
        if message.author.bot:
            return
        choice = random.randint(1,30)
        msg = ""
        for i in range(choice):
            msg += "あ"
        await m(msg)