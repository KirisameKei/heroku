import discord,random,re,datetime,json,time,math,os,asyncio,requests,bs4,ast,sys,traceback
import urllib.request
from collections import namedtuple
from datetime import date
from discord.ext import tasks
from discord import Embed#ここまでモジュールのインポート

from quote import expand#メッセージリンク展開用
import quote

try:
    import tokens
except ModuleNotFoundError:
    pass

import server_log,kyoutuu,kei_ex_server,muhou,iroha#on_message関数の使用に必要(メッセージサーバごとに処理を分ける)
import channel_dic,my_guild_role_dic,message_list,ban_list#このbotを動かすのに必要な辞書とリスト


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
            made_time = member.created_at
            made_time_msg = f"{member.name}さんは{made_time.year}年{made_time.month}月{made_time.day}日"
            made_time_msg += f"{made_time.hour}時{made_time.minute}分{made_time.second}秒からdiscordを使用しています。"
            await sanka_dattai_channel.send(made_time_msg)

    elif member.guild.id == 587909823665012757:#無法地帯なら
        if member.id in ban_list.ban_list:
            await member.guild.kick()
        else:
            await sanka_dattai_channel.send(member.name+"が無法地帯に参加しました。")

    elif member.guild.id == 624551872933527553:#処罰部なら
        await sanka_dattai_channel.send(member.name+"がHJKに参加しました。")

    else:
        await sanka_dattai_channel.send(member.name+"さんが"+member.guild.name+"に参加しました。")


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
    if channel.guild.id == 585998962050203672:#けいの実験サーバ
        make_guild = client1.get_guild(647311568454811649)
        new_channel = await make_guild.create_text_channel(name=channel.name)
        sagyousiji_channel = client1.get_channel(636359382359080961)
        await sagyousiji_channel.send("<@!523303776120209408>\n\
新しいチャンネル、「"+channel.name+"」がけいの実験サーバに作成されました。\n辞書に追加してください。\n"+\
    str(channel.id)+"\n"+str(new_channel.id))

    if channel.guild.id == 624551872933527553:#処罰部
        make_guild = client1.get_guild(633328124968435712)#やることリスト
        new_channel = await make_guild.create_text_channel(name=channel.name)
        sagyousiji_channel = client1.get_channel(638904268543361037)#作業指示書
        await sagyousiji_channel.send("<@!523303776120209408>\n\
新しいチャンネル、「"+channel.name+"」が作成されました。辞書に追加してください。\n"+str(channel.id)+"\n"+str(new_channel.id))

    if channel.guild.id == 604945424922574848:#いろは鯖
        make_guild = client1.get_guild(660445544296218650)
        new_channel = await guild.create_text_channel(name=channel.name)
        sagyousiji_channel = client1.get_channel(636359382359080961)
        await sagyousiji_channel.send("<@!523303776120209408>\n\
新しいチャンネル、「"+channel.name+"」がいろは鯖に作成されました。\n辞書に追加してください。\n"+\
    str(channel.id)+"\n"+str(new_channel.id))

    itijihinan_channel1 = client1.get_channel(663037579406606337)
    itijihinan_channel2 = client1.get_channel(663037675141595147)
    flag1 = False
    async for msg in itijihinan_channel1.history(limit=1):
        mitouroku_channel1 = await itijihinan_channel1.fetch_message(msg.id)
        await itijihinan_channel1.send(mitouroku_channel1.connect+" "+str(channel.id))
        flag1 = True
    if not flag1:
        await itijihinan_channel1.send(str(channel.id))
    flag2 = False
    async for msg in itijihinan_channel2.history(limit=1):
        mitouroku_channel2 = await itijihinan_channel2.fetch_message(msg.id)
        await itijihinan_channel2.send(mitouroku_channel2.content+" "+str(new_channel.id))
        flag2 = True
    if not flag2:
        await itijihinan_channel2.send(str(new_channel.id))


