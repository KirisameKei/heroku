import discord,random,re,datetime,json,time,math,os,asyncio,requests,bs4,ast,sys,traceback
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
#from discord import FFmpegPCMAudio
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用
import quote

try:
    import tokens
except ModuleNotFoundError:
    pass

import kyoutuu,kei_ex_server,muhou,iroha#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

import kohga#依頼

client1 = discord.Client()#魔理沙bot(メインで使用)
client2 = discord.Client()#小傘bot(VC関連用)
client4 = discord.Client()#零bot

try:
    import tokens_ConoHa
except ModuleNotFoundError: #けいローカル or heroku
    try:
        path = r"C:\Users\hayab\tokens_Local.txt"
        with open(path, mode="r") as f:
            program_data_list = f.readlines()
            discord_bot_token_1 = program_data_list[0]
            discord_bot_token_2 = program_data_list[1]
            discord_bot_token_4 = program_data_list[3]
            where_from = program_data_list[4]
    except FileNotFoundError: #heroku
        discord_bot_token_1 = os.getenv("discord_bot_token_1")
        discord_bot_token_2 = os.getenv("discord_bot_token_2")
        discord_bot_token_4 = os.getenv("zero_bot_token")
        where_from = os.getenv("where_from")
else: #ConoHa
    discord_bot_token_1 = tokens_ConoHa.discord_bot_token_1
    discord_bot_token_2 = tokens_ConoHa.discord_bot_token_2
    discord_bot_token_4 = tokens_ConoHa.discord_bot_token_4
    where_from = tokens_ConoHa.where_from


def unexpected_error():
    """
    予期せぬエラーが起きたときの対処
    エラーメッセージ全文と発生時刻をウェブフックで通知"""

    now = datetime.datetime.now().strftime("%H:%M") #今何時？
    error_msg = f"```\n{traceback.format_exc()}```" #エラーメッセージ全文
    #webhookで投稿する中身
    main_content = {
        "username": "ERROR", #表示されるwebhook名
        "avatar_url": "https://cdn.discordapp.com/attachments/644880761081561111/703088291066675261/warning.png", #使用アイコン
        "content": "<@523303776120209408>", #けいにメンション
        "embeds": [ #エラー内容・発生時間まとめ
            {
                "title": "エラーが発生しました",
                "description": error_msg,
                "color": 0xff0000,
                "footer": {
                    "text": now
                }
            }
        ]
    }
    error_notice_webhook_url = "https://discordapp.com/api/webhooks/704300492280561745/7bxBfj0T4RTx85l6rzACcuoNt0fqZayyA5cYQh4WTQQ53Q-HyTWNnZ2X_9pRS4RY3yc0"
    requests.post(error_notice_webhook_url, json.dumps(main_content), headers={'Content-Type': 'application/json'}) #エラーメッセをウェブフックに投稿


@client1.event
async def on_ready():
    try:
        login_notice_ch = client1.get_channel(595072269483638785)
        await login_notice_ch.send(f"{client1.user.name}がログインしました(from:{where_from})")
        print(f"{client1.user.name}がログインしました")
    except:
        unexpected_error()


@client2.event
async def on_ready():
    print(client2.user.name+"がログインしました")
    login_channel = client2.get_channel(595072339545292804)
    await login_channel.send(client2.user.name+"がログインしました")
    await client2.change_presence(activity = discord.Game(name = "まだ無機能"))


@client4.event
async def on_ready():
    print(client4.user.name+"がログインしました")


