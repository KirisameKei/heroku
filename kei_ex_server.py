import discord,random,re,datetime,json,time,math,os,asyncio,requests,bs4,ast
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート/name

from quote import expand#メッセージリンク展開用

import server_log,kyoutuu,kei_ex_server,muhou#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

async def kei_ex_server(message,client1):
    m = message.channel.send
    await kyoutuu.itibu_kyoutuu_greeting(message)
    await kyoutuu.itibu_kyoutuu_thank(message)
    await kyoutuu.itibu_kyoutuu_mention(message,client1)
    await hatugensuu_kiroku(message,client1,m)
    await role_add_remove(message,client1,m)
    await login_bonus(message,client1,m)
    await my_server_commands(message,client1,m)
    await mcid_check(message,client1,m)

    if "https://discord.gg/" in message.content or "http://discord.gg/" in message.content:
        if not message.channel.id in channel_dic.my_guild_allow_senden_channel:#宣伝許可チャンネルに入っていなければ
            await message.delete()
            await m(message.author.mention+"\n指定チャンネル以外での宣伝は禁止です！メッセージを削除しました。")

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

    if message.content.startswith("/last_login "):
        mcid = message.content.replace("/last_login ","")
        p = re.compile(r"^[a-zA-Z0-9_]+$")
        if not p.fullmatch(mcid):
            await m("MCIDに使えない文字が含まれています。")
            return
        if len(mcid) < 3:
            await m("短すぎます！")
            return
        if len(mcid) > 16:
            await m("長すぎます！")
            return
        url = f"https://w4.minecraftserver.jp/player/{mcid}"
        try:
            res = requests.get(url)
            res.raise_for_status()
            soup = bs4.BeautifulSoup(res.text, "html.parser")
            td = soup.td
            if not f'{mcid}' in f'{td}':
                await m("整地鯖にログインしたことのないMCIDです。")
                return
            last_login = soup.select('td')[1]
            await m(str(last_login))
        except requests.exceptions.HTTPError:
            await m(f'requests.exceptions.HTTPError')


    if message.content == "利子を付与します":
        if message.author != client1.user:
            await m("いいえ、しません。")
            return
        point_log_channel = client1.get_channel(634602916233216020)
        async for msg in point_log_channel.history():
            str_userid_pt = await point_log_channel.fetch_message(msg.id)
            str_userid = str_userid_pt.content[0:18]
            str_pt = str_userid_pt.content[19:]
            int_userid = int(str_userid)
            int_pt = int(str_pt)
            int_after_pt = math.floor(int_pt*1.1)
            str_after_pt = str(int_after_pt)
            await point_log_channel.send(str_userid+" "+str_after_pt)
            await str_userid_pt.delete()
        osirase_channel = client1.get_channel(585999375952642067)
        await osirase_channel.send("利子を付与しました")

    if message.content == "今週の当選発表を行います":
        if message.author != client1.user:
            await m("いいえ、しません。")
            return
        tousen_bangou = random.randint(0,999)
        str_tousen_bangou = str(tousen_bangou)
        if len(str_tousen_bangou) == 1:
            send = "00" + str_tousen_bangou
        if len(str_tousen_bangou) == 2:
            send = "0" + str_tousen_bangou
        if len(str_tousen_bangou) == 3:
            send = str_tousen_bangou
        await m("今週の当選番号は**"+send+"**です")

        atari_mae = tousen_bangou - 1
        atari_usiro = tousen_bangou + 1

        if atari_mae == -1:
            atari_mae = 999
        if atari_usiro == 1000:
            atari_usiro = 0

        atari_mae = str(atari_mae)
        atari_usiro = str(atari_usiro)
        
        if len(atari_mae) == 1:
            atari_mae = "00" + atari_mae
        if len(atari_mae) == 2:
            atari_mae = "0" + atari_mae
        if len(atari_mae) == 3:
            atari_mae = atari_mae
        if len(atari_usiro) == 1:
            atari_usiro = "00" + atari_usiro
        if len(atari_usiro) == 2:
            atari_usiro = "0" + atari_usiro
        if len(atari_usiro) == 3:
            atari_usiro = atari_usiro

        simoniketa_issyo = send[1:3]
        
        loto_kiroku_channel = client1.get_channel(654897878140977154)
        point_log_channel = client1.get_channel(634602916233216020)
        async for msg in loto_kiroku_channel.history():
            str_userid_tyuusen_bangou = await loto_kiroku_channel.fetch_message(msg.id)
            int_userid_loto_channel = int(str_userid_tyuusen_bangou.content[0:18])
            str_tyuusen_bangou = str_userid_tyuusen_bangou.content[19:22]
            if str_tyuusen_bangou == send:#ピタリ賞なら
                async for msg2 in point_log_channel.history():
                    str_userid_pt = await point_log_channel.fetch_message(msg2.id)
                    int_userid_point_channel = int(str_userid_pt.content[0:18])
                    int_before_pt = int(str_userid_pt.content[19:])
                    if int_userid_point_channel == int_userid_loto_channel:
                        int_after_pt = int_before_pt + 3456
                        str_after_pt = str(int_after_pt)
                        await point_log_channel.send(str_userid_pt.content[0:18]+" "+str_after_pt)
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await m(user_name+"の所有pt:"+str_userid_pt.content[19:]+"→"+str_after_pt)
                        break
            elif str_tyuusen_bangou == atari_mae:
                async for msg3 in point_log_channel.history():
                    str_userid_pt = await point_log_channel.fetch_message(msg3.id)
                    int_userid_point_channel = int(str_userid_pt.content[0:18])
                    int_before_pt = int(str_userid_pt.content[19:])
                    if int_userid_point_channel == int_userid_loto_channel:
                        int_after_pt = int_before_pt + 1728
                        str_after_pt = str(int_after_pt)
                        await point_log_channel.send(str_userid_pt.content[0:18]+" "+str_after_pt)
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await m(user_name+"の所有pt:"+str_userid_pt.content[19:]+"→"+str_after_pt)
                        break
            elif str_tyuusen_bangou == atari_usiro:
                async for msg4 in point_log_channel.history():
                    str_userid_pt = await point_log_channel.fetch_message(msg4.id)
                    int_userid_point_channel = int(str_userid_pt.content[0:18])
                    int_before_pt = int(str_userid_pt.content[19:])
                    if int_userid_point_channel == int_userid_loto_channel:
                        int_after_pt = int_before_pt + 1728
                        str_after_pt = str(int_after_pt)
                        await point_log_channel.send(str_userid_pt.content[0:18]+" "+str_after_pt)
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await m(user_name+"の所有pt:"+str_userid_pt.content[19:]+"→"+str_after_pt)
                        break
            elif str_tyuusen_bangou.endswith(simoniketa_issyo):
                async for msg5 in point_log_channel.history():
                    str_userid_pt = await point_log_channel.fetch_message(msg5.id)
                    int_userid_point_channel = int(str_userid_pt.content[0:18])
                    int_before_pt = int(str_userid_pt.content[19:])
                    if int_userid_point_channel == int_userid_loto_channel:
                        int_after_pt = int_before_pt + 64
                        str_after_pt = str(int_after_pt)
                        await point_log_channel.send(str_userid_pt.content[0:18]+" "+str_after_pt)
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await m(user_name+"の所有pt:"+str_userid_pt.content[19:]+"→"+str_after_pt)
                        break
            else:
                pass
        await loto_kiroku_channel.purge()
        await m("以上です")


