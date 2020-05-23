import discord,random,re,datetime,json,time,math,os,asyncio,io,bs4,chromedriver_binary,asyncio,requests,ast
from PIL import Image,ImageDraw,ImageFont
from selenium import webdriver
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

#from quote import expand#メッセージリンク展開用
from discord import Embed

import kyoutuu#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import my_guild_role_dic,message_list#このbotを動かすのに必要な辞書とリスト

client1 = discord.Client()


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