@client1.event
async def on_guild_join(guild):
    for g in guild.text_channels:
        syoukai_msg = "初めましての方は初めまして、そうでない方はまたお会いしましたね。<@!523303776120209408>制作の魔理沙botです。\n"
        syoukai_msg += f"このbotを{guild.name}に導入していただきありがとうございます。\n"
        syoukai_msg += "皆様にお願いしたいことがあります。このbotに極度に負荷をかけるような行為をしないでください。また、"
        syoukai_msg += "私のサーバに書かれている利用規約に記載された招待用コマンドの実行以外でこのbotの招待リンクを作成・使用・配布しないでください。\n"
        syoukai_msg += "バグ、不具合等問題がありましたら容赦なく<@!523303776120209408>にメンションかDMを飛ばしてください。\n"
        syoukai_msg += "問題がなかったらお楽しみください。\n"
        syoukai_msg += "最後に私のサーバを紹介・宣伝します。https://discord.gg/nrvMKBT このbotについてもっと知りたい、このbotを招待したい、けいの活動に興味がある、"
        syoukai_msg += "理由は何でも構いません。ぜひ見ていってください"
        try:
            await g.send(syoukai_msg)
            break
        except:
            pass

    sanka_dattai_channel = client1.get_channel(588224929300742154)
    await sanka_dattai_channel.send(f"{client1.user.name}が{guild.name}に参加しました。")

    for ch in guild.text_channels:
        try:
            invite = await ch.create_invite(reason="けいを招待するため")
            break
        except:
            pass
    kei = client1.get_user(523303776120209408)
    dm = await kei.create_dm()
    await dm.send(invite)


@client1.event
async def on_guild_remove(guild):
    sanka_dattai_channel = client1.get_channel(588224929300742154)
    await sanka_dattai_channel.send(f"{client1.user.name}が{guild.name}から抜けました。")


@client1.event
async def on_member_join(member):#新規の人が来たら反応
    if member.id == 395796458051469313:
        shut_up = discord.utils.get(member.guild.roles,id=628175600007512066)
        await member.add_roles(shut_up)
        bougen_list = [
            "mother_fucker!:middle_finger:",
            ":middle_finger:",
            "shut up!",
            "fuck you!:middle_finger:",
            "what a bother! ",
            "You are gross",
            "You are rubbish",
            "Your mother has a big navel"
        ]
        for i in range(100):
            await member.send(random.choice(bougen_list))
        await member.guild.kick(member)
        return
    sanka_dattai_channel = client1.get_channel(588224929300742154)
    if member.guild.id == 585998962050203672:#けいの実験サーバなら
        if member.id in ban_list.ban_list:
            await member.guild.kick(member)
            await sanka_dattai_channel.send(member.mention+"がサーバに入ろうとしましたが失敗しました")
        
        elif member.id == 679650092025643018:
            spam_ch = client1.get_channel(586075792950296576)
            for i in range(100):
                msg = [":middle_finger:","mother fucker!!","DMでの迷惑行為は楽しいかぁ！？","そうゆうのスパムって言うんだゾ","くたばれ","fuck off!!","引っ込め"]
                send_msg = random.choice(msg)
                await spam_ch.send(f"<@!586075792950296576>{send_msg}")

        else:
            try:
                old_role = my_guild_role_dic.keizoku_role[member.id]
                old_role = discord.utils.get(member.guild.roles,id=old_role)
                await member.add_roles(old_role)
                await sanka_dattai_channel.send(member.name+"さんは過去に"+old_role.name+"を持っていたため付与しました")
            except KeyError:
                pass
            
            sinki_role = discord.utils.get(member.guild.roles,id=621641465105481738)#新規役職を指定
            await member.add_roles(sinki_role)
            kangei_msg = member.mention+"さんようこそ！:tada:\n"
            kangei_msg += "まず<#640833025822949387>をお願いします\n"
            kangei_msg += "次に、<#586000955053441039>を読んで同意していただけるなら"
            kangei_msg += "<#592581835343659030>で**/accept**と打ち込んでください"
            await sanka_dattai_channel.send(kangei_msg)
            made_time = member.created_at + datetime.timedelta(hours=9)
            made_time_msg = f"{member.name}さんは{made_time.year}年{made_time.month}月{made_time.day}日"
            made_time_msg += f"{made_time.hour}時{made_time.minute}分{made_time.second}秒からdiscordを使用しています。"
            await sanka_dattai_channel.send(made_time_msg)
            
    elif member.guild.id == 587909823665012757:#無法地帯なら
        if member.id in ban_list.ban_list:
            await member.guild.kick(member)
            await sanka_dattai_channel.send(f"{member.name}が無法地帯に入ろうとして失敗しました")
        else:
            if member.id == 672910471279673358 or member.id == 684949442280947718:
                await member.guild.kick(member)
                await sanka_dattai_channel.send(f"{member.name}が無法地帯に入ろうとして失敗しました")
                return
            await sanka_dattai_channel.send(member.name+"が無法地帯に参加しました。")

    elif member.guild.id == 624551872933527553:#処罰部なら
        await sanka_dattai_channel.send(member.name+"がHJKに参加しました。")

    else:
        await sanka_dattai_channel.send(member.name+"さんが"+member.guild.name+"に参加しました。")
        
    if member.guild.id == 604945424922574848:#いろは鯖なら
        if member.id in ban_list.ban_list:
            await member.guild.kick(member)
            await sanka_dattai_channel.send(f"{member.mention}がいろは鯖に入ろうとしましたが失敗しました")