async def hatugensuu_kiroku(message,client1,m):
    #日間発言数発表
    if message.author == client1.user:
        if message.content.startswith("日付変更をお知らせします。"):
            today = datetime.date.today()
            kinou = str(today - datetime.timedelta(days=1))
            ototoi = str(today - datetime.timedelta(days=2))
            nikkan_hatugensuu_logchannel = client1.get_channel(641511982805024768)
            flag = False
            async for msg in nikkan_hatugensuu_logchannel.history(limit=2):
                kinou_ototoi_hatugensuu = await nikkan_hatugensuu_logchannel.fetch_message(msg.id)
                if kinou_ototoi_hatugensuu.content.startswith(kinou):
                    kinou_hatugensuu = int(kinou_ototoi_hatugensuu.content[11:])
                if kinou_ototoi_hatugensuu.content.startswith(ototoi):
                    ototoi_hatugensuu = int(kinou_ototoi_hatugensuu.content[11:])
            hatugensuu_zougen = kinou_hatugensuu - ototoi_hatugensuu
            if hatugensuu_zougen > 0:
                send = "+"+str(hatugensuu_zougen)
            else:
                send = str(hatugensuu_zougen)
            await asyncio.sleep(3)
            await m("昨日の発言数："+str(kinou_hatugensuu))
            await m("前日比："+send)


