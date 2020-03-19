import discord,random,re,datetime,json,time,math,os,asyncio,requests,bs4,ast,sys,traceback
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用

import server_log,kyoutuu,kei_ex_server,muhou#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

async def kei_ex_server_log(message,client1):
    now = datetime.datetime.now().strftime("%H:%M")
    embed = discord.Embed(description=message.content,color=0xfffffe)
    embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    embed.set_footer(text=now)
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    try:
        write_channel = channel_dic.my_guild_log_dic[message.channel.id]
        write_channel = client1.get_channel(write_channel)
        await write_channel.send(embed=embed)
    except KeyError:
        channel_dic_channel = client1.get_channel(663037675141595147)
        channel_dic_in_embed = await channel_dic_channel.fetch_message(682935760512352274)
        channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
        channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
        write_channel = channel_dic_in_channel[message.channel.id]
        write_channel = client1.get_channel(write_channel)
        await write_channel.send(embed=embed)

async def syobatubu_server_log(message,client1):
    now = datetime.datetime.now().strftime("%H:%M")
    embed = discord.Embed(description=message.content,color=0xfffffe)
    embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    embed.set_footer(text=now)
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    try:
        write_channel = channel_dic.syobatubu_log_dic[message.channel.id]
        write_channel = client1.get_channel(write_channel)
        await write_channel.send(embed=embed)
    except KeyError:
        channel_dic_channel = client1.get_channel(663037675141595147)
        channel_dic_in_embed = await channel_dic_channel.fetch_message(682944795794079767)
        channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
        channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
        write_channel = channel_dic_in_channel[message.channel.id]
        write_channel = client1.get_channel(write_channel)
        await write_channel.send(embed=embed)

async def iroha_server_log(message,client1):
    now = datetime.datetime.now().strftime("%H:%M")
    embed = discord.Embed(description=message.content,color=0xfffffe)
    embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    embed.set_footer(text=now)
    if message.attachments:
        embed.set_image(url=message.attachments[0].url)
    try:
        write_channel = channel_dic.iroha_server_log_dic[message.channel.id]
        write_channel = client1.get_channel(write_channel)
        await write_channel.send(embed=embed)
    except KeyError:
        channel_dic_channel = client1.get_channel(663037675141595147)
        channel_dic_in_embed = await channel_dic_channel.fetch_message(682944796834398336)
        channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
        channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
        write_channel = channel_dic_in_channel[message.channel.id]
        write_channel = client1.get_channel(write_channel)
        await write_channel.send(embed=embed)