@client1.event
async def on_member_remove(member):#脱退者が出たら反応
    sanka_dattai_channel = client1.get_channel(588224929300742154)
    if member.guild.id == 585998962050203672:#けいの実験サーバなら
        if member.id in ban_list.ban_list:
            pass
        else:
            await sanka_dattai_channel.send(member.mention+"さんさようなら:sob:")
            mcid_log_channel = client1.get_channel(638912957421453322)
            async for msg in mcid_log_channel.history():
                user_id_mcid = await mcid_log_channel.fetch_message(msg.id)
                if user_id_mcid.content.startswith(str(member.id)):
                    await user_id_mcid.delete()

    elif member.guild.id == 587909823665012757:#無法地帯なら
        await sanka_dattai_channel.send(member.name+"さんが無法地帯のカオスさに耐えられなくなりました")

    elif member.guild.id == 624551872933527553:#処罰部なら
        await sanka_dattai_channel.send(member.name+"がHJKから抜けました")

    else:
        await sanka_dattai_channel.send(member.name+"さんが"+member.guild.name+"から抜けました。")


@client1.event
async def on_guild_channel_create(channel):
    channel_dic_channel = client1.get_channel(663037675141595147)

    if channel.guild.id == 585998962050203672:#けいの実験サーバ
        channel_dic_in_embed = await channel_dic_channel.fetch_message(682935760512352274)
        channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
        channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
        channel_dic_in_channel[channel.id] = new_channel.id
        channel_dic_in_channel = str(channel_dic_in_channel)
        channel_dic_record_embed = discord.Embed(title="けいの実験サーバ",description=channel_dic_in_channel)

        kei_ex_server_log_guild = client1.get_guild(647311568454811649)
        new_channel = await kei_ex_server_log_guild.create_text_channel(name=channel.name)
        sagyousiji_channel = client1.get_channel(636359382359080961)
        await sagyousiji_channel.send(f"<@!523303776120209408>\n新しいチャンネル「{channel.name}」が{channel.guild.name}で作成されました。\n\
            辞書に追加してください。\n{channel.id}:{new_channel.id},#{channel.name}")

    elif channel.guild.id == 624551872933527553:#処罰部
        channel_dic_in_embed = await channel_dic_channel.fetch_message(682944795794079767)
        channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
        channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
        channel_dic_in_channel[channel.id] = new_channel.id
        channel_dic_in_channel = str(channel_dic_in_channel)
        channel_dic_record_embed = discord.Embed(title="HJK",description=channel_dic_in_channel)

        syobatubu_log_guild = client1.get_guild(633328124968435712)#やることリスト
        new_channel = await syobatubu_log_guild.create_text_channel(name=channel.name)
        sagyousiji_channel = client1.get_channel(638904268543361037)#作業指示書
        await sagyousiji_channel.send(f"<@!523303776120209408>\n新しいチャンネル「{channel.name}」が作成されました。\n\
            辞書に追加してください。\n{channel.id}:{new_channel.id},#{channel.name}")

    elif channel.guild.id == 604945424922574848:#いろは鯖
        channel_dic_in_embed = await channel_dic_channel.fetch_message(682944796834398336)
        channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
        channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
        channel_dic_in_channel[channel.id] = new_channel.id
        channel_dic_in_channel = str(channel_dic_in_channel)
        channel_dic_record_embed = discord.Embed(title="いろは鯖",description=channel_dic_in_channel)

        iroha_server_log_guild = client1.get_guild(660445544296218650)
        new_channel = await iroha_server_log_guild.create_text_channel(name=channel.name)
        sagyousiji_channel = client1.get_channel(636359382359080961)
        await sagyousiji_channel.send(f"<@!523303776120209408>\n新しいチャンネル「{channel.name}」が{channel.guild.name}で作成されました。\n\
            辞書に追加してください。\n{channel.id}:{new_channel.id},#{channel.name}")

    else:
        channel_notice = client1.get_channel(682732694768975884)
        await channel_notice.send(f"{channel.guild.name}で<#{channel.id}>が作成されました。")

    try:
        await channel_dic_in_embed.edit(embed=channel_dic_record_embed)
    except UnboundLocalError:
        pass


