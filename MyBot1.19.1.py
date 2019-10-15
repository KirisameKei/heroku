import discord
import random
import re
import datetime
import urllib.request
import json
import time
import asyncio
from discord.ext import tasks
from datetime import date
from datetime import datetime#ここまでインポート、このbotを動かすのに必要

client = discord.Client()
now = datetime.now().strftime("%H:%M")#現在の時刻

citycodes = {
"稚内": '011000',"旭川": '012010',"網走": '013010',"根室": '014010',"釧路": '014020',
"室蘭": '015010',"札幌": '016010',"函館": '017010',"青森": '020010',"八戸": '020030',
"盛岡": '030010',"仙台": '040010',"秋田": '050010',"山形": '060010',"新庄": '060040',
"福島": '070010',"若松": '070030',"水戸": '080010',"宇都宮": '090010',"前橋": '100010',
"みなかみ": '100020',"さいたま": '110010',"熊谷": '110020',"千葉": '120010',"銚子": '120020',
"館山": '120030',"東京": '130010',"横浜": '140010',"新潟": '150010',"長岡": '150020',
"富山": '160010',"金沢": '170010',"福井": '180010',"敦賀": '180020',"甲府": '190010',
"長野": '200010',"松本": '200020',"岐阜": '210010',"高山": '210020',"静岡": '220010',
"浜松": '220040',"名古屋": '230010',"豊橋": '230020',"津": '240010',"大津": '250010',
"京都": '260010',"舞鶴": '260020',"大阪": '270000',"神戸": '280010',"奈良": '290010',
"和歌山": '300010',"潮岬": '300020',"鳥取": '310010',"米子": '310020',"松江": '320010',
"岡山": '330010',"広島": '340010',"下関": '350010',"山口": '350020',"萩": '350040',
"徳島": '360010',"高松": '370000',"松山": '380010',"宇和島": '380030',"高知": '390010',
"室戸岬": '390020',"福岡": '400010',"久留米": '400040',"佐賀": '410010',"長崎": '420010',
"熊本": '430010',"人吉": '430040',"大分": '440010',"佐伯": '440040',"宮崎": '450010',
"延岡": '450020',"都城": '450030',"鹿児島": '460010',"種子島": '460030',"那覇": '471010',
"南大東": '472000',"宮古島": '473000',"石垣島": '474010',"与那国島": '474020'}


@client.event
async def on_ready():#このbotがログインしたら
    print(client.user.name+"がログインしました")#ターミナルにログインしたことを表示
    channel = client.get_channel(595072269483638785)#チャンネルの指定
    await channel.send(client.user.name+"がログインしました")#指定チャンネルにログインしたことを表示

    await client.change_presence(activity = discord.Game(name = "年中不眠不休"))


@client.event
async def on_member_join(member):#新規の人が来たら反応
    come = member.name
    comeid = member.id
    channel = client.get_channel(588224929300742154)#メッセージを送るチャンネルを指定
    channel1 = client.get_channel(586000955053441039)#誘導先のチャンネルを指定
    msg1 = f"{channel1.mention}"#チャンネルにメンション以下同じ
    channel2 = client.get_channel(592576217962512394)
    msg2 = f"{channel2.mention}"
    channel3 = client.get_channel(592576272752967681)
    msg3 = f"{channel3.mention}"
    channel4 = client.get_channel(586571234276540449)
    msg4 = f"{channel4.mention}"
    channel5 = client.get_channel(626063435498520606)
    msg5 = f"{channel5.mention}"
    channel6 = client.get_channel(592581835343659030)
    msg6 = f"{channel6.mention}"
    if member.guild.id == 58598962050203672:#もしけいの実験サーバなら
        if comeid == 607459082873602059:#もしネクストなら
            role = discord.utils.get(member.guild.roles, name = "発言禁止")
            await member.add_roles(role)
            await channel.send("botのおもちゃが参加しました")
            for i in range(50):
                if i <= 50:
                    fuck = "<@!607459082873602059>"
                    bougen = "引っかかったな、バーカがーーーwww!ざまぁみやがれwww"
                    channel = client.get_channel(595072269483638785)
                    await channel.send(fuck+bougen)
        else:
            await channel.send(f"{member.mention}\n__**"+come+"**__さんそうこそ!:tada:\n\
まず"+msg5+"をお願いします！\n\
次に"+msg1+","+msg2+","+msg3+"を読んで同意していただけるなら、"+msg6+"に**/accept**と打ち込んでください！")#歓迎メッセージ
            role = discord.utils.get(member.guild.roles,id=621641465105481738)#新規役職を指定
            await member.add_roles(role)#役職を付与
    
    if member.guild.id == 587909823665012757:#無法地帯なら
        await channel.send(come+"さんが無法地帯に参加しました")

    if member.guild.id == 624551872933527553:
        await channel.send(come+"しょに入った")


@client.event
async def on_member_remove(member):#ユーザーがサーバを抜けたら反応
    muhouid = member.guild.id
    channel = client.get_channel(588224929300742154)#メッセージを送るチャンネルを指定
    left = member.name
    if member.guild.id == 58598962050203672:
        await channel.send("__**"+left+"**__さんさようなら・・・:sob:")#お悔やみを伝える
    if member.guild.id == 587909823665012757:
        await channel.send(left+"さんが無法地帯のカオスさに耐えられなくなりました")
    if member.guild.id == 624551872933527553:
        await channel.send(left+"しょから抜けた")