async def role_add_remove(message,client1,m):
    if not message.author.bot:
        #役職付与・剥奪
        if message.content in my_guild_role_dic.ippan_role:
            if not message.channel.id in channel_dic.my_guild_allow_command_channel:
                await m("ここで実行しないでください！")
                return
            role = my_guild_role_dic.ippan_role[message.content]
            role = discord.utils.get(message.guild.roles,name=role)
            if not message.content.startswith("/not "):#notで始まっていなければ(付与系なら)
                if discord.utils.get(message.author.roles,name=role.name):
                    await m("もう持ってるじゃん・・・")
                else:
                    await message.author.add_roles(role)
                    await m(message.author.name+"に"+role.name+"を付与しました")

            else:#notで始まっていたら(剥奪系なら)
                if discord.utils.get(message.author.roles,name=role.name):
                    await message.author.remove_roles(role)
                    await m(message.author.name+"から"+role.name+"を剥奪しました")
                else:
                    await m("もう付いてないよ^^")

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


async def login_bonus(message,client1,m):
    if message.channel.id == 634602609017225225:
        if message.author.bot:
            return
        kouho = ["おめでとう！","はずれ","はずれ"]
        touraku = random.choice(kouho)
        if touraku == "おめでとう！":
            get_pt = random.randint(1,30)
            flag = False
            point_log_channel = client1.get_channel(634602916233216020)
            async for msg in point_log_channel.history():
                str_userid_pt = await point_log_channel.fetch_message(msg.id)
                int_userid = int(str_userid_pt.content[0:18])
                if int_userid == message.author.id:
                    str_before_pt = str_userid_pt.content[19:]
                    int_before_pt = int(str_before_pt)
                    int_after_pt = int_before_pt+get_pt
                    str_after_pt = str(int_after_pt)
                    await point_log_channel.send(str(message.author.id)+" "+str_after_pt)
                    await str_userid_pt.delete()
                    await m(touraku+str(get_pt)+"ptゲット！\n"+message.author.name+"の所有pt:"+str_before_pt+"→"+str_after_pt)
                    flag = True
                    break
            if not flag:
                str_get_pt = str(get_pt)
                await point_log_channel.send(str(message.author.id)+" "+str_get_pt)
                await m(touraku+message.author.name+"が初めてptを獲得しました。\n"+message.author.name+"の所有pt:"+str_get_pt)

        else:
            await m(touraku)

    if message.content == "/mypt" or message.content.startswith("/otherpt ") or \
        message.content.startswith("/addpt ") or message.content.startswith("/usept ") or message.content.startswith("/lottery "):
        await point_commands(message,client1,m)


