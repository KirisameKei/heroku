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

async def kanzen_kyoutuu_message_link(message,client1,client4):
    m = message.channel.send
    #メッセージURL先を表示する
    if message.content.startswith("https://discordapp.com/channels/"):
        await expand(message,client1,client4)

    if message.content == "/report":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSfK9DQkUCD2qs8zATUuYIC3JuV3MyXRVCYjMb5g4g_hBUusSA/viewform")
    if message.content == "/failure":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSdn9fTTs55c-oGLT3c68KVTGvfUjTK-W_cdataU7_XyzqcBRg/viewform")
    if message.content == "/idea":
        await m("http://w4.minecraftserver.jp/ideaForm")
    if message.content == "opinion":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSctLrByNvAiQop2lha9Mxn-D5p1OUaOf8JKQJCyAdggGBbzpg/viewform?c=0&w=1")
    if message.content == "donation":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSezwur20tx0JCQ0KMY0JiThYy7oEQDykFRiic96KxK17WOBwA/viewform?c=0&w=1")
    if message.content == "inquiry":
        await m("https://w4.minecraftserver.jp/inquiryForm")

    if message.content == "/new_func":
        await m("機能追加の申請をします。\n各項目は全て1回の送信で書いてください。\n\
各項目は10分でタイムアウトします。\n備考などがない場合はなしと入力してください。\n\
複雑な場合は直接言っていただいても構いません。")
        await m("この依頼内容を公開してよろしいですか？\n良い場合はyes、悪い場合はnoと入力してください\n\
__**特殊な理由がない限りyesにしてください。**__")
        def koukai_settei(m):
            return m.content == "yes" or m.content == "no" and m.author == message.author and m.channel == message.channel
        try:
            reply0 = await client1.wait_for("message",check=koukai_settei,timeout=360)
        except asyncio.TimeoutError:
            await m("タイムアウトしました。最初からやり直してください。")
        else:
            await m("何をしたら？\n例：/seichiと入力したら、16時になったら等")
            def naniwositara(m):
                return m.author == message.author and m.channel == message.channel
            try:
                reply1 = await client1.wait_for("message",check=naniwositara,timeout=360)
            except asyncio.TimeoutError:
                await m("タイムアウトしました。最初からやり直してください。")
            else:
                await m("何をする？\n例：整地鯖役職を付与する、チャンネルにあるメッセージをすべて消去する等")
                def naniwosuru(m):
                    return m.author == message.author and m.channel == message.channel
                try:
                    reply2 = await client1.wait_for("message",check=naniwosuru,timeout=360)
                except asyncio.TimeoutError:
                    await m("タイムアウトしました。最初からやり直してください。")
                else:
                    await m("チャンネル、役職の指定は？\n例：Hypixl役職持ちが実行すると怒られる、<#603832801036468244>を消す等")
                    def sonotanojyouken(m):
                        return m.author == message.author and m.channel == message.channel
                    try:
                        reply3 = await client1.wait_for("message",check=sonotanojyouken,timeout=360)
                    except asyncio.TimeoutError:
                        await m("タイムアウトしました。最初からやり直してください。")
                    else:
                        await m("その他備考は？\n他に要求がある場合ここに書いてください。")
                        def bikou(m):
                            return m.author == message.author and m.channel == message.channel
                        try:
                            reply4 = await client1.wait_for("message",check=bikou,timeout=360)
                        except asyncio.TimeoutError:
                            await m("タイムアウトしました。最初からやり直してください。")
                        else:
                            embed = discord.Embed(title="これで申請してよろしいですか？",description="良ければyes、やり直すならnoと入力してください",color=0xfffffe)
                            embed.add_field(name="やりたいこと",value=reply1.content+reply2.content,inline=False)
                            embed.add_field(name="条件の指定",value=reply3.content)
                            embed.add_field(name="備考",value=reply4.content)
                            if reply0.content == "yes":
                                koukai_hikoukai = "公開"
                            if reply0.content == "no":
                                koukai_hikoukai = "非公開"
                            embed.add_field(name="公開設定",value=koukai_hikoukai,inline=False)
                            await m(embed=embed)
                            def kakunin(m):
                                return m.content == "yes" or m.content == "no" and m.author == message.author and m.channel == message.channel
                            try:
                                send_msg = await client1.wait_for("message",check=kakunin,timeout=360)
                            except asyncio.TimeoutError:
                                await m("タイムアウトしました。最初からやり直してください。")
                            else:
                                embed = discord.Embed(title="依頼が届きました",color=0x00ff00)
                                embed.add_field(name="やりたいこと",value=reply1.content+reply2.content,inline=False)
                                embed.add_field(name="条件の指定",value=reply3.content)
                                embed.add_field(name="備考",value=reply4.content)
                                embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                                embed.set_footer(text=message.guild.name,icon_url=message.guild.icon_url)
                                if send_msg.content == "yes":
                                    if reply0.content == "yes":#公開していいなら
                                        yarukoto = client1.get_channel(636359382359080961)
                                        await yarukoto.send("<@!523303776120209408>\n",embed=embed)
                                        await m("依頼内容を<#636359382359080961>に送信しました。回答をお待ちください。\n\
疑問点がある、情報が不十分等の理由でメンションやDMをさせていただく場合があります。")
                                    if reply0.content == "no":#公開禁止なら
                                        kei = client1.get_user(523303776120209408)
                                        dm = await kei.create_dm()
                                        await dm.send(embed=embed)
                                        await m("依頼内容をけいのDMに送信しました。回答をお待ちください。\n\
疑問点がある、情報が不十分等の理由でDMを送らせていただく場合があります。")
                                if send_msg.content == "no":
                                    await m("最初からやり直してください。")


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
        await m(":eggplant:")

async def itibu_kyoutuu_mention(message,client1):#メンション対応
    m = message.channel.send
    if message.author.bot:
        return
    if  client1.user in message.mentions:
        await m("おいゴラァ")
        await m("やめろ")
        await m("てめぇ常識持ってんのか？")
        await m("誰にメンション飛ばしたと思ってるんだ")