@client1.event
async def on_guild_channel_update(before,after):
    itijihinan_channel1 = client1.get_channel(663037579406606337)
    itijihinan_channel2 = client1.get_channel(663037675141595147)
    if before.guild.id == 585998962050203672:#けいの実験サーバ
        try:
            new_name_channel = channel_dic.my_guild_log_dic[before.id]
            new_name_channel = client1.get_channel(new_name_channel)
        except KeyError:
            async for msg in itijihinan_channel1.history(limit=1):
                mitouroku_channel1 = await itijihinan_channel1.fetch_message(msg.id)
                async for msg in itijihinan_channel2.history(limit=1):
                    mitouroku_channel2 = await itijihinan_channel2.fetch_message(msg.id)
                mitouroku_channel_list1 = mitouroku_channel1.content.split()
                mitouroku_channel_list2 = mitouroku_channel2.content.split()
                i = mitouroku_channel_list1.index(before.id)
                new_name_channel = client1.get_channel(mitouroku_channel_list2[i])
        await new_name_channel.edit(name=after.name,position=after.position)

    if before.guild.id == 624551872933527553:#処罰部
        try:
            new_name_channel = channel_dic.syobatubu_log_dic[before.id]
            new_name_channel = client1.get_channel(new_name_channel)
        except KeyError:
            async for msg in itijihinan_channel1.history(limit=1):
                mitouroku_channel1 = await itijihinan_channel1.fetch_message(msg.id)
                async for msg in itijihinan_channel2.history(limit=1):
                    mitouroku_channel2 = await itijihinan_channel2.fetch_message(msg.id)
                mitouroku_channel_list1 = mitouroku_channel1.content.split()
                mitouroku_channel_list2 = mitouroku_channel2.content.split()
                i = mitouroku_channel_list1.index(before.id)
                new_name_channel = client1.get_channel(mitouroku_channel_list2[i])
        await new_name_channel.edit(name=after.name,position=after.position)

    if before.guild.id == 604945424922574848:#いろは鯖
        try:
            new_name_channel = channel_dic.iroha_server_log_dic[before.id]
            new_name_channel = client1.get_channel(new_name_channel)
            await new_name_channel.edit(name=after.name,position=after.position)
        except KeyError:
            sagyousiji_channel = client1.get_channel(636359382359080961)#作業指示書
            await sagyousiji_channel.send("<@!523303776120209408>\nおいゴルァ！"+before.channel.mention+"の辞書登録あく！")


@client1.event
async def on_guild_channel_delete(channel):
    msg = channel.name+"が削除されました"
    if channel.guild.id == 585998962050203672:#けいの実験サーバ
        sagyousiji_channel = client1.get_channel(636359382359080961)#やることリスト
        await sagyousiji_channel.send(msg)
    if channel.guild.id == 624551872933527553:#処罰部
        sagyousiji_channel = client1.get_channel(638904268543361037)#作業指示書
        await sagyousiji_channel.send(msg)
    if channel.guild.id == 604945424922574848:#いろは鯖
        sagyousiji_channel = client1.get_channel(636359382359080961)#やることリスト
        await sagyousiji_channel.send(msg)