async def my_server_commands(message,client1,m):
    if message.content == "/accept":
        if not message.channel.id == 592581835343659030:
            await m("ここで実行しないでください！")
            return
        if not discord.utils.get(message.author.roles,name="新規"):
            await m("もう付いてないよ^^")
            return
        if not discord.utils.get(message.author.roles,name="accept送信可能"):
            await m("まず<#640833025822949387>をお願いします。")
            return
        sinki_role = discord.utils.get(message.guild.roles,name="新規")
        accept_role = discord.utils.get(message.guild.roles,name="accept送信可能")
        crafter_role = discord.utils.get(message.guild.roles,name="クラフタ")
        await message.author.remove_roles(sinki_role)
        await message.author.remove_roles(accept_role)
        await message.author.add_roles(crafter_role)
        await m(message.author.name+"から新規を剥奪し、クラフタを付与しました。")
        await m(message.author.mention+"\n"+message.author.name+"さん参加ありがとうございます。\n\
このチャンネルで<#592576217962512394>や<#592576272752967681>を参考に、自分に必要な役職をつけてください。\n\
もしよろしければ、<#586571234276540449>もお願いします。")

    if message.content == "/omikuji" or message.content == "/speca" or message.content == "/meigen" or \
        message.content.startswith("/osusume_") or message.content.startswith("/name ") or message.content.startswith("/weather ") or \
        message.content.startswith("/stimer ") or message.content.startswith("/mtimer ") or message.content.startswith("/htimer ") or \
        message.content.startswith("/role_count ") or message.content.startswith("/mcid ") or message.content.startswith("/vote ") or \
        message.content.startswith("/mcavatar ") or message.content == "/help":
        if not message.channel.id in channel_dic.my_guild_allow_command_channel:
            await m("ここで実行しないでください！")
            return

        if message.content == "/omikuji":
            send = random.choice(message_list.omikuji)
            await m(send)

        if message.content == "/speca":
            send = random.choice(message_list.speca)
            await m(send)

        if message.content == "/meigen":
            send = random.choice(message_list.meigen)
            await m(send)
        
        if message.content == "/osusume_eshi":
            send = random.choice(message_list.osusume_eshi)
            await m(send)

        if message.content == "/osusume_youtuber":
            send = random.choice(message_list.osusume_youtuber)
            await m(send)

        if message.content == "/osusume_movie":
            send = random.choice(message_list.osusume_movie)
            await m(send)

        if message.content.startswith("/name "):
            try:
                int_loop_suu = int(message.content[6:])
                if int_loop_suu > 10:
                    await m("長すぎます！10文字以下にしてください。")
                    return
                if int_loop_suu < 1:
                    await m("短すぎます！1文字以上にしてください。")
                    return
                kouho = random.choice(message_list.name_kouho)
                send = kouho
                for i in range(int_loop_suu-1):
                    kouho = random.choice(message_list.name_kouho)
                    send += kouho
                await m(send)
            except ValueError:
                await m("文字数は半角数字で入力してください。")

        if message.content.startswith("/weather "):
            reg_res = re.compile(u"/weather (.+)").search(message.content)
            if reg_res:
                if reg_res.group(1) in message_list.citycodes.keys():
                    citycode = message_list.citycodes[reg_res.group(1)]
                    resp = urllib.request.urlopen('http://weather.livedoor.com/forecast/webservice/json/v1?city=%s'%citycode).read()
                    resp = json.loads(resp.decode('utf-8'))
                    msg = resp['publicTime']+"に発表\n"
                    msg += resp['location']['city']+"の天気は、\n"
                    for f in resp['forecasts']:
                        msg += f['dateLabel'] + "が" + f['telop']+"\n"
                    msg += "です。\n"
                    AsuMaxTemp = resp['forecasts'][1]['temperature']['max']['celsius']
                    AsuMinTemp = resp['forecasts'][1]['temperature']['min']['celsius']
                    try:
                        KyouMaxTemp = resp['forecasts'][0]['temperature']['max']['celsius']#今日の最高気温を試す
                        try:#今日の最低気温を試す
                            KyouMinTemp = resp['forecasts'][0]['temperature']['min']['celsius']
                            await message.channel.send(message.author.mention+"\n"+msg+"今日の最高気温は"+KyouMaxTemp+"℃で、最低気温は"+KyouMinTemp+"℃、\n\
明日の最高気温は"+AsuMaxTemp+"℃で、最低気温は"+AsuMinTemp+"℃です。")
                        except TypeError:#最高は取得成功、最低は取得失敗
                            await message.channel.send(message.author.mention+"\n"+msg+"今日の最高気温は"+KyouMaxTemp+"℃で、最低気温の情報なし、\n\
明日の最高気温は"+AsuMaxTemp+"℃で、最低気温は"+AsuMinTemp+"℃です。")
                    except TypeError:#最高の取得失敗、最低不明
                        try:#今日の最低気温を試す
                            KyouMinTemp = resp['forecasts'][0]['temperature']['min']['celsius']#最高の取得失敗、最低の取得成功
                            await message.channel.send(message.author.mention+"\n"+msg+"今日の最高気温は情報なしで、最低気温は"+KyouMinTemp+"℃、\n\
明日の最高気温は"+AsuMaxTemp+"℃で、最低気温は"+AsuMinTemp+"℃です。")
                        except TypeError:#最高も最低も取得失敗
                            await message.channel.send(message.author.mention+"\n"+msg+"今日の最高気温の情報なしで、最低気温の情報もなし、\n\
明日の最高気温は"+AsuMaxTemp+"℃で、最低気温は"+AsuMinTemp+"℃です。")
                else:
                    await message.channel.send("そこの天気はわかりません...")

        if message.content.startswith("/role_count "):
            str_role_id = message.content[12:30]
            try:
                int_role_id = int(str_role_id)
                role = discord.utils.get(message.guild.roles,id=int_role_id)
                ninzuu = str(len(role.members))
                if int_role_id == 585998962050203672:
                    await m("このサーバには"+ninzuu+"人います。")
                else:
                    await m(role.name+"は"+ninzuu+"人います。")

            except ValueError:
                await m("IDは18桁の半角数字です。")

        if message.content.startswith("/mcid "):
            str_userid = message.content[6:]
            if not len(str_userid) == 18:
                await m("IDは18桁の半角数字です。")
                return
            try:
                int_userid = int(str_userid)
                member = message.guild.get_member(int_userid)
                mcid_log_channel = client1.get_channel(638912957421453322)
                flag = False
                how_many_accounts = 0
                send_msg = member.name+"のMCID:\n"
                async for msg in mcid_log_channel.history():
                    userid_mcid = await mcid_log_channel.fetch_message(msg.id)
                    if userid_mcid.content[0:18] == str_userid:
                        mcid = userid_mcid.content[19:]
                        send_msg += mcid+"\n"
                        how_many_accounts = how_many_accounts + 1
                        flag = True
                    
                if not flag:
                    await m("まだMCIDを報告していないユーザーです。")

                if flag:
                    send_msg += "以上"+str(how_many_accounts)+"アカ"
                    await m(send_msg)

            except ValueError:
                await m("IDは18桁の半角数字です。")

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

        if message.content == "/help":
            help_command = "\
            /crafter\n\
            /shooter\n\
            **__/tuuti__**\n\
            /omikuji\n\
            /speca\n\
            /meigen\n\
            /htimer n content\n\
            /mtimer n content\n\
            /stimer n content\n\
            /osusume_eshi\n\
            /osusume_youtuber\n\
            /osusume_movie\n\
            "
            help_kyodou = "\
            クラフタ役職を付与\n\
            シュータ役職を付与\n\
            **__通知ほしい役職を付与__**\n\
            おみくじが引けます\n\
            けいが独断と偏見で選んだ名スペカを宣言します\n\
            けいが独断と偏見で選んだ名言と迷言を言います\n\
            n時間後にメンション付きでcontentを送ります\n\
            n分後に(ry\n\
            n秒後に(ry\n\
            けいの好きな絵師を紹介します\n\
            けいの好きな動画投稿者を紹介します\n\
            けいの好きな動画を紹介します\n\
            "

            help_sonota = "\
            ・「ありがとう」の入ったメッセージを送ると反応します\n\
            ・「おはよう」「こんにちは」「こんばんは」の入ったメッセージを送ると時間によって違う反応をします\n\
            ・毎週しりとりチャンネルをリセットして最初のお題を言います。\n\
            ・<#634602609017225225>にメッセージを送ると確率でポイントがもらえます(1pt == 1ガチャ券)\n\
            ・毎週日曜日にを持っているユーザーに利子を付与します\n\
            ・しりとりを「ん」や「ン」で終わらせると続けてくれます\n\
            ・隠し要素がいくつかあります。最初に発見すれば役職がもらえます。(現在一枠あります)\n\
            ・「魔理ちゃんのことが大好きです」というとフラれます。実は告白成功するバグが仕様で存在します。最初に見つけた人には役職あげます。\n\
            ・指定チャンネル以外でディスコの招待リンクを貼ると消されて怒られます。\n\
            ・DMにメッセージを送ると返事をします。(ラグがひどいです)\n\
            ・発言数をカウントします。日間発言数とユーザーごとの発言数があり、日間は一日の最後に発表、ユーザーはレベルアップ機能があります。\n\
            ・管理者以外が/tokusyu、/delmsgを実行すると魔理ちゃんに怒られます。そして・・・？```\n\
            "

            help_embed_1 = discord.Embed(title="HELP(1/2)",description="[コマンド系]",color=0x0000ff)
            help_embed_1.add_field(name="コマンド",value=help_command)
            help_embed_1.add_field(name="挙動",value=help_kyodou)

            help_embed_2 = discord.Embed(title="HELP(2/2)",description="[その他の機能]",color=0x0000ff)
            help_embed_2.add_field(value=help_sonota)

            await m(embed=help_embed_1)
            await m(embed=help_embed_2)


