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

import server_log,kyoutuu,kei_ex_server,muhou,iroha#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト

import kohga#依頼

client1 = discord.Client()#魔理沙bot(メインで使用)
client2 = discord.Client()#小傘bot(VC関連用)
client4 = discord.Client()#零bot


@client1.event
async def on_ready():
    print(client1.user.name+"がログインしました")
    login_channel = client1.get_channel(595072269483638785)
    await login_channel.send(client1.user.name+"がログインしました")
    await client1.change_presence(activity = discord.Game(name = "少なくとも某MEE6よりは優秀"))


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
async def on_guild_channel_update(before,after):
    channel_dic_channel = client1.get_channel(663037675141595147)
    parameter = True
    if before.guild.id == 585998962050203672:#けいの実験サーバ
        try:
            new_name_channel_id = channel_dic.my_guild_log_dic[before.id]#ログ鯖の対応するチャンネルID
            new_name_channel = client1.get_channel(new_name_channel_id)#ログ鯖の対応するチャンネル
        except KeyError:
            channel_dic_in_embed = await channel_dic_channel.fetch_message(682935760512352274)
            channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
            channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
            new_name_channel_id = channel_dic_in_channel[before.id]#ログ鯖の対応するチャンネルID
            new_name_channel = client1.get_channel(new_name_channel_id)#ログ鯖の対応するチャンネルID
        await new_name_channel.edit(name=after.name,position=after.position)

    elif before.guild.id == 624551872933527553:#処罰部
        parameter = False
        try:
            new_name_channel = channel_dic.syobatubu_log_dic[before.id]
            new_name_channel = client1.get_channel(new_name_channel)
        except KeyError:
            channel_dic_in_embed = await channel_dic_channel.fetch_message(682944795794079767)
            channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
            channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
            new_name_channel_id = channel_dic_in_channel[before.id]#ログ鯖の対応するチャンネルID
            new_name_channel = client1.get_channel(new_name_channel_id)#ログ鯖の対応するチャンネルID
        await new_name_channel.edit(name=after.name,position=after.position)

    elif before.guild.id == 604945424922574848:#いろは鯖
        try:
            new_name_channel = channel_dic.iroha_server_log_dic[before.id]
            new_name_channel = client1.get_channel(new_name_channel)
            await new_name_channel.edit(name=after.name,position=after.position)
        except KeyError:
            pass
            """
            channel_dic_in_embed = await channel_dic_channel.fetch_message(682944796834398336)
            channel_dic_in_channel = channel_dic_in_embed.embeds[0].description
            channel_dic_in_channel = ast.literal_eval(channel_dic_in_channel)#辞書完成
            new_name_channel_id = channel_dic_in_channel[before.id]#ログ鯖の対応するチャンネルID
            new_name_channel = client1.get_channel(new_name_channel_id)#ログ鯖の対応するチャンネルID
        await new_name_channel.edit(name=after.name,position=after.position)"""

    if parameter:
        if before.name != after.name:
            channel_notice = client1.get_channel(682732694768975884)
            await channel_notice.send(f"{before.guild.name}の{before.name}が{after.name}に変わりました。")



@client1.event
async def on_guild_channel_delete(channel):
    msg = f"{channel.guild.name}で{channel.name}が削除されました"
    if channel.guild.id == 624551872933527553:#処罰部
        sagyousiji_channel = client1.get_channel(638904268543361037)#作業指示書
        await sagyousiji_channel.send(msg)
    else:
        channel_notice = client1.get_channel(682732694768975884)
        await channel_notice.send(msg)


@client1.event
async def on_message(message):
    m = message.channel.send
    
    await kyoutuu.kanzen_kyoutuu_message_link(message,client1,client4)#リンク展開

    if message.author.name == "MEE6":
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

            await server_log.kei_ex_server_log(message,client1)#ログ
            await kei_ex_server.kei_ex_server(message,client1)#本体

        if message.guild.id == 624551872933527553:#処罰部
            await server_log.syobatubu_server_log(message,client1)#ログ

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

        if message.guild.id == 587909823665012757:#無法地帯
            await muhou.muhou(message)

        if message.guild.id == 604945424922574848:#いろは鯖
            await server_log.iroha_server_log(message,client1)
            await iroha.iroha(message,client1)

        if message.guild.id == 668743334109642752:
            await kohga.kohga(message,client1,m)


        if message.guild.id == 659375053707673600:
            if message.content.endswith("がなんか喋ろうとしてる！"):
                await message.delete()

    #except AttributeError:
    #    await message.channel.send("エラー")