@client.event
async def on_message(message):#メッセージを受け取る

    #宣伝禁止
    okgu = message.guild.id
    okca = message.channel.category_id
    okch = message.channel.id
    if okch != 586002750823858186 and okca != 595072154068975625 and okca != 592579516858236928 and\
        okca != 598864281626476544 and okgu != 587909823665012757 and okgu != 624551872933527553 and \
        okgu != 633328124968435712:
        if "https://discord.gg/" in message.content or "http://discord.gg/" in message.content:
            mention = f"{message.author.mention}"
            await message.channel.purge(limit = 1)
            await message.channel.send(mention+"\n指定チャンネル以外での宣伝は禁止です。メッセージを削除しました。")
    
    m = message.channel.send
    if client.user != message.author:#送り主が自分の場合反応しない

        #処罰部
        if message.channel.id == 624551872933527555:#一般
            channel = client.get_channel(633331445955297286)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624565990314737664:#ほんみょうよそくするとこ
            channel = client.get_channel(633331576071127080)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624815373841203231:#ぶらっくりすと
            channel = client.get_channel(633331855151595521)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624906595385606154:#予備軍リスト
            channel = client.get_channel(633331904434798593)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 626692760870715392:#証拠まとめ
            channel = client.get_channel(633331938970828810)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 627352301757136899:#☆gt☆
            channel = client.get_channel(633332039419953175)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 632067738524844043:#申請
            channel = client.get_channel(633332131183198222)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 632568100620861460:#ディスコのログでやべーやつ探し
            channel = client.get_channel(633332202125393931)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 632568697432571915:#鯖参加投票
            channel = client.get_channel(633332394535157770)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624869474214084609:#かめさま
            channel = client.get_channel(633332603054718997)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624869667818962945:#ねこさま
            channel = client.get_channel(633332636001107970)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624905875223740417:#いぶき
            channel = client.get_channel(633332681626746895)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 625667260169584640:#gogotrain
            channel = client.get_channel(633332943527608332)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 626002696603697182:#ぱむぱむ
            channel = client.get_channel(633333001681502219)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 628175026721390612:#ネクスト
            channel = client.get_channel(633333399146332160)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 630196403666288660:#ソビエトの巫女
            channel = client.get_channel(633333684665319469)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 631792683538710549:#ryuuku07
            channel = client.get_channel(633333757725769778)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 630005567598886912:#sonicucu
            channel = client.get_channel(633333978572783637)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624821367505944586:#くーるー
            channel = client.get_channel(633334175201624094)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624873931693621248:#みっちー
            channel = client.get_channel(633334276884267056)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 626820388910792714:#s1複数
            channel = client.get_channel(633334496510476329)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624867397970690058:#くーるーマンション
            channel = client.get_channel(633334647907942401)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 624859173573885952:#のりはま
            channel = client.get_channel(633334694997655552)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 632488443494137856:#雑談VC
            channel = client.get_channel(633334893568458752)
            await channel.send(message.author.name+">>>"+message.content)
        if message.channel.id == 632488488960262144:#作戦VC
            channel = client.get_channel(633334926472642590)
            await channel.send(message.author.name+">>>"+message.content)

    
        if "ありがとう" in message.content:#メッセージの中に「ありがとう」が入っていたら
            kouho = ["ありナス!","いえいえ","どういたしまして","気にしないで～"]#送るメッセージの候補
            send = (random.choice(kouho))#kouhoの中からランダムで選ぶ
            await m(send)#メッセージを送信

        if "おはよう" in message.content:#メッセージの中に「おはよう」が入っていて
            if now >= "05:00" and now <= "11:00":#指定時間内なら
                msg = "おはようございます__" + message.author.name + "__さん！"#送るメッセージ
                await m(msg)#メッセージを送信
            else:#時間外だったら
                await m("今おはよう!?")#怒る。以下同じ

        if "こんにちは" in message.content:
            if now >= "09:00" and now <= "18:00":
                msg = "こんにちは__" + message.author.name + "__さん！"
                await m(msg)
            else:
                await m("今こんにちは!?")

        if "こんばんは" in message.content:
            if now >= "00:00" and now <= "06:00" or now >= "17:00" and now <= "23:59":
                msg = "こんばんは__" + message.author.name + "__さん！"
                await m(msg)
            else:
                await m("今こんばんは!?")

        if message.channel.id == 626063435498520606:
            if discord.utils.get(message.author.roles, name = "新規"):
                p = re.compile( r'^[a-zA-Z0-9_ ]+$' )
                if p.fullmatch( message.content ):
                    role = discord.utils.get(message.guild.roles,name = "accept送信可能")
                    channel = client.get_channel(592581835343659030)
                    msg = f"{channel.mention}"
                    await message.author.add_roles(role)
                    await m("MCIDの報告ありがとうございます。ルールに同意いただけるなら"+msg+"で**/accept**をお願い致します。")
                else :
                    await m("MCIDに使用できない文字が含まれています。もう一度ご確認ください。")
            else:
                p = re.compile( r'^[a-zA-Z0-9_→ ]+$' )
                if p.fullmatch( message.content ):
                    if "→" in message.content:
                        await m("MCID変更の報告ありがとうございます")
                    else:
                        await m("MCID変更報告は旧MCID→新MCIDの形でお願いします。")
                else:
                    await m("MCIDに使用できない文字が含まれています。もう一度ご確認ください。")

                
        if message.content.startswith("/"):
            chan = message.channel.id
            if chan == 592581835343659030 or chan ==586075792950296576 or chan ==587909823665012759 or chan == 588009676185272321 or\
            chan == 588009727494193154 or chan == 588009770514907138 or chan == 588009806674264075 or chan == 588009850668056579 or\
            chan == 592576272752967681 or chan == 595072269483638785 or chan == 595072339545292804 or chan == 597978849476870153 or\
            chan == 597122356606926870 or chan == 586420890678591509:

                #以下返答系コマンド
                if message.content=="/speca":#送られたメッセージが/specaと一致するなら
                    speca = ["反魂蝶「n分咲き」","「無双風神」","紫奥義「弾幕結界」","「風神様の神徳」","「マウンテン・オブ・フェイス」",\
                "「幻想風靡」","滅罪「正直者の死」","禁忌「フォーオブアカインド」","魍魎「二重黒死蝶」","恋符「マスタースパーク」",\
                "氷符「アイシクルフォール」",""]
                    reply = (random.choice(speca))
                    await m(reply)

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
                    await m(henji)

                if message.content == "/meigen":
                    meigen = ["あんた一人で陣なのか","斬れぬものなどあんまりない！","美しく残酷にこの大地から往ね！",\
                    "そーなのかー","むきゅー","コインいっこ","2時間前に出直してきな","くろまく～","しゅ～ん",\
                    "大・正・解","きゃん","いぬにく～","派手でなければ魔法じゃない。弾幕は火力だぜ。","弾幕はブレイン。常識よ。",\
                    "弾幕はパワーだよ","弾幕はパワーだよ","弾幕はパワーだよ","さあ、さでずむ？","大丈夫、生きている間は一緒にいますから",\
                    "動くと撃つ！間違えた。撃つと動くだ。今すぐ動く","２時間前に出直してきな","夢のような現実だわ！"]
                    henji = (random.choice(meigen))
                    await m(henji)

                if message.content == "/fairy":
                    mana = ["やあ!","うわーん!お腹空いたよー!","(';ω;`)ｳｩｩ ﾋﾓｼﾞｲ…","がちゃりんごがっ!食べたいっ!","@うんちゃま",\
                "お腹空いたなぁー。","あぁ!幸せ!","いつもりんごをありがとう!","のりんごはおいしいなあ","には帰るよー。","がちゃりんごっておいしいよね!",\
                "('～`)ﾓｸﾞﾓｸﾞ…","はどのりんごが好き？ぼくはがちゃりんご!","動いてお腹を空かしていっぱい食べるぞー!","たくさん働いて、たくさんりんごを食べようね!",\
                "ちょっと食べ疲れちゃった","整地しないのー？","あ、もうこんな時間だ!","じゃーねー!"]
                    send = (random.choice(mana))
                    sousinsya = message.author.name
                    if send == "@うんちゃま":
                        await m(send+"　"+sousinsya+"が意地悪するんだっ!")
                    elif send == "やあ!":
                        await m(send+sousinsya)
                    elif send == "のりんごはおいしいなあ":
                        await m(sousinsya+send)
                    elif send == "はどのりんごが好き？ぼくはがちゃりんご!":
                        await m(sousinsya+send)
                    elif send == "じゃーねー!":
                        await m(send+sousinsya)
                    elif send =="には帰るよー。":
                        await m("僕は"+now+send)
                    else:
                        await m(send)

                member = message.author.name
                have = "もう持ってんじゃん・・・"
                nothave = "もう付いてないよ^^"

                #アカウント名作成
                if message.content.startswith("/name"):
                    msg = f'{message.content}'.replace("/name ","")
                    p = re.compile( r'^[0-9]+$' )
                    if p.fullmatch(msg):
                        kazu = int(msg)
                        if kazu <= 10:
                            for i in range(kazu):
                                if i <= kazu:
                                    kouho = ["あ","い","う","え","お","か","き","く","け","こ","さ","し","す","せ","そ",\
                            "た","ち","つ","て","と","な","に","ぬ","ね","の","は","ひ","ふ","へ","ほ",\
                            "ま","み","む","め","も","や","ゆ","よ","ら","り","る","れ","ろ","わ","ゐ","ゑ","を","ん",\
                            "が","ぎ","ぐ","げ","ご","ざ","じ","ず","ぜ","ぞ","だ","ぢ","づ","で","ど",\
                            "ば","び","ぶ","べ","ぼ","ぱ","ぴ","ぷ","ぺ","ぽ"]
                                    choice = (random.choice(kouho))
                                    await m(choice)
                        else:
                            await m("名前の長さは10文字以下にしてください！")

                #タイマー機能
                if message.content.startswith("/stimer "):
                    swait = f"{message.content}".replace("/stimer ","")#数字＋メッセージ   3 aiueo
                    p = re.compile(r'^[-0-9]')
                    if p.match(swait):
                        kesu = swait.split()[0]#str     "3 "
                        jikan = kesu.replace(" ","")#str,数字のみ
                        kazu = int(jikan)
                        if kazu >= 1:
                            await m(jikan+"秒後にメッセージを送信")
                            msg = swait.replace(kesu,"")
                            await asyncio.sleep(kazu)
                            mention = message.author.mention
                            await m(mention+"\n"+msg)
                        else:
                            fixed = jikan.replace("-","")
                            await m(fixed+"秒前に出直してきな" )      
                    else:
                        await m("時間は数値で指定してください")

                if message.content.startswith("/mtimer "):
                    mwait = f"{message.content}".replace("/mtimer ","")#数字＋メッセージ   3 aiueo
                    p = re.compile(r'^[-0-9]')
                    if p.match(mwait):
                        kesu = mwait.split()[0]#str
                        jikan = kesu.replace(" ","")#str,数字のみ
                        kazu = int(jikan)
                        if kazu >= 1:
                            await m(jikan+"分後にメッセージを送信")
                            msg = mwait.replace(kesu,"")
                            await asyncio.sleep(kazu*60)
                            mention = message.author.mention
                            await m(mention+"\n"+msg)
                        else:
                            fixed = jikan.replace("-","")
                            await m(fixed+"分前に出直してきな" )      
                    else:
                        await m("時間は数値で指定してください")

                if message.content.startswith("/htimer "):
                    hwait = f"{message.content}".replace("/htimer ","")#数字＋メッセージ   3 aiueo
                    p = re.compile(r'^[-0-9]')
                    if p.match(hwait):
                        kesu = hwait.split()[0]#str
                        jikan = kesu.replace(" ","")#str,数字のみ
                        kazu = int(jikan)
                        if kazu >= 1:
                            await m(jikan+"時間後にメッセージを送信")
                            msg = hwait.replace(kesu,"")
                            await asyncio.sleep(kazu*3600)
                            mention = message.author.mention
                            await m(mention+"\n"+msg)
                        else:
                            fixed = jikan.replace("-","")
                            await m(fixed+"時間前に出直してきな" )      
                    else:
                        await m("時間は数値で指定してください")

                #ロールカウント
                if message.content.startswith("/role_count"):
                    msg = f'{message.content}'.replace("/role_count ","")
                    p = re.compile(r'[0-9]+$')
                    if p.fullmatch(msg):
                        kazu = int(msg)
                        if kazu != 585998962050203672:
                            role = discord.utils.get(message.guild.roles,id = kazu)
                            role_count = int( len( role.members ) )
                            ninzuu = f"{role_count}"
                            await m("__"+role.name+"__は"+ninzuu+"人います")
                        else:
                            await m("なぜかeveryoneメンションが飛ぶので実行できません")

                #天気予報
                reg_res = re.compile(u"/weather (.+)").search(message.content)
                if reg_res:

                    if reg_res.group(1) in citycodes.keys():

                        citycode = citycodes[reg_res.group(1)]
                        resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
                        resp = json.loads(resp.decode('utf-8'))

                        msg = resp['publicTime']
                        msg += "に発表\n"
                        msg += resp['location']['city']
                        msg += "の天気は、\n"
                        for f in resp['forecasts']:
                            msg += f['dateLabel'] + "が" + f['telop']+"\n"
                        msg += "です。"
                        await message.channel.send(message.author.mention+"\n"+msg)

                    else:
                        await message.channel.send("そこの天気はわかりません...")

                #新規対処
                if message.content == "/accept":
                    if discord.utils.get(message.author.roles,name="新規"):
                        if discord.utils.get(message.author.roles,name="accept送信可能"):
                            role1 = discord.utils.get(message.guild.roles,name = "新規")
                            role2 = discord.utils.get(message.guild.roles,name = "accept送信可能")
                            await message.author.remove_roles(role1)
                            await message.author.remove_roles(role2)
                            role = discord.utils.get(message.guild.roles,name = "クラフタ")
                            await message.author.add_roles(role)
                            await m(member+"から__新規__を剥奪し__クラフタ__を付与しました")
                            channel2 = client.get_channel(592576217962512394)
                            msg2 = f"{channel2.mention}"
                            channel3 = client.get_channel(592576272752967681)
                            msg3 = f"{channel3.mention}"
                            channel4 = client.get_channel(586571234276540449)
                            msg4 = f"{channel4.mention}"
                            new = message.author
                            await m(f"{new.mention}さん参加ありがとうございます!\n\
このチャンネルで"+msg2+"や"+msg3+"を参考に自分に必要な役職をつけてください\n\
もしよろしければ"+msg4+"もお願いします。")
                        else:
                            channel5 = client.get_channel(626063435498520606)
                            msg5 = f"{channel5.mention}"
                            await m("まず"+msg5+"をお願いします")
                    else:
                        await m(nothave)

                #以下役職付与系
                if message.content == "/crafter":
                    if discord.utils.get(message.author.roles,name="クラフタ"):
                        await m(have)
                    else:
                        role = discord.utils.get(message.guild.roles,name = "クラフタ")
                        await message.author.add_roles(role)
                        await m(member+"に__クラフタ__を付与しました")

                if message.content == "/shooter":
                    if discord.utils.get(message.author.roles,name="シュータ"):
                        await m(have)
                    else:
                        role = discord.utils.get(message.guild.roles,name = "シュータ")
                        await message.author.add_roles(role)
                        await m(member+"に__シュータ__を付与しました")

                if message.content == "/tuuti":
                    if discord.utils.get(message.author.roles,name="通知ほしい"):
                        await m(have)
                    else:
                        role = discord.utils.get(message.guild.roles,name = "通知ほしい")
                        await message.author.add_roles(role)
                        await m(member+"に__通知ほしい__を付与しました")

                if message.content == "/sadezumu":
                    if discord.utils.get(message.author.roles,name="さでずむ"):
                        await m(have)
                    else:
                        role = discord.utils.get(message.guild.roles,name = "さでずむ")
                        await message.author.add_roles(role)
                        await m(member+"に__さでずむ__を付与しました")

                if message.content.startswith("/hide"):
                    if message.content == "/hide me":
                        if discord.utils.get(message.author.roles,name="かくれんぼなう"):
                            await m(member+"が見つかりませんでした")
                        else:
                            role = discord.utils.get(message.guild.roles,name = "かくれんぼなう")
                            await message.author.add_roles(role)
                            await m(member+"が隠れました。もーいーよ")
                    else:
                        msg = f'{message.content}'.replace("/hide ","")
                        p = re.compile( r'^[0-9]+$' )
                        if p.fullmatch(msg):
                            kazu = int(msg)
                            hide = message.guild.get_member(kazu)
                            if discord.utils.get(hide.roles,name="かくれんぼなう"):
                                await m(hide.name+"はもう隠れているようです。私には見つけられませんでした")
                            else:
                                if discord.utils.get(hide.roles,name="管理者"):
                                    await m("管理者を隠そうとはさてはこの鯖を乗っ取る気だなオメー")
                                else:
                                    role = discord.utils.get(message.guild.roles,name = "かくれんぼなう")
                                    await hide.add_roles(role)
                                    await m(hide.name+"が隠れました。もーいーよ")
                        else:
                            await m("IDに使えない文字が入っています。もう一度ご確認ください。")


                if message.content == "/testmember":
                    if discord.utils.get(message.author.roles,name="実験台"):
                        await m(have)
                    else:
                        role = discord.utils.get(message.guild.roles,name = "実験台")
                        await message.author.add_roles(role)
                        await m(member+"に__実験台__を付与しました")

                #以下役職剥奪系
                if message.content == "/not crafter":
                    if discord.utils.get(message.author.roles,name="クラフタ"):
                        role = discord.utils.get(message.guild.roles,name = "クラフタ")
                        await message.author.remove_roles(role)
                        await m(member+"から__クラフタ__を剥奪しました")
                    else:
                        await m(nothave)

                if message.content == "/not shooter":
                    if discord.utils.get(message.author.roles,name="シュータ"):
                        role = discord.utils.get(message.guild.roles,name = "シュータ")
                        await message.author.remove_roles(role)
                        await m(member+"から__シュータ__を剥奪しました")
                    else:
                        await m(nothave)

                if message.content == "/not tuuti":
                    if discord.utils.get(message.author.roles,name="通知ほしい"):
                        role = discord.utils.get(message.guild.roles,name = "通知ほしい")
                        await message.author.remove_roles(role)
                        await m(member+"から__通知ほしい__を剥奪しました")
                    else:
                        await m(nothave)

                if message.content == "/not sadezumu":
                    if discord.utils.get(message.author.roles,name="さでずむ"):
                        role = discord.utils.get(message.guild.roles,name = "さでずむ")
                        await message.author.remove_roles(role)
                        await m(member+"から__さでずむ__を剥奪しました")
                    else:
                        await m(nothave)

                if message.content.startswith("/find"):
                    if message.content == "/find me":
                        if discord.utils.get(message.author.roles,name="かくれんぼなう"):
                            role = discord.utils.get(message.guild.roles,name = "かくれんぼなう")
                            await message.author.remove_roles(role)
                            await m(member+"！みーつけた！")
                        else:
                            await m("もう見つけてるよ・・・")
                    else:
                        msg = f'{message.content}'.replace("/find ","")
                        p = re.compile( r'^[0-9]+$' )
                        if p.fullmatch(msg):
                            kazu = int(msg)
                            find = message.guild.get_member(kazu)
                            if discord.utils.get(find.roles,name = "かくれんぼなう"):
                                role = discord.utils.get(message.guild.roles,name = "かくれんぼなう")
                                await find.remove_roles(role)
                                await m(find.name+"を見つけたよ！")
                            else:
                                await m("もう見つけてるよ・・・")
                        else:
                            await m("IDに使えない文字が入っています。もう一度ご確認ください。")

                if message.content == "/not testmember":
                    if discord.utils.get(message.author.roles,name="実験台"):
                        role = discord.utils.get(message.guild.roles,name = "実験台")
                        await message.author.remove_roles(role)
                        await m(member+"から__実験台__を剥奪しました")

                #オススメ絵師紹介
                if message.content == "/osusume eshi":
                    esi = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r"]
                    choice = (random.choice(esi))
                    if choice == "a":
                        await m("https://twitter.com/franruhika \nルヒカさん\n万人受けする絵柄(だと思う)。はずれがない(と思う)。")
                    if choice == "b":
                        await m("https://twitter.com/Haruki50501 \n春樹さん\nきれいな絵を描く。時々微エロ注意。")
                    if choice == "c":
                        await m ("https://twitter.com/tauminust \nminusTさん\n凄い。とにかく凄い。見ればわかる。凄い。時々微エロ注意だが上品なエロなのでご安心を(？)")
                    if choice == "d":
                        await m("https://twitter.com/magus_night_ \nHajinさん\n線画、塗り共にきれい。よくminusTさんと組んでいる。")
                    if choice == "e":
                        await m("https://twitter.com/saltty__ \nsaltさん\n小傘ちゃん愛が凄い人。小傘ちゃん好きなら一度見ておくべき。小傘ちゃんbotのアイコンの作者でもある")
                    if choice == "f":
                        await m("https://twitter.com/arinutan \nアリヌさん\n穣子ちゃんだけでとんでもなく有名になった。サブアカはドエロ注意")
                    if choice == "g":
                        await m("https://twitter.com/LEXUS_6737 \n虚無僧さん\n面白い漫画を描く人。~~ここ数か月更新が途絶えているので心配である。~~先日投稿がありました。生きています。")
                    if choice == "h":
                        await m("https://twitter.com/itatatata6 \nいたたたたさん\nネタ絵師。ときどきえっちいのがくるので注意。")
                    if choice == "i":
                        await m("https://twitter.com/korokoroudon \nののこさん\nすごくきれいな線画を描く人。更新は遅いものの見る価値あり。")
                    if choice == "j":
                        await m("https://twitter.com/siina_motiduki \n望月しいなさん\nすごくきれいな絵を描く人。ラフと完成絵の違いが判らないほど(ほめてます)")
                    if choice == "k":
                        await m("https://twitter.com/ayn398 \nあやのさん\n一枚漫画を描く。そこそこうまいし面白い。最近更新が途絶えているがプロフに育児中と書いてあるので多分それが原因だろう。先ほど投稿を確認しました。生きています。")
                    if choice == "l":
                        await m("https://twitter.com/LOSER_na \n楠なのはさん\nきれいな絵を描く。百合注意。サブアカはもっと注意。")
                    if choice == "m":
                        await m("https://twitter.com/Muccuman \nむっく氏\n私は結構好き。最近エロが増えてきた気がするので注意。")
                    if choice == "n":
                        await m("https://twitter.com/norawanko102 \nのらわんこさん\nたくさんの絵柄を持っている。時々絵の描き方講座？的な絵もあげてくれる")
                    if choice == "o":
                        await m("https://twitter.com/nekurodayo \n根黒さん\nかっこいい絵を描く。私は好き。")
                    if choice == "p":
                        await m("https://twitter.com/papiermesser \nふみ切さん\n短編漫画家。とにかくストーリーがいい。たった一ページの漫画でうるっとくるものまである。すばらしい作品を量産する。過去に7年間連続で毎日投稿をしていたらしい。すごい。")
                    if choice == "q":
                        await m("https://twitter.com/satentosakana \n冬野インコさん\n今伸びが著しい人。凄くきれいな絵を描く。透明感凄い。")
                    if choice == "r":
                        await m("https://twitter.com/junyamaekaki \nヤマジュンさん\n今すごい伸びてる人。アナログデジタル共にうまい。色鉛筆のプロ。あくまで予感だがいずれエロに転向しそう。")
                    await m("アカウント名、URLはbot作成時のものです。現在変わっている可能性があります。")

                #オススメユーチューバー紹介
                if message.content == "/osusume youtuber":
                    youtuber = ["a","b","c"]
                    choice = (random.choice(youtuber))#minusT
                    if choice == "a":
                        await m("https://www.youtube.com/user/marasy8 \nまらしぃ\n凄いピアニスト")
                    if choice == "b":
                        await m("https://www.youtube.com/channel/UCp6b7eo3AOEOSaz3laqWp2A \nえびちゃんねる\n解説動画、ネタ動画の割合がちょうどよい。解説動画はとことん分かりやすくネタ動画も面白い。マイクラの仕様にもそこそこ詳しく特に赤石とリソパを得意とする。便利系リソパやネタリソパの配布もしている。")
                    if choice == "c":
                        await m("https://www.youtube.com/channel/UCEc2gctIynWHMDq2tuCBPJw \nminusT\nえ？絵師のほうで出てきただろって？見ればわかる。動画も凄い。blender使い(よく間違われるがMMDではないので注意)")
                    if choice == "d":
                        await m("https://www.youtube.com/channel/UCuG5ehhxJKWgMEN64eVL70A \nうちゃ\n凄いシューター。東方全作品LNNFSしている。避け方の参考になるかもしれないので東方プレイヤーは見てみるといいかもしれない。")
                    await m("アカウント名、URLはbot作成時のものです。現在変わっている可能性があります。")


                #ヘルプコマンド
                if message.content == "/help":
                    await m("\
コマンド系\n\
```\n\
/crafter            クラフタ役職を付与\n\
/not crafter        クラフタ役職を剥奪\n\
/shooter            シュータ役職を付与\n\
/not shooter        シュータ役職を剥奪\n\
/tuuti              通知ほしい役職を付与\n\
/not tuuti          通知ほしい役職を剥奪\n\
/sadezumu           さでずむ役職を付与\n\
/not sadezumu       さでずむ役職を剥奪\n\
/hide me            (背景テーマをダークにしてる人からは)名前が見えなくなります\n\
/hide 他人のID      他人をかくれんぼに強制的に参加させられます。管理者やbotに対しては無効です。\n\
/find me            元に戻ります\n\
/find 他人のID      かくれんぼ中の人を見つけます。\n\
/supeca             けいが独断と偏見で選んだ名スペカを宣言します\n\
/meigen             けいが(ry名言と迷言を発言します\n\
/fairy              マナ妖精のつぶやきを発言します\n\
/osusume eshi       お勧めの絵師を紹介します。紹介文はすべて主観です\n\
/osusume youtuber   お勧めのYoutuberを紹介します。紹介文は(ry(四人分だけ実装しました。まだ追加すると思います)\n\
/stimer 秒数 内容    指定秒後にメンション付きで内容を表示\n\
/mtimer 分数 内容    指定分後にメンション付きで(ry\n\
/htimer 時間数 内容  指定時間後にメン(ry\n\
タイマー機能を使ったことによるいかなる被害もけいは責任を取りません\n\
    (要はこの機能に任せっきりで自分の用事を忘れるなよってこと。再起動したらリセットされちゃうだろうしね)\n\
/help               これを出します```\n\
その他の機能\n\
```\n\
・「おはよう」、「こんにちは」、「こんばんは」の入った文字列を送ると返事をします。時間によって反応が変わります。(また調子が悪くなっています(原因究明中))\n\
・一週間に一度しりとりチャンネルをリセットして最初のワードを言います。\n\
・しりとりを「ん」や「ン」で終わらせると続けてくれます。\n\
・隠し要素がいくつかあります。最初に発見すれば役職がもらえます。いつかは特典を用意したいがまだ決まってない。\n\
・管理者以外が/tokusyu、/delmsgを実行すると魔理ちゃんに怒られます。そして・・・？```\n\
")
            else:
                await m("ここで実行しないでください！")

        #以下メッセージ削除関連
        #特殊操作役職の付与
        if message.content=="/tokusyu":#送られたメッセージが/tokusyuと一致するなら
            if discord.utils.get(message.author.roles, name="管理者"):
                if message.channel.id == 597122356606926870:
                    role = discord.utils.get(message.guild.roles,id=597123894775775252)
                    await message.author.add_roles(role)
                    dm = await message.author.create_dm()
                    await dm.send(f"{message.author.mention}さんに「特殊操作」役職を付与しました。")
                else:
                    await m("ここで実行しないでください!")
            else:
                await m("何様のつもり？")
                role = discord.utils.get(message.guild.roles,id=616212704818102275)
                await message.author.add_roles(role)

        #全消去
        if message.content.startswith("/delmsg"):
            if message.content == "/delmsg":
                if discord.utils.get(message.author.roles,name="特殊操作"):
                    await message.channel.purge()
                else:
                    await m("何様のつもり？")
                    role = discord.utils.get(message.guild.roles,id=616212704818102275)
                    await message.author.add_roles(role)
            else:      
                if discord.utils.get( message.author.roles, name="特殊操作" ):
                    msg = f'{message.content}'.replace("/delmsg ","")
                    p = re.compile( r'^[0-9]+$' )
                    if p.fullmatch(msg):
                        kazu = int(msg)
                        await message.channel.purge(limit=kazu+1)
                else:
                    await m("何様のつもり？")
                    role = discord.utils.get(message.guild.roles,id=616212704818102275)
                    await message.author.add_roles(role)

        if message.content.startswith("/delmsg"):
            role = discord.utils.get(message.guild.roles,name = "特殊操作")
            await message.author.remove_roles(role)

        #アンチbot機能
        fuck = message.author.id
        if fuck == 159985870458322944 or fuck == 365975655608745985:
            bougen = [":middle_finger:","少し静かにしていただけますか？","ちょっと黙っててもらっていいですか？","お引き取りください","f*ck",\
                "たいそうにぎやかなご様子でいらっしゃいますところまことに恐縮でございますが、ご逝去あそばしていただければ幸甚に存じます"]#送るメッセージの候補
            boo = (random.choice(bougen))#bougenの中からランダムに一つ選ぶ
            mention = f"{message.author.mention}"
            await m(mention+boo)#発言したチャンネルに発言

        if message.channel.id == 603832801036468244:
            if message.content.endswith ("ん"):
                channel = client.get_channel(603832801036468244)
                end = ["ンジャメナ","ンゴロンゴロ","ンカイ","ンガミ湖","ンズワニ島","ンゼレコレ","ンスタ","ンスカ","ンジャジジャ島"]
                send = (random.choice(end))
                await m(send)
            if message.content.endswith ("ン"):
                channel = client.get_channel(603832801036468244)
                end = ["ンジャメナ","ンゴロンゴロ","ンカイ","ンガミ湖","ンズワニ島","ンゼレコレ","ンスタ","ンスカ","ンジャジジャ島"]
                send = (random.choice(end))
                await m(send)

        if message.content == "魔理ちゃんのことが大好きです":
            if message.author.name == "けい":
                await m("私も好きだぜ///:heart:")
            else:
                await m("ごめんな、私はけいさんのほうが好きなんだぜ・・・")
        
        #以下隠し要素
        if "フェムト" in message.content:
            femuto = "フェムトわかりやすく言うと須臾\n須臾とは生き物が認識できない僅かな時のことよ\n\
時間とは、認識できない時が無数に積み重なってできています\n時間の最小単位である須臾が認識できないから\n\
時間は連続に見えるけど\n本当は短い時が組み合わさってできているの\n\
組紐も1本の紐のようだけど\n本当は細い紐が組み合わさっているもの\n認識できない細さの繊維で組まれた組紐は\n\
限りなく連続した物質に見えるでしょう\nそのとき紐から余計な物がなくなり最強の強度を誇る\n\
さらには余計な穢れもつかなくなるのです\nこの紐をさらに組み合わせて太い縄にすることで\n決して腐らない縄ができる\n\
その縄は遥か昔から\n不浄な者の出入りを禁じるために使われてきたのよ"
            await m(femuto)
        
        if client.user in message.mentions:
            await message.channel.send("おいゴラァ")
            await message.channel.send("やめろ")
            await message.channel.send("てめぇ常識持ってんのか？")
            await message.channel.send("誰にメンション飛ばしたと思ってるんだ")

        if message.channel.id == 597122356606926870:
            if message.content == "/fuck":
                for i in range(100):
                    if i <= 100:
                        fuck = "<@!607459082873602059>"
                        bougen = ["FUCK","Fuck off","mother fucker",":middle_finger:"]
                        msg = (random.choice(bougen))
                        channel = client.get_channel(595072269483638785)
                        await channel.send(fuck+msg)

            if message.content == "/dmtotu":
                fuckuser = client.get_user(607459082873602059)
                for i in range(100):
                    if i <= 100:
                        dm = await fuckuser.create_dm()
                        hansei = ["何でこんな目に遭っているのかよく考えてください","荒らされる側の気持ちも考えてください","あなたは結局何がしたかったんですか？",\
            "少し頭を冷やされては？",":middle_finger:"]
                        msg = (random.choice(hansei))
                        await dm.send(f"{fuckuser.mention}\n"+msg)

            if message.content == "/dmtest":
                fuckuser = client.get_user(582377618309906491)
                for i in range(100):
                    if i <= 100:
                        dm = await fuckuser.create_dm()
                        hansei = ["何でこんな目に遭っているのかよく考えてください","荒らされる側の気持ちも考えてください","あなたは結局何がしたかったんですか？",\
            "少し頭を冷やされては？",":middle_finger:"]
                        msg = (random.choice(hansei))
                        await dm.send(f"{fuckuser.mention}\n"+msg)


