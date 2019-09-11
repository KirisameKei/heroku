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
    await channel.send(client.user.name+'がログインしました')


@client.event
async def on_member_join(member):
    role = discord.utils.get(member.guild.roles,id=586123363513008139)
    await member.add_roles(role)
    come = member.name
    channel = client.get_channel(588224929300742154)
    channel1 = client.get_channel(586000955053441039)
    msg1 = f"{channel1.mention}"
    channel2 = client.get_channel(592576217962512394)
    msg2 = f"{channel2.mention}"
    channel3 = client.get_channel(592576272752967681)
    msg3 = f"{channel3.mention}"
    channel4 = client.get_channel(586571234276540449)
    msg4 = f"{channel4.mention}"
    await channel.send(f"__**"+come+"**__さんそうこそ!:tada:\n\
"+msg1+","+msg2+","+msg3+"を読んで、できれば"+msg4+"をお願いします！")


@client.event
async def on_member_remove(member):
    channel = client.get_channel(588224929300742154)
    come = member.name
    await channel.send("__**"+come+"**__さんさようなら・・・:sob:")
    

@client.event
async def on_message(message):
    if "ありがとう" in message.content:
        kouho = ["ありナス!","いえいえ","どういたしまして","気にしないで～"]
        send = (random.choice(kouho))
        await message.channel.send(send)

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
    
    if message.content.startswith("/"):
        chan = message.channel.id
        if chan == 592581835343659030 or chan ==586075792950296576 or chan ==587909823665012759 or chan == 588009676185272321 or\
            chan == 588009727494193154 or chan == 588009770514907138 or chan == 588009806674264075 or chan == 588009850668056579 or\
            chan == 592576272752967681 or chan == 595072269483638785 or chan == 595072339545292804 or chan == 597978849476870153 or\
            chan == 597122356606926870:

            if message.content=="/speca":#送られたメッセージが/specaと一致するなら
                speca = ["反魂蝶「n分咲き」","「無双風神」","紫奥義「弾幕結界」","「風神様の神徳」","「マウンテン・オブ・フェイス」",\
                "「幻想風靡」","滅罪「正直者の死」","禁忌「フォーオブアカインド」","魍魎「二重黒死蝶」","恋符「マスタースパーク」",\
                "氷符「アイシクルフォール」",""]
                reply = (random.choice(speca))
                await message.channel.send(reply)

            if message.content=="/omikuji":
                omikuji = ["大吉！\n今日はいいことがあるでしょう。\nきっとたぶんおそらくひょっとすると",\
                "中吉！\n今日は普段よりちょっといい日になるかもしれませんんね。\nもしかしたら",\
                "中吉！\n今日は普段よりちょっといい日になるかもしれませんんね。\nもしかしたら",\
                "中吉！\n今日は普段よりちょっといい日になるかもしれませんんね。\nもしかしたら",\
                "小吉！\n普段通りの日常です。普通が一番。",\
                "小吉！\n普段通りの日常です。普通が一番。",\
                "小吉！\n普段通りの日常です。普通が一番。",\
                "小吉！\n普段通りの日常です。普通が一番。",\
                "小吉！\n普段通りの日常です。普通が一番。",\
                "凶…\n気をつけて生活しましょう。そうすれば大丈夫ですたぶんきっとメイビー",\
                "凶…\n気をつけて生活しましょう。そうすれば大丈夫ですたぶんきっとメイビー",\
                "凶…\n気をつけて生活しましょう。そうすれば大丈夫ですたぶんきっとメイビー",\
                "大凶…\n物忌みと言って会社や学校を休んでもいいでしょう。ただし何かあっても責任はとりません()"]
                henji = (random.choice(omikuji))
                await message.channel.send(henji)

            if message.content == "/meigen":
                meigen = ["あんた一人で陣なのか","斬れぬものなどあんまりない！","美しく残酷にこの大地から往ね！",\
                "そーなのかー","むきゅー","コインいっこ","2時間前に出直してきな","くろまく～","しゅ～ん",\
                "大・正・解","きゃん","いぬにく～","派手でなければ魔法じゃない。弾幕は火力だぜ。","弾幕はブレイン。常識よ。",\
                "弾幕はパワーだよ","弾幕はパワーだよ","弾幕はパワーだよ","さあ、さでずむ？"]
                henji = (random.choice(meigen))
                await message.channel.send(henji)
    
            if message.content=="/spam":#送られたメッセージが/specaと一致するなら
                tyuusen = ["/spam","/spam","/spam","/spam","/sparn"]
                spam = (random.choice(tyuusen))
                await message.channel.send(spam)

            if message.content=="/femuto":
                femuto = "フェムトわかりやすく言うと須臾\n須臾とは生き物が認識できない僅かな時のことよ\n\
時間とは、認識できない時が無数に積み重なってできています\n時間の最小単位である須臾が認識できないから\n\
時間は連続に見えるけど\n本当は短い時が組み合わさってできているの\n\
組紐も1本の紐のようだけど\n本当は細い紐が組み合わさっているもの\n認識できない細さの繊維で組まれた組紐は\n\
限りなく連続した物質に見えるでしょう\nそのとき紐から余計な物がなくなり最強の強度を誇る\n\
さらには余計な穢れもつかなくなるのです\nこの紐をさらに組み合わせて太い縄にすることで\n決して腐らない縄ができる\n\
その縄は遥か昔から\n不浄な者の出入りを禁じるために使われてきたのよ"
                await message.channel.send(femuto)

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

            if message.content == "/crafter":
                if client.user != message.author:#送り主がbotの場合反応しない
                    role = discord.utils.get(message.guild.roles,id=586123363513008139)
                    if discord.utils.get(message.author.roles,name="クラフタ"):
                        await message.channel.send("もう持ってるじゃん・・・")
                    else:
                        member = message.author
                        await member.add_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"にクラフタ役職を付与しました")

            if message.content == "/shooter":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=586123567146729475)
                    if discord.utils.get(message.author.roles,name="シュータ"):
                        await message.channel.send("もう持ってるじゃん・・・")
                    else:
                        member = message.author
                        await member.add_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"にシュータ役職を付与しました")

            if message.content == "/tuuti":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=606481478078955530)
                    if discord.utils.get(message.author.roles,name="通知ほしい"):
                        await message.channel.send("もう持ってるじゃん・・・")
                    else:
                        member = message.author
                        await member.add_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"に通知ほしい役職を付与しました")

            if message.content == "/sadezumu":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=616547823416246272)
                    if discord.utils.get(message.author.roles,name="さでずむ"):
                        await message.channel.send("もう持ってるじゃん・・・")
                    else:    
                        await member.add_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"にさでずむ役職を付与しました")

            if message.content == "/hide me":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=616790954200006717)
                    if discord.utils.get(message.author.roles,name="かくれんぼなう"):
                        member = message.author.name
                        await message.channel.send(member+"が見つからないから付与できなかったよ・・・")
                    else:    
                        await member.add_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"が隠れました")

            if message.content == "/not crafter":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=586123363513008139)
                    if discord.utils.get(message.author.roles,name="クラフタ"):
                        member = message.author
                        await member.remove_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"からクラフタ役職を剥奪しました")
                    else:
                        await message.channel.send("もう付いてないよ^^")

            if message.content == "/not shooter":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=586123567146729475)
                    if discord.utils.get(message.author.roles,name="シュータ"):
                        member = message.author
                        await member.remove_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"からシュータ役職を剥奪しました")
                    else:
                        await message.channel.send("もう付いてないよ^^")

            if message.content == "/not tuuti":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=606481478078955530)
                    if discord.utils.get(message.author.roles,name="通知ほしい"):
                        member = message.author
                        await member.remove_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"から通知ほしい役職を剥奪しました")
                    else:
                        await message.channel.send("もう付いてないよ^^")

            if message.content == "/not sadezumu":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=616547823416246272)
                    if discord.utils.get(message.author.roles,name="さでずむ"):
                        member = message.author
                        await member.remove_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"からさでずむ役職を剥奪しました")
                    else:
                        await message.channel.send("もう付いてないよ^^")

            if message.content == "/find me":
                if client.user != message.author:#送り主がbotの場合反応しない
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=616790954200006717)
                    if discord.utils.get(message.author.roles,name="かくれんぼなう"):
                        member = message.author
                        await member.remove_roles(role)
                        member = message.author.name
                        await message.channel.send(member+"!みーつけた!")
                    else:
                        await message.channel.send("もう見つかってるよ^^")

            if message.content == "/help":
                helpmsg = "```\
**/crafter**        クラフタ役職を付与\n\
**/not crafter**    クラフタ役職を剥奪\n\
**/shooter**        シュータ役職を付与\n\
**/not shooter**    シュータ役職を剥奪\n\
**/speca**          スペルカードを宣言\n\
**/meigen**           東方の名言と迷言を発言\n\
**/omikuji**        おみくじが引けます\n\
**/spam**           スパム発言を行います\n\
**/fairy**          マナ妖精と同じことをつぶやきます\n\
**/tuuti**        __通知ほしい役職を付与__\n\
**/not tuuti**    __通知ほしい役職を剥奪__\n\
**/sadezumu**       さでずむ役職を付与\n\
**/not sadezumu**   さでずむ役職を剥奪\n\
**/delmsg**         魔理ちゃんに怒られます。そして・・・？\n\
**/help**           この画面を出します\n\
                    ```"
            await message.channel.send(helpmsg)

        else:
            await message.channel.send("ここで実行しないでください！")

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
                        await message.channel.send(win)
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

    if client.user != message.author:
        if message.content=="/tokusyu":#送られたメッセージが/tokusyuと一致するなら
            if discord.utils.get(message.author.roles, name="管理者"):
                if message.channel.id == 597122356606926870:
                    member = message.author
                    role = discord.utils.get(message.guild.roles,id=597123894775775252)
                    await member.add_roles(role)
                    rep = f'{message.author.mention} に役職「特殊操作」を付与しました。気を付けてください'
                    await message.channel.send(rep)
                    dm = await message.author.create_dm()
                    await dm.send(f"{message.author.mention}さんに「特殊操作」役職を付与しました。")

                else:
                    await message.channel.send("ここで実行しないでください!")
            else:
                await message.channel.send("何様のつもり？")
                member = message.author
                role = discord.utils.get(message.guild.roles,id=616212704818102275)
                await member.add_roles(role)
    
    if client.user != message.author:
        if message.content == "/delmsg":
            if discord.utils.get(message.author.roles,name="特殊操作"):
                await message.channel.purge()
            else:
                await message.channel.send("何様のつもり？")
                member = message.author
                role = discord.utils.get(message.guild.roles,id=616212704818102275)
                await member.add_roles(role)

    if client.user != message.author:
        if message.content.startswith("/delmsg"):
            member = message.author
            role = discord.utils.get(message.guild.roles,id=597123894775775252)
            await member.remove_roles(role)

    if client.user in message.mentions:
        await message.channel.send("おいゴラァ")
        await message.channel.send("やめろ")
        await message.channel.send("てめぇ常識持ってんのか？")
        await message.channel.send("誰にメンション飛ばしたと思ってるんだ")


@tasks.loop(seconds=60)#60秒に一回ループ
async def loop():
    weekday = datetime.today().weekday()#現在の曜日
    if weekday == 5:
        now = datetime.now().strftime('%H:%M')#現在の時刻
        if now == '2:19':
            channel = client.get_channel(603832801036468244)
            await channel.purge()
        if now == '2:20':
            channel = client.get_channel(603832801036468244)
            start = ['しりとり','霧雨魔理沙(きりさめまりさ)','多々良小傘(たたらこがさ)','リリカ・プリズムリバー']
            hajime = (random.choice(start))
            await channel.send(hajime)

loop.start()#ループ処理実行

client.run("NTk0MDUyMzQ5MTQwNDAyMTc5.XRW0fA.FpO2ru74maCDsqbBFMeT9K-v1fA")