@client1.event
async def on_message_edit(before,after):
    now = datetime.datetime.now().strftime("%H:%M")
    embed = discord.Embed(description="編集前\n"+before.content+"\n\n編集後\n"+after.content,color=0x0000ff)
    embed.set_author(name=before.author.name,icon_url=before.author.avatar_url)
    embed.set_footer(text=now)
    if before.guild.id == 585998962050203672:#けいの実験サーバ
        try:
            write_channel = channel_dic.my_guild_log_dic[before.channel.id]
            write_channel = client1.get_channel(write_channel)
            await write_channel.send(embed=embed)
        except KeyError:
            sagyousiji_channel = client1.get_channel(636359382359080961)#やることリスト
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+before.channel.mention+"の辞書登録あく！")

    if before.guild.id == 624551872933527553:#処罰部
        try:
            write_channel = channel_dic.syobatubu_log_dic[before.channel.id]
            write_channel = client1.get_channel(write_channel)
            await write_channel.send(embed=embed)
        except KeyError:
            sagyousiji_channel = client1.get_channel(638904268543361037)#作業指示書
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+before.channel.mention+"の辞書登録あく！")

    if before.guild.id == 604945424922574848:#いろは鯖
        try:
            write_channel = channel_dic.iroha_server_log_dic[before.channel.id]
            write_channel = client1.get_channel(write_channel)
            await write_channel.send(embed=embed)
        except KeyError:
            sagyousiji_channel = client1.get_channel(636359382359080961)#やることリスト
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+before.channel.mention+"の辞書登録あく！")


@client1.event
async def on_message_delete(message):
    now = datetime.datetime.now().strftime("%H:%M")
    embed = discord.Embed(description="削除されたメッセージ\n"+message.content,color=0xff0000)
    embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
    embed.set_footer(text=now)
    if message.guild.id == 585998962050203672:#けいの実験サーバ
        try:
            write_channel = channel_dic.my_guild_log_dic[message.channel.id]
            write_channel = client1.get_channel(write_channel)
            await write_channel.send(embed=embed)
        except KeyError:
            sagyousiji_channel = client1.get_channel(636359382359080961)#やることリスト
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+message.channel.mention+"の辞書登録あく！")

    if message.guild.id == 624551872933527553:#処罰部
        try:
            write_channel = channel_dic.syobatubu_log_dic[message.channel.id]
            write_channel = client1.get_channel(write_channel)
            await write_channel.send(embed=embed)
        except KeyError:
            sagyousiji_channel = client1.get_channel(638904268543361037)#作業指示書
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+message.channel.mention+"の辞書登録あく！")

    if message.guild.id == 604945424922574848:#いろは鯖
        try:
            write_channel = channel_dic.iroha_server_log_dic[message.channel.id]
            write_channel = client1.get_channel(write_channel)
            await write_channel.send(embed=embed)
        except KeyError:
            sagyousiji_channel = client1.get_channel(636359382359080961)#やることリスト
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+message.channel.mention+"の辞書登録あく！")


@client2.event
async def on_message(message):
    if message.author.id == 159985870458322944:
        await message.add_reaction("\U0001F595")


