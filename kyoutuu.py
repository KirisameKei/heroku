import discord,random,re,datetime,json,time,math,os,asyncio,io,bs4,chromedriver_binary,asyncio,requests
from PIL import Image,ImageDraw,ImageFont
from selenium import webdriver
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

#from quote import expand#メッセージリンク展開用
from discord import Embed

import server_log,kyoutuu,kei_ex_server,muhou#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

now = datetime.datetime.now()
client1 = discord.Client()

async def kanzen_kyoutuu_message_link(message,client1,client4):
    m = message.channel.send
    #メッセージURL先を表示する
    if "https://discordapp.com/channels/" in message.content:
        for url in message.content.split( 'https://discordapp.com/channels/' )[1:]:
            try:
                guild_id = int(url[0:18])
                channel_id = int(url[19:37])
                message_id = int(url[38:56])
                try:
                    guild = client1.get_guild(guild_id)
                    ch = guild.get_channel(int(channel_id))
                    msg = await ch.fetch_message(int(message_id))
                except AttributeError:
                    faild_embed = discord.Embed(title="404NotFriend")
                    await message.channel.send(embed=faild_embed)
                    return

                def quote_reaction(msg,embed):
                    if msg.reactions:
                        reaction_send = ""
                        for reaction in msg.reactions:
                            emoji = reaction.emoji
                            count = str(reaction.count)
                            reaction_send = f"{reaction_send}{emoji}{count}"
                        embed.add_field(name="reaction",value=reaction_send,inline=False)
                    return embed
                if msg.embeds or msg.content or msg.attachments:
                    embed = Embed(description=msg.content,timestamp=msg.created_at)
                    embed.set_author(name=msg.author,icon_url=msg.author.avatar_url)
                    embed.set_footer(text=msg.channel.name,icon_url=msg.guild.icon_url)
                    if msg.attachments:
                        embed.set_image(url=msg.attachments[0].url)
                    embed = quote_reaction(msg,embed)
                    if msg.content or msg.attachments:
                        await message.channel.send(embed=embed)
                    if len(msg.attachments) >= 2:
                        for attachment in msg.attachments[1:]:
                            embed = Embed().set_image(url=attachment.url)
                            await message.channel.send(embed=embed)
                    for embed in msg.embeds:
                        embed = quote_reaction(msg,embed)
                        await message.channel.send(embed=embed)
                else:
                    await message.channel.send("メッセージIDは存在しますが、内容がありません")
            except discord.errors.NotFound:
                await message.channel.send("指定したメッセージが見つかりません")

    if message.content == "/report":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSfK9DQkUCD2qs8zATUuYIC3JuV3MyXRVCYjMb5g4g_hBUusSA/viewform")
    if message.content == "/failure":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSdn9fTTs55c-oGLT3c68KVTGvfUjTK-W_cdataU7_XyzqcBRg/viewform")
    if message.content == "/idea":
        await m("http://w4.minecraftserver.jp/ideaForm")
    if message.content == "/opinion":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSctLrByNvAiQop2lha9Mxn-D5p1OUaOf8JKQJCyAdggGBbzpg/viewform?c=0&w=1")
    if message.content == "/donation":
        await m("https://docs.google.com/forms/d/e/1FAIpQLSezwur20tx0JCQ0KMY0JiThYy7oEQDykFRiic96KxK17WOBwA/viewform?c=0&w=1")
    if message.content == "/inquiry":
        await m("https://w4.minecraftserver.jp/inquiryForm")

    if message.content == "/form":
        embed = discord.Embed(title="各フォームへのリンク一覧",color=0xff0000)
        embed.add_field(name="通報フォーム",value="https://docs.google.com/forms/d/e/1FAIpQLSfK9DQkUCD2qs8zATUuYIC3JuV3MyXRVCYjMb5g4g_hBUusSA/viewform",inline=False)
        embed.add_field(name="不具合フォーム",value="https://docs.google.com/forms/d/e/1FAIpQLSdn9fTTs55c-oGLT3c68KVTGvfUjTK-W_cdataU7_XyzqcBRg/viewform",inline=False)
        embed.add_field(name="アイデアフォーム",value="http://w4.minecraftserver.jp/ideaForm",inline=False)
        embed.add_field(name="意見・感想フォーム",value="https://docs.google.com/forms/d/e/1FAIpQLSctLrByNvAiQop2lha9Mxn-D5p1OUaOf8JKQJCyAdggGBbzpg/viewform?c=0&w=1",inline=False)
        embed.add_field(name="寄付フォーム",value="https://docs.google.com/forms/d/e/1FAIpQLSezwur20tx0JCQ0KMY0JiThYy7oEQDykFRiic96KxK17WOBwA/viewform?c=0&w=1",inline=False)
        embed.add_field(name="お問い合わせフォーム",value="https://w4.minecraftserver.jp/inquiryForm",inline=False)
        await m(embed=embed)

    if message.content == "/formal":
        await m("https://www.seichi.network/gigantic")
    if message.content == "/informal":
        await m("https://seichi-click-network.sokuhou.wiki/")

    if message.content == "/new_func":
        await m("```\n機能追加の申請をします。\n各項目は全て1回の送信で書いてください。\n\
各項目は10分でタイムアウトします。\n備考などがない場合はなしと入力してください。\n\
複雑な場合は直接言っていただいても構いません。```")
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

    if message.content == "/daily_ranking":
        driver = webdriver.Chrome()
        haikei = Image.new(mode="RGB",size=(840,2000),color=0xffffff)
        moji = ImageDraw.Draw(haikei)
        try:
            font1 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=72)
            font2 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=36)
        except OSError:
            font1 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=72)
            font2 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=36)

        for j in range(3):
            try:
                driver.get("https://w4.minecraftserver.jp/#page=1&type=break&duration=daily")
                html = driver.page_source.encode('utf-8')
                soup = bs4.BeautifulSoup(html, "html.parser")

                #情報を選別
                number = []
                number_img = []
                for i in range(20):
                    #全体を取得
                    n = soup.select_one(f"#ranking-container > div > div > table > tbody > tr:nth-child({i+1}) > td:nth-child(3)")
                    number.append(n)
                    #アイコン
                    n = str(soup.select_one(f"#ranking-container > div > div > table > tbody > tr:nth-child({i+1}) > td:nth-child(2) > div > img"))
                    icon_url = n[24:-16]
                    number_img.append(icon_url)
        
                for i in range(20):
                    mcid = number[i].text.split("：")[0].replace("整地量","")
                    seitiryou = number[i].text.split("：")[1].replace("Last quit","")
                    r = requests.get(number_img[i])
                    image = io.BytesIO(r.content)
                    image.seek(0)
                    icon = Image.open(image)

                    haikei.paste(icon,(180,100*i+2))

                    moji.text((0,100*i+14),text=f"{i+1}位",font=font1,fill=0x000000)
                    moji.text((320,100*i+32),text=mcid,font=font2,fill=0x000000)
                    moji.text((620,100*i+32),text=seitiryou,font=font2,fill=0x000000)
            except AttributeError:
                await asyncio.sleep(3)
            else:
                print(j)
                break

        haikei.save(r"c:\users\hayab\desktop\pic.png")
        p = discord.File(r"c:\users\hayab\desktop\pic.png")
        await message.channel.send(file=p)
        driver.close()


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