async def mcid_check(message,client1,m):
    if message.channel.id == 640833025822949387:
        if message.author == client1.user:
            return
        p = re.compile(r"^[a-zA-Z0-9_ ]+$")
        if not p.fullmatch(message.content):
            await m("MCID報告に使えない文字が含まれています。")
            return
        mcid_log_channel = client1.get_channel(638912957421453322)
        mcid_list = message.content.split(" ")
        for i in range(len(mcid_list)):
            try:
                mcid_mojisuu = len(mcid_list[i])
                if mcid_mojisuu < 3:
                    await m("**"+mcid_list[i]+"**は短すぎます。")
                    del mcid_list[i]
                if mcid_mojisuu > 16:
                    await m("**"+mcid_list[i]+"**は長すぎます。")
                    del mcid_list[i]
            except IndexError:
                pass

        for i in range(len(mcid_list)):
            try:
                flag = False
                async for msg in mcid_log_channel.history():
                    userid_mcid = await mcid_log_channel.fetch_message(msg.id)
                    mcid = userid_mcid.content[19:]
                    ch = client1.get_channel(595072339545292804)
                    if mcid_list[i] == mcid:
                        await m(f"**{mcid}**は既に登録されています。これが本当に現在の自分のMCIDならけいにお知らせください。")
                        del mcid_list[i]
                        flag = True
                        break
            except IndexError:
                pass
        
        right_mcid_list = []
        for i in range(len(mcid_list)):
            mcid = mcid_list[i]
            mcid = str.lower(mcid)
            url = f"https://w4.minecraftserver.jp/player/{mcid}"
            try:
                res = requests.get(url)
                res.raise_for_status()
                soup = bs4.BeautifulSoup(res.text, "html.parser")
                td = soup.td
                if f'{mcid}' in f'{td}':
                    right_mcid_list.append(mcid)
                    await mcid_log_channel.send(str(message.author.id)+" "+mcid)
                else:
                    await m("**"+mcid+"**は\n・実在しない\n・整地鯖にログインしたことがない\n\
・MCIDを変更した\n・整地鯖ログイン後1分以上たっていない\n・MCID変更後整地鯖にログインして1分以上たっていない\n可能性があります。\n\
この機能は整地鯖ウェブページへの負荷となります。__**意図的に間違った入力を繰り返していると判断した場合処罰の対象になります。**__もしこれがバグならけいにお知らせください。")
            except requests.exceptions.HTTPError:
                await m(f'requests.exceptions.HTTPError')
        await m("MCIDの登録が完了しました。登録されたMCID:"+str(right_mcid_list))
        if discord.utils.get(message.author.roles,name="新規"):
            role = discord.utils.get(message.guild.roles,name = "accept送信可能")
            await message.author.add_roles(role)
            await m(message.author.mention+"MCIDの報告ありがとうございます。ルールに同意いただけるなら<#592581835343659030>で**/accept**をお願い致します。")
        else:
            await m("MCID追加の報告ありがとうございます。")

    if message.channel.id == 640833084782018580:
        if message.author == client1.user:
            return
        if not "→" in message.content:
            await m("MCID変更報告の形式は旧MCID→新MCIDです。")
            return
        p = re.compile(r"^[a-zA-Z0-9_→]+$")
        if not p.fullmatch(message.content):
            await m("MCID変更報告に使えない文字が含まれています。")
            return
        mcid_log_channel = client1.get_channel(638912957421453322)
        old_mcid_user_say = message.content.split("→")[0]
        new_mcid = message.content.replace(old_mcid_user_say+"→","")
        if old_mcid_user_say == new_mcid:
            await m("変えてないじゃん！")
            return
        flag = False
        async for msg in mcid_log_channel.history():
            userid_mcid = await mcid_log_channel.fetch_message(msg.id)
            userid = int(userid_mcid.content[0:18])
            old_mcid_touroku = userid_mcid.content[19:]
            if old_mcid_touroku == old_mcid_user_say:
                if not userid == message.author.id:
                    await m("他人のMCIDの変更報告はできません")
                    flag = True
                    break
                flag1 = False
                async for msg in mcid_log_channel.history():
                    touroku_mcid = await mcid_log_channel.fetch_message(msg.id)
                    if touroku_mcid.content[19:] == new_mcid:
                        await m("そのMCIDはすでに登録されています。これが本当に現在の自分のMCIDならけいにお知らせください。")
                        flag1 = True
                        flag = True
                        break
                    if not flag1:
                        await change_mcid(message,client1,m,new_mcid,userid_mcid)
                        flag = True
                        break

        if not flag:
            await m("まだ登録されていないMCIDを変更しようとしています")