@client4.event
async def on_message(message):
    m = message.channel.send

    if message.content == "/new_func":
        start_msg = "```\n機能追加の申請をします。\n各項目は全て1回の送信で書いてください。\n\
各項目は10分でタイムアウトします。\n備考などがない場合はなしと入力してください。\n\
複雑な場合はけいまたはdisneyresidentsに直接言っていただいても構いません。```"
        msg_list = [
            "この依頼内容を公開してよろしいですか？\n良い場合はyes、悪い場合はnoと入力してください\n\
__**特殊な理由がない限りyesにしてください。**__(noの場合けいのDMに送られるためログが埋もれて忘れ去られる可能性があります。)",
            "何をしたら？\n例：/seichiと入力したら、16時になったら等",
            "何をする？\n例：整地鯖役職を付与する、チャンネルにあるメッセージをすべて消去する等",
            "チャンネル、役職の指定は？\n例：Hypixl役職持ちが実行すると怒られる、<#665937884662202434>を消す等",
            "その他備考は？\n他に要求がある場合ここに書いてください。",
        ]
        reply_list = []
        send_msg_list = []

        def check1(m):#公開設定
            return m.author == message.author and m.channel == message.channel and m.content == "yes" or m.content == "no"
        def check2(m):#何をしたら？
            return m.author == message.author and m.channel == message.channel
        def check3(m):#何をする？
            return m.author == message.author and m.channel == message.channel
        def check4(m):#チャンネルや役職の指定は？
            return m.author == message.author and m.channel == message.channel
        def check5(m):#備考は？
            return m.author == message.author and m.channel == message.channel
        def check6(m):#これでいいですか？
            return m.author == message.author and m.channel == message.channel and m.content == "yes" or m.content == "no"

        check_list = [
            check1,
            check2,
            check3,
            check4,
            check5,
        ]

        flag = False
        start = await m(start_msg)
        msg = await m(msg_list[0])
        send_msg_list.append(msg)
        for i in range(len(msg_list)):
            try:
                reply = await client4.wait_for("message",check=check_list[i],timeout=600)
                reply_list.append(reply)
            except asyncio.TimeoutError:
                await m("タイムアウトしました。最初からやり直してください。")
                await start.delete()
                for j in range(i+1):
                    await send_msg_list[j].delete()
                    try:
                        await reply_list[j].delete()
                    except IndexError:
                        pass
                break
            else:
                try:
                    send_msg = await m(msg_list[i+1])
                    send_msg_list.append(send_msg)
                except IndexError:
                    flag = True
                
        if flag:
            embed = discord.Embed(title="これで申請してよろしいですか？",description="良ければyes、やり直すならnoと入力してください",color=0xfffffe)
            embed.add_field(name="やりたいこと",value=f"{reply_list[1].content}{reply_list[2].content}",inline=False)
            embed.add_field(name="条件の指定",value=reply_list[3].content)
            embed.add_field(name="備考",value=reply_list[4].content)
            if reply_list[0].content == "yes":
                koukai_hikoukai = "公開"
            else:
                koukai_hikoukai = "非公開"
            embed.add_field(name="公開設定",value=koukai_hikoukai,inline=False)
            await start.delete()
            for j in range(5):
                await send_msg_list[j].delete()
                await reply_list[j].delete()
            kakunin = await m(embed=embed)
            try:
                reply = await client4.wait_for("message",check=check6,timeout=600)
            except asyncio.TimeoutError:
                await m("タイムアウトしました。最初からやり直してください。")
                await kakunin.delete()
            else:
                if reply.content == "yes":
                    embed = discord.Embed(title="依頼が届きました",color=0x00ff00)
                    embed.add_field(name="やりたいこと",value=f"{reply_list[1].content}{reply_list[2].content}",inline=False)
                    embed.add_field(name="条件の指定",value=reply_list[3].content)
                    embed.add_field(name="備考",value=reply_list[4].content)
                    embed.set_author(name=message.author.name,icon_url=message.author.avatar_url)
                    embed.set_footer(text=message.guild.name,icon_url=message.guild.icon_url)
                    if reply_list[0].content == "no":#非公開なら
                        dm = await client4.get_user(523303776120209408).create_dm()
                        await reply.delete()
                        await dm.send(embed=embed)
                        await m("依頼内容をけいのDMに送信しました。回答をお待ちください。\n疑問点がある、情報が不十分等の理由でDMを送らせていただく場合があります。")
                    else:
                        guild_name = message.guild.name
                        await reply.delete()
                        await rem_to_marichan(client1,embed,guild_name)
                        await m("依頼内容をけいの実験サーバ「python開発やることリスト」に送信しました。回答をお待ちください。\n\
疑問点がある、情報が不十分等の理由でメンションやDMをさせていただく場合があります。")

                else:
                    await m("最初からやり直してください。")
                    await kakunin.delete()
                    await reply.delete()

    if not message.author.bot:
        #日間発言数記録
        if not message.guild.id == 626739606674735134:
            return
        nikkan_hatugensuu_logchannel = client4.get_channel(643078487359619082)
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
                    await m("<@!523303776120209408>\nbotの処理が追い付きませんでした。<#643078487359619082>を確認して下さい。")
        if not flag:
            await nikkan_hatugensuu_logchannel.send(str(today)+" 1")

    #日間発言数発表
    if message.author == client4.user:
        if message.content.startswith("日付変更をお知らせします。"):
            today = datetime.date.today()
            kinou = str(today - datetime.timedelta(days=1))
            ototoi = str(today - datetime.timedelta(days=2))
            nikkan_hatugensuu_logchannel = client4.get_channel(643078487359619082)
            async for msg in nikkan_hatugensuu_logchannel.history(limit=3):
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
            await m("昨日の発言数："+str(kinou_hatugensuu))
            await m("前日比："+send)

            guild = client4.get_guild(626739606674735134)
            user_count = len(guild.members)
            today = datetime.date.today()
            user_log_channel = client4.get_channel(656486784330629140)
            await user_log_channel.send(str(today)+" "+str(user_count))

            user_count_channel = client4.get_channel(656486784330629140)
            kirokunaiyou_list = []
            async for msg in user_count_channel.history(limit=2):
                kyou_kinou_user = await user_count_channel.fetch_message(msg.id)
                kirokunaiyou_list.append(kyou_kinou_user.content)
                
            kyou_user = kirokunaiyou_list[0]
            kinou_user = kirokunaiyou_list[1]
                
            kinou_user = int(kirokunaiyou_list[1][11:])
            kyou_user = int(kirokunaiyou_list[0][11:])

            ninzuu_zougen = kyou_user - kinou_user
            if ninzuu_zougen > 0:
                send = "+"+str(ninzuu_zougen)
            else:
                send = str(ninzuu_zougen)
            await m("今のユーザー数："+str(kyou_user))
            await m("前日比："+send)


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
    if channel.id == 659774769746673676:
        if payload.message_id == 678223516436529154:
            kei_3104 = client1.get_emoji(653433434185662485)
            if reactioned_emoji == kei_3104:
                ch = client1.get_channel(605029247962185738)
                await ch.send(f"{user.mention}がDJ役職を申請しています。")

    if channel.id == 664286990677573680:
        if payload.message_id == 681797627330691141:
            if user == client1.user:
                return
            msg = await channel.fetch_message(payload.message_id)
            abcdefg = ["\U0001f1e6","\U0001f1e7","\U0001f1e8","\U0001f1e9","\U0001f1ea","\U0001f1eb","\U0001f1ec"]
            free_roles = [586123363513008139,586123567146729475,678445373324263454,678445640027734032,678445821603217448,606481478078955530,673349311228280862]
            if payload.emoji.name in abcdefg:
                abcdefg_index = abcdefg.index(payload.emoji.name)
                guild = client1.get_guild(585998962050203672)
                member = guild.get_member(payload.user_id)
                role = discord.utils.get(guild.roles,id=free_roles[abcdefg_index])
                if discord.utils.get(member.roles,id=free_roles[abcdefg_index]):
                    await member.remove_roles(role)
                    system_message = await channel.send(f"{user.mention}から{role.name}を剥奪しました。")
                else:
                    await member.add_roles(role)
                    system_message = await channel.send(f"{user.mention}に{role.name}を付与しました。")
            else:
                await msg.clear_reactions()
                system_message = await channel.send(f"{user.mention}その絵文字は使用できません。")

            await msg.clear_reactions()
            for i in range(7):
                await msg.add_reaction(abcdefg[i])
            await asyncio.sleep(3)
            await system_message.delete()