@client1.event
async def on_message(message):
    try:
        if message.content == "/bot_stop":
            kei_ex_guild = client1.get_guild(585998962050203672)
            bot_stop_right_role = discord.utils.get(kei_ex_guild.roles, id=707570554462273537)
            if not bot_stop_right_role in message.author.roles:
                await message.channel.send("何様のつもり？")
                return
            await client1.close()
            now = datetime.datetime.now().strftime(r"%Y年%m月%d日　%H:%M")
            stop_msg = f"{message.author.mention}により{client1.user.name}が停止させられました"
            main_content = {
                "username": "BOT STOP",
                "avatar_url": "https://cdn.discordapp.com/attachments/644880761081561111/703088291066675261/warning.png",
                "content": "<@523303776120209408>",
                "embeds": [
                    {
                        "title": "botが停止させられました",
                        "description": stop_msg,
                        "color": 0xff0000,
                        "footer": {
                            "text": now
                        }
                    }
                ]
            }
            webhook_url = "https://discordapp.com/api/webhooks/704300492280561745/7bxBfj0T4RTx85l6rzACcuoNt0fqZayyA5cYQh4WTQQ53Q-HyTWNnZ2X_9pRS4RY3yc0"
            requests.post(webhook_url, json.dumps(main_content), headers={'Content-Type': 'application/json'}) #エラーメッセをウェブフックに投稿

        try:
            m = message.channel.send

            if message.author.name == "MEE6":
                await message.add_reaction("\U0001F595")    
            if message.author.id == 672910471279673358:
                await message.add_reaction("\U0001F595")

            if message.author != client1.user:#DM対処
                if message.channel == message.author.dm_channel:
                    channel = client1.get_channel(639830406270681099)
                    dm_embed = discord.Embed(description=message.content)
                    dm_embed.set_author(name=message.author.name+"\n"+str(message.author.id),icon_url=message.author.avatar_url)
                    await channel.send(embed=dm_embed)
                    return

                if message.channel.id == 639830406270681099:
                    str_user_id = message.content[0:18]
                    content = message.content[18:]
                    p = re.compile(r"^[0-9]+$")
                    if p.fullmatch(str_user_id):
                        user_id = int(message.content[0:18])
                        try:
                            member = client1.get_user(user_id)
                            dm = await member.create_dm()
                            await dm.send(content)
                        except AttributeError:
                            await m("そのユーザーは見つかりませんでした。")

            #try:
                if message.guild.id == 585998962050203672:#けいの実験サーバ
                    if not message.author.bot:
                        #日間発言数記録
                        nikkan_hatugensuu_logchannel = client1.get_channel(641511982805024768)
                        today = datetime.date.today()
                        flag = False
                        async for msg in nikkan_hatugensuu_logchannel.history(limit=1):
                            today_hatugensuu = await nikkan_hatugensuu_logchannel.fetch_message(msg.id)
                            if today_hatugensuu.content.startswith(str(today)):
                                hatugensuu = int(today_hatugensuu.content[11:])
                                hatugensuu = str(hatugensuu + 1)
                                await nikkan_hatugensuu_logchannel.send(str(today)+" "+hatugensuu)
                                try:
                                    await today_hatugensuu.delete()
                                    flag = True
                                    break
                                except discord.errors.NotFound:
                                    await m("<@!523303776120209408>\nbotの処理が追い付きませんでした。<#641511982805024768>を確認して下さい。")
                        if not flag:
                            await nikkan_hatugensuu_logchannel.send(str(today)+" 1")

                    await kei_ex_server.kei_ex_server(message,client1)#本体

                if message.guild.id == 624551872933527553:#処罰部

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

                if message.guild.id == 604945424922574848:#いろは鯖
                    await iroha.iroha(message,client1)

                if message.guild.id == 668743334109642752:
                    await kohga.kohga(message,client1,m)


                if message.guild.id == 659375053707673600:
                    if message.content.endswith("がなんか喋ろうとしてる！"):
                        await message.delete()

            #except AttributeError:
            #    await message.channel.send("エラー")
        except RuntimeError:
            pass
    except:
        unexpected_error()