async def point_commands(message,client1,m):
    if not message.channel.id in channel_dic.my_guild_allow_command_channel:
        await m("ここで実行しないでください！")
        return

    point_log_channel = client1.get_channel(634602916233216020)
    if message.content == "/mypt":
        flag = False
        async for msg in point_log_channel.history():
            str_userid_pt = await point_log_channel.fetch_message(msg.id)
            if str_userid_pt.content.startswith(str(message.author.id)):
                str_pt = str_userid_pt.content[19:]
                await m(message.author.name+"さんの所有pt:"+str_pt)
                flag = True
                break
        if not flag:
            await m(message.author.name+"さんはまだptを保有していません。")

    if message.content.startswith("/otherpt "):
        try:
            nyuuryoku_user_id = int(message.content[9:27])
            try:
                ptwo_nusumimirareru_user = client1.get_user(nyuuryoku_user_id)
                flag = False
                async for msg in point_log_channel.history():
                    str_userid_pt = await point_log_channel.fetch_message(msg.id)
                    if str_userid_pt.content.startswith(message.content[9:27]):
                        str_pt = str_userid_pt.content[19:]
                        await m(ptwo_nusumimirareru_user.name+"の所有pt:"+str_pt)
                        flag = True
                        break
                if not flag:
                    await m(ptwo_nusumimirareru_user.name+"さんはまだptを保有していません。")
            except AttributeError:#要検証
                await m("そのユーザーはこのサーバにいません。")
        except ValueError:
            await m("ユーザーIDは18桁の半角数字です、")

    if message.content.startswith("/addpt "):
        if not discord.utils.get(message.author.roles,name="けい"):
            await m("何様のつもり？")
            return
        try:
            nyuuryoku_user_id = int(message.content[7:25])
            try:
                nyuuryoku_pt = int(message.content[26:])
                try:
                    ptwo_huyosareru_user = client1.get_user(nyuuryoku_user_id)
                    flag = False
                    async for msg in point_log_channel.history():
                        str_userid_pt = await point_log_channel.fetch_message(msg.id)
                        if str_userid_pt.content.startswith(message.content[7:25]):
                            int_before_pt = int(str_userid_pt.content[19:])
                            int_after_pt = int_before_pt + nyuuryoku_pt
                            str_after_pt = str(int_after_pt)
                            await point_log_channel.send(message.content[7:25]+" "+str_after_pt)
                            await m(ptwo_huyosareru_user.name+"の所有pt:"+str_userid_pt.content[19:]+"→"+str_after_pt)
                            flag = True
                            break
                    if not flag:
                        await point_log_channel.send(message.content[7:])
                        await m(ptwo_huyosareru_user.name+"が初めてptを獲得しました。\n"+\
                            ptwo_huyosareru_user.name+"の保有pt:"+message.content[26:])
                except AttributeError:#要検証
                    await m("そのユーザーはこのサーバにいません。")
            except NameError:#要検証
                await m("付与するptは半角数字を使用してください。")
        except NameError:#要検証
            await m("ユーザーIDは18桁の半角数字です。")

    if message.content.startswith("/usept "):
        if not discord.utils.get(message.author.roles,name="けい"):
            await m("何様のつもり？")
            return
        try:
            nyuuryoku_user_id = int(message.content[7:25])
            try:
                nyuuryoku_pt = int(message.content[26:])
                try:
                    ptwo_hakudatusareru_user = client1.get_user(nyuuryoku_user_id)
                    flag = False
                    async for msg in point_log_channel.history():
                        str_userid_pt = await point_log_channel.fetch_message(msg.id)
                        if str_userid_pt.content.startswith(message.content[7:25]):
                            int_before_pt = int(str_userid_pt.content[19:])
                            int_after_pt = int_before_pt - nyuuryoku_pt
                            str_after_pt = str(int_after_pt)
                            if int_after_pt < 0:
                                await m("ptが足りません。")
                                flag = True
                                return
                            await point_log_channel.send(message.content[7:25]+" "+str_after_pt)
                            await m(ptwo_hakudatusareru_user.name+"の所有pt:"+str_userid_pt.content[19:]+"→"+str_after_pt)
                            flag = True
                            break
                    if not flag:
                        await m(ptwo_hakudatusareru_user.name+"さんはまだptを保有していません。")
                except AttributeError:#要検証
                    await m("そのユーザーはこのサーバにいません。")
            except NameError:#要検証
                await m("付与するptは半角数字を使用してください。")
        except NameError:#要検証
            await m("ユーザーIDは18桁の半角数字です。")

    if message.content.startswith("/lottery "):
        tyuusen_bangou = message.content[9:12]
        if not len(tyuusen_bangou) == 3:
            await m("抽選番号は3桁で指定してください")
            return
        try:
            int_tyuusen_bangou = int(tyuusen_bangou)
            flag = False
            async for msg in point_log_channel.history():
                str_userid_pt = await point_log_channel.fetch_message(msg.id)
                str_userid = str_userid_pt.content[0:18]
                str_before_pt = str_userid_pt.content[19:]
                int_before_pt = int(str_before_pt)
                if str(message.author.id) == str_userid:
                    int_after_pt = int_before_pt - 64
                    if int_after_pt < 0:
                        await m("ptが足りません")
                        flag = True
                        break
                    await point_log_channel.send(str(message.author.id)+" "+str(int_after_pt))
                    await str_userid_pt.delete()
                    loto_kiroku_channel = client1.get_channel(654897878140977154)
                    await loto_kiroku_channel.send(str(message.author.id)+" "+tyuusen_bangou)
                    flag = True
                    break
            if not flag:
                await m("まだptを保有していません")
        except ValueError:
            await m("抽選番号は半角数字です")