@tasks.loop(seconds = 60)#60秒に一回ループ
async def loop():
    weekday = datetime.today().weekday()#現在の曜日
    if weekday == 6:
        now = datetime.now().strftime("%H:%M")#現在の時刻
        channel = client.get_channel(603832801036468244)
        if now == "02:20":
            await channel.purge()
            start = ['しりとり','霧雨魔理沙(きりさめまりさ)','多々良小傘(たたらこがさ)','リリカ・プリズムリバー']
            hajime = (random.choice(start))
            await channel.send(hajime)


    channel = client.get_channel(586420858512343050)
    okuchannel1 = client.get_channel(626630881326661632)
    okuchannel2 = client.get_channel(627040994851946496)
    if now.month == 10 and now.day == 10 and now.hour == 21 and now.minute == 00:
        await channel.send("オク終了まであと3日です・・・")
    
    if now.month == 10 and now.day == 12 and now.hour == 21 and now.minute == 00:
        await channel.send("オク終了まであと一日です・・・")

    if now.month == 10 and now.day == 13 and now.hour == 20 and now.minute == 00:
        await channel.send("オク終了まであと1時間です・・・")

    if now.month == 10 and now.day == 13 and now.hour == 20 and now.minute == 50:
        await channel.send("オク終了まであと10分です・・・")

    if now.month == 10 and now.day == 13 and now.hour == 20 and now.minute == 59:
        await channel.send("オク終了まであと1分です・・・")
    
    if now.month == 10 and now.day == 13 and now.hour == 21 and now.minute == 00:
        await channel.send ("オークション締め切ります。以降の買い値提示はできません。")
        await channel.send("この発表があるころ多分私はバイト中です。落札者様、もう少しお待ちください。")
        await okuchannel1.send("オークション締め切ります。このメッセージ以降の買い値提示はすべて無効となります。")
        await okuchannel2.send("オークション締め切ります。このメッセージ以降の買い値提示はすべて無効となります。")
            
    
loop.start()#ループ処理実行

                
client.run("NTk0MDUyMzQ5MTQwNDAyMTc5.XRW0fA.FpO2ru74maCDsqbBFMeT9K-v1fA")#botを動かすのに必要