@client1.event
async def on_message(message):
    try:
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

        try:
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

                if not message.author.bot:
                    kojin_hatugensuu_logchannel = client1.get_channel(641264504696602656)
                    level_up_channel = client1.get_channel(641274239110086666)
                    flag = False
                    async for msg in kojin_hatugensuu_logchannel.history():
                        str_userid_hatugensuu = await kojin_hatugensuu_logchannel.fetch_message(msg.id)
                        if str_userid_hatugensuu.content[0:18] == str(message.author.id):
                            int_hatugensuu = int(str_userid_hatugensuu.content[19:])
                            int_after_hatugensuu = int_hatugensuu + 1
                            str_after_hatugensuu = str(int_after_hatugensuu)
                            await kojin_hatugensuu_logchannel.send(str(message.author.id)+" "+str_after_hatugensuu)
                            try:
                                await str_userid_hatugensuu.delete()
                                level = math.sqrt(int_after_hatugensuu)
                                if level % 1 == 0:
                                    level = math.floor(level)
                                    level_up_message = await level_up_channel.send(message.author.mention+"\nﾑﾑｯwwwwwwwﾚﾍﾞﾙｱｯﾌ゜wwwwwww【Lv"+str(level - 1)+"→Lv"+str(level)+"】")
                                    await level_up_message.add_reaction("\U0001F595")
                                flag = True
                                break
                            except discord.errors.NotFound:
                                await message.channel.send(message.author.mention+"連投のしすぎです！気をつけてください！")
                                flag = True
                                break
                    if not flag:
                        await kojin_hatugensuu_logchannel.send(str(message.author.id)+" 1")
                        level_up_message = await level_up_channel.send(message.author.mention+"\nﾑﾑｯwwwwwwwﾚﾍﾞﾙｱｯﾌ゜wwwwwww【Lv1】")
                        await level_up_message.add_reaction("\U0001F595")

                await server_log.kei_ex_server_log(message,client1)#ログ
                await kei_ex_server.kei_ex_server(message,client1)#本体

            if message.guild.id == 624551872933527553:#処罰部
                await server_log.syobatubu_server_log(message,client1)#ログ

            if message.guild.id == 587909823665012757:#無法地帯
                await muhou.muhou(message)

            if message.guild.id == 604945424922574848:#いろは鯖
                await server_log.iroha_server_log(message,client1)
                await iroha.iroha(message,client1)

        except AttributeError:
            pass
    
    except:#エラーを表示！！------------
        error_msg = "```\n" + traceback.format_exc() + "\n```" +"(" + str(time) + ")"
        error_ch = client1.get_channel(597978849476870153)#エラー用のチャンネル

        if isinstance(message.channel, discord.DMChannel):
            await error_ch.send(ni_men + "dmでエラーが発生しました")
            await message.channel.send("エラーが発生しました")
        else:
            await m("<@!523303776120209408>\nエラーが発生しました<#597978849476870153>")
        embed = discord.Embed(title='Error_log', description=error_msg, color=0xf04747)
        embed.set_footer(text=f'channel:{message.channel}\ntime:{time}')
        await error_ch.send(embed=embed)


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
            await m("昨日の発言数："+str(kinou_hatugensuu))
            await m("前日比："+send)

            guild = client4.get_guild(626739606674735134)
            user_count = len(guild.members)
            today = datetime.date.today()
            user_log_channel = client4.get_channel(656486784330629140)
            await user_log_channel.send(str(today)+" "+str(user_count))

            user_count_channel = client4.get_channel(656486784330629140)
            async for msg in user_count_channel.history(limit=2):
                today = datetime.date.today()
                kyou = str(today - datetime.timedelta(days=1))
                kinou = str(today - datetime.timedelta(days=2))
                kyou_kinou_user = await user_count_channel.fetch_message(msg.id)
                if kyou_kinou_user.content.startswith(kyou):
                    kyou_user = int(kyou_kinou_user.content[11:])
                if kyou_kinou_user.content.startswith(kinou):
                    kinou_user = int(kyou_kinou_user.content[11:])
                ninzuu_zougen = kinou_user - kyou_user
                if ninzuu_zougen > 0:
                    send = "+"+str(ninzuu_zougen)
                else:
                    send = str(ninzuu_zougen)
                await m("今のユーザー数："+str(kyou_user))
                await m("前日比："+send)


@tasks.loop(seconds=60)
async def loop():
    now = datetime.datetime.now().strftime("%H:%M")
    weekday = datetime.datetime.now().weekday()

    if now == "09:10":
        channel = client1.get_channel(597130965927723048)
        await channel.send("<@!523303776120209408>\nhttps://minecraft.jp/servers/54d3529e4ddda180780041a7")

    if weekday == 6:
        if now == "02:00":
            channel = client1.get_channel(585999375952642067)
            await channel.send("利子を付与します")
        if now == "03:00":
            channel = client1.get_channel(603832801036468244)
            await channel.purge()
            start = message_list.siritori_start
            hajime = random.choice(start)
            await channel.send(hajime)
        if now == "04:00":
            channel = client1.get_channel(585999375952642067)
            await channel.send("今週の当選発表を行います")

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