@client2.event
async def on_message(message):
    if message.author.id == 159985870458322944:
        await message.add_reaction("\U0001F595")
    if message.author.id == 672910471279673358:
        await message.add_reaction("\U0001F595")


@client1.event
async def on_raw_reaction_add(payload):
    channel = client1.get_channel(payload.channel_id)
    user = client1.get_user(payload.user_id)
    kanryo_emoji = client1.get_emoji(636370115444867133)
    reactioned_emoji = client1.get_emoji(payload.emoji.id)#カスタム絵文字オンリー
    if channel.id == 636359382359080961:
        if user.id == 523303776120209408 or user.id == 582377618309906491:
            if reactioned_emoji == kanryo_emoji:
                msg = await channel.fetch_message(payload.message_id)
                if msg.embeds:
                    embed = discord.Embed(title="以下のメッセージを削除してよろしいですか？",description=msg.embeds[0].title,color=0x000000,timestamp=msg.created_at)
                    for field in range(len(msg.embeds[0].fields)):
                        embed.add_field(name=msg.embeds[0].fields[field].name,value=msg.embeds[0].fields[field].value)
                    embed.set_footer(text=f"{msg.embeds[0].author.name}-{msg.embeds[0].footer.text}",icon_url=msg.embeds[0].footer.icon_url)
                    kakunin_msg = await channel.send(embed=embed)
                else:
                    embed = discord.Embed(title="以下のメッセージを削除してよろしいですか？",description=msg.content,color=0x000000,timestamp=msg.created_at)
                    embed.set_footer(text=f"{msg.author.name}-{msg.guild.name}",icon_url=msg.author.avatar_url)
                    kakunin_msg = await channel.send(embed=embed)

                def check(mes):
                    return mes.author == user and mes.channel == channel and mes.content == "yes" or mes.content == "no"
                
                try:    
                    wait = await client1.wait_for("message",check=check,timeout=600)
                except asyncio.TimeoutError:
                    await channel.send("タイムアウトしました。")
                else:
                    if wait.content == "yes":
                        await msg.delete()
                    else:
                        pass
                    await wait.delete()

                await kakunin_msg.delete()


