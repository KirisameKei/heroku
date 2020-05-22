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
    await kyoutuu.itibu_kyoutuu_check_break(message,client1)
    await role_add_remove(message,client1,m)
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


async def role_add_remove(message,client1,m):
    if not message.author.bot:
        #役職付与・剥奪

        if message.content.startswith("/hide"):
            if not message.channel.id in channel_dic.my_guild_allow_command_channel:
                await m("ここで実行しないでください！")
                return
            role = discord.utils.get(message.guild.roles,name="かくれんぼなう")
            if message.content == "/hide me":
                if discord.utils.get(message.author.roles,name="かくれんぼなう"):
                    await m(message.author.name+"が見つかりませんでした。")
                else:
                    await message.author.add_roles(role)
                    await m(message.author.name+"が隠れました。もーいーよ！")
            else:
                user_id = message.content[6:]
                p = re.compile(r"^[0-9]+$")
                if not p.fullmatch(user_id):
                    await m("IDは18桁の半角数字です")
                    return
                user_id = int(user_id)
                member = message.guild.get_member(user_id)
                if discord.utils.get(member.roles,name="管理者"):
                    await m("管理者を隠そうとは・・・さてはこの鯖を乗っ取る気だなおめー")
                    return
                if discord.utils.get(member.roles,name="かくれんぼなう"):
                    await m(member.name+"は既に隠れているようです。私には見つけられませんでした。")
                    return
                await member.add_roles(role)
                await m(member.name+"が隠れました。もーいーよ！")

        if message.content.startswith("/find "):
            if not message.channel.id in channel_dic.my_guild_allow_command_channel:
                await m("ここで実行しないでください！")
                return
            role = discord.utils.get(message.guild.roles,name="かくれんぼなう")
            if message.content == "/find me":
                if discord.utils.get(message.author.roles,name="かくれんぼなう"):
                    await message.author.remove_roles(role)
                    await m(message.author.name+"、みーっけ！")
                else:
                    await m("もう見つけてるよ・・・")
            else:
                user_id = message.content[6:]
                p = re.compile(r"^[0-9]+$")
                if not p.fullmatch(user_id):
                    await m("IDは18桁の半角数字です")
                    return
                user_id = int(user_id)
                member = message.guild.get_member(user_id)
                if not discord.utils.get(member.roles,name="かくれんぼなう"):
                    await m("そこにいるよ・・・")
                    return
                await member.remove_roles(role)
                await m(member.name+"、みーっけ！")


        if message.content == "/delallow":
            if not discord.utils.get(message.author.roles,name="管理者"):
                await m("何様のつもり？")
                doM = discord.utils.get(message.guild.roles,name="ドM")
                await message.author.add_roles(doM)
                return
            if not message.channel.id == 597122356606926870:#ここにマル秘のIDを入れる
                await m("ここで実行しないでください！")
                return
            role = discord.utils.get(message.guild.roles,name="delmsg許可")
            await message.author.add_roles(role)
            await m(message.author.name+"にdelmsg許可を付与しました。")

        if message.content.startswith("/delmsg"):
            role = discord.utils.get(message.guild.roles,name="delmsg許可")
            if not discord.utils.get(message.author.roles,name="delmsg許可"):
                await m("何様のつもり？")
                doM = discord.utils.get(message.guild.roles,name="ドM")
                await message.author.add_roles(doM)
                return
                
            if message.content == "/delmsg":
                await message.channel.purge()
                await message.author.remove_roles(role)
            else:
                sakusyosuu = message.content[8:]
                p = re.compile(r"^[0-9]+$")
                if p.fullmatch(sakusyosuu):
                    sakusyosuu = int(sakusyosuu) + 1
                    await message.channel.purge(limit=sakusyosuu)
                    await message.author.remove_roles(role)


async def my_server_commands(message,client1,m):

    if message.content == "/omikuji" or message.content == "/speca" or message.content == "/meigen" or \
        message.content.startswith("/osusume_") or message.content.startswith("/name ") or message.content.startswith("/weather ") or \
        message.content.startswith("/stimer ") or message.content.startswith("/mtimer ") or message.content.startswith("/htimer ") or \
        message.content.startswith("/role_count ") or message.content.startswith("/mcid ") or message.content.startswith("/vote ") or \
        message.content.startswith("/mcavatar ") or message.content == "/help":
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