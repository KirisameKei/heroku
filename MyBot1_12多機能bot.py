import discord
import random
import re
from discord.ext import tasks
from datetime import datetime 

client = discord.Client()
mee = 'MEE6'
poke = 'Pokécord'
win = '私の勝ち!何で負けたのか次回ま(ry'
lose = 'あなたの勝ち!やるやん'
aiko = 'あいこ!やり直し'

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    channel = client.get_channel(595072269483638785)
    await channel.send('MyBot2がログインしました')
    

@client.event
async def on_message(message):
    # 「おはよう」と一致するか調べる
    if message.content=="おはよう":
            # メッセージを書きます
            m = "おはようございます" + message.author.name + "さん！"
            await message.channel.send(m)
    # 「こんにちは」と一致するか調べる
    if message.content=="こんにちは":
            # メッセージを書きます
            m = "こんにちは" + message.author.name + "さん！"
            await message.channel.send(m)
    # 「こんばんは」と一致するか調べる
    if message.content=="こんばんは":
            # メッセージを書きます
            m = "こんばんは" + message.author.name + "さん！"
            await message.channel.send(m)
    
    if message.content=="/speca":#送られたメッセージが/specaと一致するなら
            speca = ["反魂蝶「n分咲き」","「無双風神」","紫奥義「弾幕結界」"]
            reply = (random.choice(speca))
            await message.channel.send(reply)
    
    if message.content=="/spam":#送られたメッセージが/specaと一致するなら
        tyuusen = ["/spam","/spam","/spam","/spam","/sparn"]
        spam = (random.choice(tyuusen))
        await message.channel.send(spam)

    if message.content == "/fairy":
        mana = ["やあ!","うわーん!お腹空いたよー!","(';ω;`)ｳｩｩ ﾋﾓｼﾞｲ…","がちゃりんごがっ!食べたいっ!","@うんちゃま",\
            "お腹空いたなぁー。","あぁ!幸せ!","いつもりんごをありがとう!","のりんごはおいしいなあ","には帰るよー。","がちゃりんごっておいしいよね!",\
            "('～`)ﾓｸﾞﾓｸﾞ…","はどのりんごが好き？ぼくはがちゃりんご!","動いてお腹を空かしていっぱい食べるぞー!","たくさん働いて、たくさんりんごを食べようね!",\
            "ちょっと食べ疲れちゃった","整地しないのー？","あ、もうこんな時間だ!","じゃーねー!"]
        send = (random.choice(mana))
        sousinsya = message.author.name
        if send == "@うんちゃま":
            await message.channel.send(send+"　"+sousinsya+"が意地悪するんだっ!")
        elif send == "やあ!":
            await message.channel.send(send+sousinsya)
        elif send == "のりんごはおいしいなあ":
            await message.channel.send(sousinsya+send)
        elif send == "はどのりんごが好き？ぼくはがちゃりんご!":
            await message.channel.send(sousinsya+send)
        elif send == "じゃーねー!":
            await message.channel.send(send+sousinsya)
        elif send =="には帰るよー。":
            now = datetime.now().strftime('%H:%M')#現在の時刻
            await message.channel.send("僕は"+now+send)
        else:
            await message.channel.send(send)

    if message.channel.id == 603832801036468244:
        if client.user != message.author:
            if message.content.endswith ("ン"):
                channel = client.get_channel(603832801036468244)
                end = ["ンジャメナ","ンゴロンゴロ","ンカイ","ンガミ湖","ンズワニ島","ンゼレコレ","ンスタ","ンスカ","ンジャジジャ島"]
                send = (random.choice(end))
                await message.channel.send(send)
        if client.user != message.author:
            if message.content.endswith ("ん"):
                channel = client.get_channel(603832801036468244)
                end = ["ンジャメナ","ンゴロンゴロ","ンカイ","ンガミ湖","ンズワニ島","ンゼレコレ","ンスタ","ンスカ","ンジャジジャ島"]
                send = (random.choice(end))
                await message.channel.send(send)
        
          
    if message.channel.id != 588224929300742154:  
        if message.author.name == mee:#送り主がみーなら
            bougen = [":middle_finger:","少し静かにしていただけますか？","ちょっと黙っててもらっていいですか？","お引き取りください","f*ck",\
                "たいそうにぎやかなご様子でいらっしゃいますところまことに恐縮でございますが、ご逝去あそばしていただければ幸甚に存じます"]#送るメッセージの候補
            messe = (random.choice(bougen))#bougenの中からランダムに一つ選ぶ
            m = "<@!159985870458322944> "
            await message.channel.send(m+messe)#MEE6の発言したチャンネルに発言
        if message.author.name == poke:
            bougen = [":middle_finger:","少し静かにしていただけますか？","ちょっと黙っててもらっていいですか？","お引き取りください","f*ck",\
                "たいそうにぎやかなご様子でいらっしゃいますところまことに恐縮でございますが、 ご逝去あそばしていただければ幸甚に存じます"]#送るメッセージの候補
            messe = (random.choice(bougen))#bougenの中からランダムに一つ選ぶ
            n = "<@!365975655608745985> "
            await message.channel.send(n+messe)

    if message.channel.id == 604534441175678995:
        if client.user != message.author:
            p = re.compile(r'^[0-9]+$')
            if p.fullmatch(message.content):#メッセージが数字のみで
                if message.content == "0":#送られてきたメッセージが0なら
                    kouho = ["0","2","5"]
                    reply = (random.choice(kouho))
                    await message.channel.send(reply)
                    if reply == "0":
                        await message.channel.send(aiko)
                    elif reply == "2":
                        await message.channel.send(lose)
                    else :
                        await message.channle.send(win)
                elif message.content == "2":
                    kouho = ["0","2","5"]
                    reply = (random.choice(kouho))
                    await message.channel.send(reply)
                    if reply == "0":
                        await message.channel.send(win)
                    elif reply == "2":
                        await message.channel.send(aiko)
                    else :
                        await message.channel.send(lose)
                elif message.content == "5":
                    kouho = ["0","2","5"]
                    reply = (random.choice(kouho))
                    await message.channel.send(reply)
                    if reply == "0":
                        await message.channel.send(lose)
                    elif reply == "2":
                        await message.channel.send(win)
                    else :
                        await message.channel.send(aiko)
                else :
                    person = message.author.name
                    num = message.content
                    await message.channel.send(person+"はじゃんけんをするとき"+num+"本の指を出すんだね!")
            else :
                await message.channel.send("数字のみを入力してください!")


@tasks.loop(seconds=60)#60秒に一回ループ
async def loop():
    weekday = datetime.today().weekday()#現在の曜日
    if weekday == 6:
        now = datetime.now().strftime('%H:%M')#現在の時刻
        if now == '02:19':
            channel = client.get_channel(603832801036468244)
            await channel.purge()
        if now == '02:20':
            channel = client.get_channel(603832801036468244)
            start = ['しりとり','霧雨魔理沙(きりさめまりさ)','多々良小傘(たたらこがさ)','リリカ・プリズムリバー']
            hajime = (random.choice(start))
            await channel.send(hajime)

loop.start()#ループ処理実行

client.run("NTk0Mzk2ODMwMDcxMjU5MTU0.XRb1mg.hWK_vQgiQW0t3guUCJclVDYp_Z4")