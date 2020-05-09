import discord,random,re,datetime,json,time,math,os,asyncio,io,bs4,chromedriver_binary,asyncio,requests,ast
from PIL import Image,ImageDraw,ImageFont
from selenium import webdriver
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

#from quote import expand#メッセージリンク展開用
from discord import Embed

import kyoutuu,kei_ex_server,muhou#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

client1 = discord.Client()

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
    now = datetime.datetime.now()
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


async def itibu_kyoutuu_daily_ranking(message):
    if message.content == "/daily_ranking":
        driver = webdriver.Chrome()
        haikei = Image.new(mode="RGB",size=(840,2100),color=0xffffff)
        moji = ImageDraw.Draw(haikei)
        try:
            font1 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=72)
            font2 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=36)
            font3 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=48)
        except OSError:
            font1 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=72)
            font2 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=36)
            font3 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=48)

        now = datetime.datetime.now()
        year = now.year
        month = now.month
        day = now.day
        hour = now.hour
        minute = now.minute
    
        moji.text((0,14),f"{year}年{month}月{day}日{hour}時{minute}分の整地量",font=font3,fill=0x000000)

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

                    haikei.paste(icon,(180,100*(i+1)+2))

                    moji.text((0,100*(i+1)+14),text=f"{i+1}位",font=font1,fill=0x000000)
                    moji.text((320,100*(i+1)+32),text=mcid,font=font2,fill=0x000000)
                    moji.text((620,100*(i+1)+32),text=seitiryou,font=font2,fill=0x000000)
            except AttributeError:
                await asyncio.sleep(3)
            else:
                break

        haikei.save(r"c:\users\hayab\desktop\pic.png")
        p = discord.File(r"c:\users\hayab\desktop\pic.png")
        picture = await message.channel.send(file=p)
        #url = picture.attachments[0].url

        try:
            import tokens
            webhook_url = tokens.kei_ex_server_webhook_url
        except ModuleNotFoundError:
            webhook_url = os.getenv("kei_ex_sercer_webhook_url")
        
        webhook = discord.Webhook.from_url(webhook_url,adapter=discord.RequestsWebhookAdapter())
        p = discord.File(r"c:\users\hayab\desktop\pic.png")
        webhook.send(file=p,username="ラッキーさんありがとう",avatar_url="https://avatar.minecraft.jp/kei_3104/minecraft//m.png")
        
        """
        main_content = {
            "username":"webhook_test",
            "avatar_url":"https://avatar.minecraft.jp/kei_3104/minecraft//m.png",
            "embeds":[
                {
                    "image":{
                        "url":url
                    }
                }
            ]
        }

        requests.post(webhook_url,json.dumps(main_content),headers={'Content-Type': 'application/json'})"""
        driver.close()

async def daily_ranking(client1):
    driver = webdriver.Chrome()
    haikei = Image.new(mode="RGB",size=(840,2100),color=0xffffff)
    moji = ImageDraw.Draw(haikei)
    try:
        font1 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=72)
        font2 = ImageFont.truetype(r"c:\Windows\Fonts\UDDigiKyokashoN-R.ttc",size=36)
    except OSError:
        font1 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=72)
        font2 = ImageFont.truetype("./UDDigiKyokashoN-R.ttc",size=36)

    now = datetime.datetime.now()
    year = now.year
    month = now.month
    day = now.day
    
    moji.text((0,14),f"{year}年{month}月{day}日の整地量",font=font1,fill=0x000000)

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

                haikei.paste(icon,(180,100*(i+1)+2))

                moji.text((0,100*(i+1)+14),text=f"{i+1}位",font=font1,fill=0x000000)
                moji.text((320,100*(i+1)+32),text=mcid,font=font2,fill=0x000000)
                moji.text((620,100*(i+1)+32),text=seitiryou,font=font2,fill=0x000000)
        except AttributeError:
            await asyncio.sleep(3)
        else:
            break

    haikei.save(r"c:\users\hayab\desktop\pic.png")
    p = discord.File(r"c:\users\hayab\desktop\pic.png")
    channel = client1.get_channel(689277331915014146)
    picture = await channel.send(file=p)
    driver.close()