async def rem_to_marichan(client1,embed,guild_name):
    yarukoto_ch = client1.get_channel(636359382359080961)
    await yarukoto_ch.send(f"<@!523303776120209408>{guild_name}の零botについての依頼です。\n",embed=embed)


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

    if now_time.month == 5 and now_time.day == 6 and now_time.hour == 22 and now_time.minute == 0:
        await kei_ex_server.kikaku_choice(client1)
        
    #──────────ここから──────────
    if now_time.minute == 3:
        await kyoutuu.daily_ranking(client1)
 
        notice_ch = client1.get_channel(597978849476870153)
        await notice_ch.send(f"───────{datetime.datetime.now()}───────")
        i = 0
        flag = False
        while True:
            url = f"https://w4.minecraftserver.jp/api/ranking?type=break&offset={i*20}&lim=20&duration=daily"
            try:
                res = requests.get(url)
                res.raise_for_status()
                player_data_dict = ast.literal_eval(str(bs4.BeautifulSoup(res.text, "html.parser")))
                player_data_list = player_data_dict["ranks"]
                for player_data in player_data_list:
                    mcid = player_data["player"]["name"]
                    raw_data = player_data["data"]["raw_data"]
                    await notice_ch.send(f"{mcid} : {raw_data}")
                    if int(raw_data) < 10000000:
                        flag = True
                        break
                    else:
                        i += 1
                if flag:
                    await notice_ch.send("───────キリトリ───────")
                    break

            except requests.exceptions.HTTPError:
                await notice_ch.send("この機能は現在ご利用いただけません")
                break
        #───────────ここまで──────────


loop.start()


#以下ログインと接続に必要、触るな

try:
    TOKEN1 = tokens.discord_bot_1
    TOKEN2 = tokens.discord_bot_2
    TOKEN4 = tokens.zero_bot

except NameError:
    TOKEN1 = os.getenv("discord_bot_token_1")
    TOKEN2 = os.getenv("discord_bot_token_2")
    TOKEN4 = os.getenv("zero_bot_token")


Entry = namedtuple("Entry", "client event token")
entries = [
    Entry(client=client1,event=asyncio.Event(),token=TOKEN1),
    Entry(client=client2,event=asyncio.Event(),token=TOKEN2),
    Entry(client=client4,event=asyncio.Event(),token=TOKEN4)
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