@tasks.loop(seconds=60)
async def loop():
    now = datetime.datetime.now().strftime("%H:%M")
    weekday = datetime.datetime.now().weekday()

    if now == "09:10":
        channel = client1.get_channel(597130965927723048)
        await channel.send("<@&673349311228280862>\nhttps://minecraft.jp/servers/54d3529e4ddda180780041a7/vote\nhttps://minecraftservers.org/server/575658")

    if now == "23:58":
        await kyoutuu.daily_ranking(client1)

    if weekday == 6:
        if now == "02:00":
            osirase_channel = client1.get_channel(585999375952642067)
            await osirase_channel.send("利子を付与します。")
            point_log_channel = client1.get_channel(663037579406606337)
            pt_dic_in_embed = await point_log_channel.fetch_message(679328510463967263)
            pt_log = pt_dic_in_embed.embeds[0].description
            pt_dic = ast.literal_eval(pt_log)

            for user_id in pt_dic:
                hoyuu_pt = pt_dic[user_id]
                if hoyuu_pt <= 128:
                    rishi = 1.2
                elif hoyuu_pt <= 576:
                    rishi = 1.1
                elif hoyuu_pt <= 1728:
                    rishi = 1.05
                elif hoyuu_pt <= 3456:
                    rishi = 1.01
                else:
                    rishi = 1
                after_pt = math.floor(hoyuu_pt*rishi)
                pt_dic[user_id] = after_pt
            pt_dic = str(pt_dic)
            pt_record_embed = discord.Embed(description=pt_dic)
            await pt_dic_in_embed.edit(embed=pt_record_embed)
            await osirase_channel.send("利子を付与しました")

        if now == "04:00":
            osirase_channel = client1.get_channel(585999375952642067)
            await osirase_channel.send("今週の当選発表を行います。")
            tousen_bangou = random.randint(0,999)
            str_tousen_bangou = str(tousen_bangou)
            if len(str_tousen_bangou) == 1:
                send = "00" + str_tousen_bangou
            if len(str_tousen_bangou) == 2:
                send = "0" + str_tousen_bangou
            if len(str_tousen_bangou) == 3:
                send = str_tousen_bangou
            await osirase_channel.send("今週の当選番号は**"+send+"**です")

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
            point_log_channel = client1.get_channel(663037579406606337)
            pt_dic_in_embed = await point_log_channel.fetch_message(679328510463967263)
            pt_log = pt_dic_in_embed.embeds[0].description
            pt_dic = ast.literal_eval(pt_log)
            async for msg in loto_kiroku_channel.history():
                str_userid_tyuusen_bangou = await loto_kiroku_channel.fetch_message(msg.id)
                int_userid_loto_channel = int(str_userid_tyuusen_bangou.content[0:18])
                str_tyuusen_bangou = str_userid_tyuusen_bangou.content[19:22]
                if str_tyuusen_bangou == send:#ピタリ賞なら
                    hoyuu_pt = pt_dic[int_userid_loto_channel]
                    after_pt = hoyuu_pt + 3456
                    pt_dic = str(pt_dic)
                    pt_record_embed = discord.Embed(description=pt_dic)
                    await pt_dic_in_embed.edit(embed=pt_record_embed)
                    try:
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await osirase_channel(f"{user_name}の所有pt:{hoyuu_pt}→{after_pt}")    
                    except AttributeError:
                        await osirase_channel(f"{int_userid_loto_channel}の所有pt:{hoyuu_pt}→{after_pt}")                

                elif str_tyuusen_bangou == atari_mae or str_tousen_bangou == atari_usiro:
                    hoyuu_pt = pt_dic[int_userid_loto_channel]
                    after_pt = hoyuu_pt + 1728
                    pt_dic = str(pt_dic)
                    pt_record_embed = discord.Embed(description=pt_dic)
                    await pt_dic_in_embed.edit(embed=pt_record_embed)
                    try:
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await osirase_channel(f"{user_name}の所有pt:{hoyuu_pt}→{after_pt}")    
                    except AttributeError:
                        await osirase_channel(f"{int_userid_loto_channel}の所有pt:{hoyuu_pt}→{after_pt}")     

                elif str_tyuusen_bangou.endswith(simoniketa_issyo):
                    hoyuu_pt = pt_dic[int_userid_loto_channel]
                    after_pt = hoyuu_pt + 64
                    pt_dic = str(pt_dic)
                    pt_record_embed = discord.Embed(description=pt_dic)
                    await pt_dic_in_embed.edit(embed=pt_record_embed)
                    try:
                        user_name = client1.get_user(int_userid_loto_channel).name
                        await osirase_channel(f"{user_name}の所有pt:{hoyuu_pt}→{after_pt}")    
                    except AttributeError:
                        await osirase_channel(f"{int_userid_loto_channel}の所有pt:{hoyuu_pt}→{after_pt}")     
                else:
                    pass
            await loto_kiroku_channel.purge()
            await osirase_channel.send("以上です")

        #しりとりリセット
        if now == "03:00":
            channel = client1.get_channel(603832801036468244)
            await channel.purge()
            start = message_list.siritori_start
            hajime = random.choice(start)
            await channel.send(hajime)

    if now == "00:00":
        hiduke = datetime.datetime.today()
        keikaniti = datetime.date.today().timetuple()[7] - 1
        syuuryouritu = str(keikaniti / 365 * 100)
        channel = client1.get_channel(597130965927723048)
        await channel.send("日付変更をお知らせします。今日の日付："+str(hiduke.year)+"年"+str(hiduke.month)+"月"+str(hiduke.day)+"日\n"+\
    str(hiduke.year)+"年の"+syuuryouritu+"%が終了しました。")

        zero_channel = client4.get_channel(656484919882547200)
        await zero_channel.send("日付変更をお知らせします。今日の日付："+str(hiduke.year)+"年"+str(hiduke.month)+"月"+str(hiduke.day)+"日")

        seichisaba_birthday = datetime.date(2020,6,29)
        atonannniti = str(seichisaba_birthday - datetime.date.today())
        atonannniti = atonannniti.replace(atonannniti[-13:],"")
        await channel.send("整地鯖4周年まであと"+atonannniti+"日です")

    #kohgaの依頼
    now_time = datetime.datetime.now()
    if now_time.day == 1 and now_time.hour == 0 and now_time.minute == 0:
        kohga_server = client1.get_guild(668743334109642752)
        house_member = discord.utils.get(kohga_server.roles,id=668743691040718858)#家の人
        payed_member = discord.utils.get(kohga_server.roles,id=668745683398033418)#支払い済み
        no_payed_member = discord.utils.get(kohga_server.roles,id=668745506817835028)#未払い
        for mem in house_member.members:
            await mem.remove_roles(payed_member)
            await mem.add_roles(no_payed_member)

    if now_time.hour == 0 and now_time.minute == 0:
        today_login_channel = client1.get_channel(682410834705907780)
        today_login_mcid_in_embed = await today_login_channel.fetch_message(682423757951991908)
        mcids = today_login_mcid_in_embed.embeds[0].description
        today_login_mcid_list = ast.literal_eval(mcids)
        today_login_mcid_list.clear()
        today_login_mcid_list = str(today_login_mcid_list)
        logined_mcid_embed = discord.Embed(description=today_login_mcid_list)
        await today_login_mcid_in_embed.edit(embed=logined_mcid_embed)

        series_login_record_channel = client1.get_channel(682732441479544918)
        today = datetime.date.today()
        ototoi = today - datetime.timedelta(days=2)
        async for msg in series_login_record_channel.history():
            today_uuid_days = await series_login_record_channel.fetch_message(msg.id)
            if today_uuid_days.content.startswith(f"{ototoi}"):
                await today_uuid_days.delete()
            else:
                pass