async def itibu_kyoutuu_check_break(message,client1):
    if message.content.startswith("/break "):
        mcid = message.content[7:]
        url = f"https://api.mojang.com/users/profiles/minecraft/{mcid}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            try:
                mcid_uuid_dict = ast.literal_eval(str(bs4.BeautifulSoup(res.text, "html.parser")))
            except SyntaxError:
                await message.channel.send(f"{mcid}は実在しません。")
                return
            uuid = mcid_uuid_dict["id"]
            uuid_1 = uuid[:8]
            uuid_2 = uuid[8:12]
            uuid_3 = uuid[12:16]
            uuid_4 = uuid[16:20]
            uuid_5 = uuid[20:]
            uuid = f"{uuid_1}-{uuid_2}-{uuid_3}-{uuid_4}-{uuid_5}"
        except requests.exceptions.HTTPError:
            await message.channel.send("現在この機能はご利用いただけません。1")
        
        url = f"https://w4.minecraftserver.jp/api/ranking/player/{uuid}?types=break"
        try:
            res = requests.get(url)
            res.raise_for_status()
            player_data_dict = ast.literal_eval(str(bs4.BeautifulSoup(res.text, "html.parser")))[0]
        except requests.exceptions.HTTPError:
            await message.channel.send(f"サーバが応答を停止しているか{mcid}は整地鯖で認識されていないMCIDです。")
            await message.channel.send(uuid)
            return

        broke = int(player_data_dict["data"]["raw_data"])
        rank = player_data_dict["rank"]
        mc_avatar_url = f"http://avatar.minecraft.jp/{mcid}/minecraft/m.png"

        if broke < 15:
            level = 1
        elif broke < 49:
            level = 2
        elif broke < 106:
            level = 3
        elif broke < 198:
            level = 4
        elif broke < 333:
            level = 5
        elif broke < 705:
            level = 6
        elif broke < 1265:
            level = 7
        elif broke < 2105:
            level = 8
        elif broke < 9557:#2105～9556までがこのelfi文内に入る
            level = 9
            n = 2015
            while True:
                n += 1242
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 11047:
            level = 15
        elif broke < 12835:
            level = 16
        elif broke < 14980:
            level = 17
        elif broke < 17554:
            level = 18
        elif broke < 20642:
            level = 19
        elif broke < 24347:
            level = 20
        elif broke < 28793:
            level = 21
        elif broke < 34128:
            level = 22
        elif broke < 40530:
            level = 23
        elif broke < 48212:
            level = 24
        elif broke < 57430:
            level = 25
        elif broke < 68491:
            level = 26
        elif broke < 81764:
            level = 27
        elif broke < 97691:
            level = 28
        elif broke < 212363:
            level = 29
            n = 97691
            while True:
                n += 19112
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 235297:
            level = 35
        elif broke < 262817:
            level = 36
        elif broke < 295891:
            level = 37
        elif broke < 335469:
            level = 38
        elif broke < 383022:
            level = 39
        elif broke < 434379:
            level = 40
        elif broke < 489844:
            level = 41
        elif broke < 549746:
            level = 42
        elif broke < 614440:
            level = 43
        elif broke < 684309:
            level = 44
        elif broke < 759767:
            level = 45
        elif broke < 841261:
            level = 46
        elif broke < 929274:
            level = 47
        elif broke < 1024328:
            level = 48
        elif broke < 1126986:
            level = 49
        elif broke < 1250000:
            level = 50
        elif broke < 2375000:
            level = 51
            n = 1250000
            while True:
                n += 125000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 4125000:
            level = 60
            n = 2375000
            while True:
                n += 175000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 6325000:
            level = 70
            n = 4215000
            while True:
                n += 220000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 9215000:
            level = 80
            n = 6325000
            while True:
                n += 280000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 13165000:
            level = 90
            n = 9215000
            while True:
                n += 360000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 13615000:
            level = 100
        elif broke < 17665000:
            level = 101
            n = 13615000
            while True:
                n += 450000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 22565000:
            level = 110
            n = 13615000
            while True:
                n += 490000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 27965000:
            level = 120
            n = 22565000
            while True:
                n += 540000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 33865000:
            level = 130
            n = 27965000
            while True:
                n += 590000
                if broke <n:
                    break
                else:
                    level += 1
        elif broke < 40465000:
            level = 140
            n = 33865000
            while True:
                n += 660000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 47865000:
            level = 150
            n = 40465000
            while True:
                n += 740000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 56065000:
            level = 160
            n = 47865000
            while True:
                n += 820000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 65265000:
            level = 170
            n = 56065000
            while True:
                n += 920000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 75265000:
            level = 180
            n = 65265000
            while True:
                n += 1000000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 85615000:
            level = 190
            n = 75265000
            while True:
                n += 1150000
                if broke < n:
                    break
                else:
                    level += 1
        elif broke < 87115000:
            level = 199
        else:
            level = 200
            star_level,amari = divmod(broke,87115000)

        try:
            embed = discord.Embed(title=f"{mcid}",description=f"整地量：{broke}\n順位：{rank}\nレベル：{level}☆{star_level}")
        except UnboundLocalError:
            embed = discord.Embed(title=f"{mcid}",description=f"整地量：{broke}\n順位：{rank}\nレベル：{level}")

        embed.set_thumbnail(url=mc_avatar_url)
        await message.channel.send(embed=embed)