async def change_mcid(message,client1,m,new_mcid,userid_mcid):
    mcid_log_channel = client1.get_channel(638912957421453322)
    mcid = str.lower(new_mcid)
    url = f"https://w4.minecraftserver.jp/player/{mcid}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        td = soup.td
        if f'{mcid}' in f'{td}':
            await mcid_log_channel.send(str(message.author.id)+" "+mcid)
            await userid_mcid.delete()
            await m("MCIDの変更登録が完了しました。")
        else:
            await m("**"+mcid+"**は\n・実在しない\n・整地鯖にログインしたことがない\n\
・MCIDを変更した\n・整地鯖ログイン後1分以上たっていない\n・MCID変更後整地鯖にログインして1分以上たっていない\n可能性があります。\n\
この機能は整地鯖ウェブページへの負荷となります。__**意図的に間違った入力を繰り返していると判断した場合処罰の対象になります。**__もしこれがバグならけいにお知らせください。")
    except requests.exceptions.HTTPError:
        await m(f'requests.exceptions.HTTPError')


"""
async def kikaku(message,client1,m):
    five_sauzando_role = discord.utils.get(message.guild.roles,id=668021019700756490)
    if message.channel.id == 665487669953953804:
        if message.author == client1.user:
            return
        if message.content == "/cancel":
            if discord.utils.get(message.author.roles,id=668021019700756490):
                await m(f"{message.author.name}さんの参加をキャンセルしました。")
                await message.author.remove_roles(five_sauzando_role)
            else:
                await m("もう付いてないよ^^")
            return
        if discord.utils.get(message.author.roles,id=668021019700756490):
            await m(f"{message.author.name}さんは既に参加しています。")
            return
        p = re.compile(r"^[0-9a-zA-Z_]+$")
        if not p.fullmatch(message.content):
            await m("MCIDに使用できない文字が含まれています。")
            return
        if len(message.content) < 3:
            await m("短すぎます！")
            return
        if len(message.content) > 16:
            await m("長すぎます！")
            return
        mcid_log_channel = client1.get_channel(638912957421453322)
        flag = False
        async for msg in mcid_log_channel.history():
            userid_mcid = await mcid_log_channel.fetch_message(msg.id)
            if int(userid_mcid.content[0:18]) == message.author.id and userid_mcid.content[19:] == message.content:
                await m(f"{message.author.name}さんが抽選に参加しました。")
                await message.author.add_roles(five_sauzando_role)
                flag = True
                break
        if not flag:
            await m(f"{message.author.mention}そのMCIDは登録されていないか、あなたのMCIDではありません。")

    movie_watched_role = discord.utils.get(message.guild.roles,id=668021150952980491)
    sikatanakutukutta_role = discord.utils.get(message.guild.roles,id=671239038321164319)
    if message.channel.id == 665487568854319124:
        if message.author == client1.user:
            return
        if message.content == "/cancel":
            if discord.utils.get(message.author.roles,id=668021150952980491):
                await m(f"{message.author.name}さんの参加をキャンセルしました。")
                await message.author.remove_roles(movie_watched_role)
            else:
                await m("もう付いてないよ^^")
            return
        if discord.utils.get(message.author.roles,id=671239038321164319):
            return
        if discord.utils.get(message.author.roles,id=668021150952980491):
            await m(f"{message.author.name}さんは既に参加しています。")
            return
        p = re.compile(r"^[0-9a-zA-Z_]+$")
        if not p.fullmatch(message.content):
            await m("MCIDに使用できない文字が含まれています。")
            return
        if len(message.content) < 3:
            await m("短すぎます！")
            return
        if len(message.content) > 16:
            await m("長すぎます！")
            return
        mcid_log_channel = client1.get_channel(638912957421453322)
        await message.author.add_roles(sikatanakutukutta_role)
        flag = False
        async for msg in mcid_log_channel.history():
            userid_mcid = await mcid_log_channel.fetch_message(msg.id)
            if int(userid_mcid.content[0:18]) == message.author.id and userid_mcid.content[19:] == message.content:
                await m(f"{message.author.name}さんが抽選に参加しました。")
                await message.author.add_roles(movie_watched_role)
                flag = True
                break
        if not flag:
            await m("そのMCIDは登録されていないか、あなたのMCIDではありません。")
        await message.author.remove_roles(sikatanakutukutta_role)

    if message.content == "/choice":
        kikaku_sanka_user = five_sauzando_role.members
        tousen_user_raretu = ""
        try:
            tousen_user = random.sample(kikaku_sanka_user,5)
            for i in range(5):
                tousen_user_raretu += tousen_user[i].name + "\n"
        except ValueError:
            for i in range(len(kikaku_sanka_user)):
                tousen_user_raretu += kikaku_sanka_user[i].name + "\n"
        await m(tousen_user_raretu+"\nさんが当たりです(これは疑似抽選です)")"""