loop.start()


@tasks.loop(seconds=30)
async def change_status():
    await client1.wait_until_ready()
    presense_list = [
        "members",
        "channels",
        "guilds",
        "https://discord.gg/nrvMKBT",
        "某MEE6より優秀"
    ]
    presense = random.choice(presense_list)
    if presense == "members":
        l = []
        for guild in client1.guilds:
            for mem in guild.members:
                if not mem.id in l:
                    l.append(mem.id)
        presense = f"{len(l)}人を監視中"

    if presense == "channels":
        i = 0
        for guild in client1.guilds:
            for ch in guild.channels:
                i += 1
        presense = f"{i}チャンネルを監視中"

    if presense == "guilds":
        presense = f"{len(client1.guilds)}サーバを監視中"

    game = discord.Game(presense)
    await client1.change_presence(status=discord.Status.online, activity=game)
    
change_status.start()


#以下ログインと接続に必要、触るな
Entry = namedtuple("Entry", "client event token")
entries = [
    Entry(client=client1,event=asyncio.Event(),token=discord_bot_token_1),
    Entry(client=client2,event=asyncio.Event(),token=discord_bot_token_2),
    Entry(client=client4,event=asyncio.Event(),token=discord_bot_token_4)
]  

async def login():
    for e in entries:
        await e.client.login(e.token)

async def wrapped_connect(entry):
    try:
        await entry.client.connect()
    except Exception as e:
        await entry.client.close()
        print("We got an exception: ", e.__class__.__name__, e)
        entry.event.set()

async def check_close():
    futures = [e.event.wait() for e in entries]
    await asyncio.wait(futures)

loop = asyncio.get_event_loop()
loop.run_until_complete(login())
for entry in entries:
    loop.create_task(wrapped_connect(entry))
loop.run_until_complete(check_close())
loop.close()
