import asyncio
import datetime
import io
import os
import random

import discord
import requests
import twitter

import commands

async def on_message(client1, message):
    """
    けい鯖にメッセージが投稿された時用の関数"""

    if message.content == "/test_member":
        test_member_role = discord.utils.get(message.guild.roles, id=586009049259311105) #実験台役職
        await message.author.add_roles(test_member_role)

    if message.content == "/not test_member":
        test_member_role = discord.utils.get(message.guild.roles, id=586009049259311105) #実験台役職
        await message.author.remove_roles(test_member_role)

    if message.channel.id == 702904669860659260:
        await twitter_connection(message)

    if message.content.startswith("/hide "):
        await hide_member(message)

    if message.content.startswith("/find "):
        await find_member(message)

    if message.content.startswith("/info "):
        await commands.info(client1, message)

    if message.content.startswith("/last_login "):
        await commands.last_login(message)

    if message.content.startswith("/weather "):
        await commands.weather(message)

    if message.content.startswith("/name "):
        await commands.random_name(message)

    if message.content.startswith("/break "):
        await commands.seichi_break(message)

    if message.content.startswith("/delmsg"):
        await delmsg(message)

    if message.content.startswith("/vote"):
        await commands.vote(message)

    if message.content.startswith("/mcavatar "):
        await commands.mcavatar(client1, message)

    if message.channel.id == 603832801036468244:
        await shiritori(message)

    if message.channel.id == 639830406270681099:
        await dm_send(client1, message)


async def on_raw_reaction_add(client1, payload):
    """
    リアクションが付けられた時用の関数"""

    channel = client1.get_channel(payload.channel_id)
    user = client1.get_user(payload.user_id)
    guild = client1.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if channel.id == 664286990677573680:
        if not payload.message_id == 708518613702803527:
            return
        if user == client1.user:
            return
        msg = await channel.fetch_message(payload.message_id)
        await msg.remove_reaction(f"{payload.emoji}", user)
        emoji_list = [
            "\U0001f1e6",
            "\U0001f1e7",
            "\U0001f1e8",
            "\U0001f1e9",
            "\U0001f1ea",
            "\U0001f1eb",
            "\U0001f1ec"
        ]
        role_id_list = [
            586123363513008139,
            586123567146729475,
            678445373324263454,
            678445640027734032,
            678445821603217448,
            606481478078955530,
            673349311228280862
        ]
        if payload.emoji.name in emoji_list:
            emoji_index = emoji_list.index(payload.emoji.name)
            role = discord.utils.get(guild.roles, id=role_id_list[emoji_index])
            if role in member.roles:
                await member.remove_roles(role)
                system_message = await channel.send(f"{member.mention}から{role.name}を剥奪しました")
            else:
                await member.add_roles(role)
                system_message = await channel.send(f"{member.mention}に{role.name}を付与しました")

        else:
            system_message = await channel.send(f"{member.mention}その絵文字は使用できません")

        await asyncio.sleep(3)
        await system_message.delete()


async def hide_member(message):
    """
    かくれんぼなう役職を付与する関数"""

    hide_role = discord.utils.get(message.guild.roles, id=616790954200006717)
    if message.content == "/hide me":
        if hide_role in message.author.roles:
            await message.channel.send("もう隠れているようです。私には見つけられませんでした。")
            return
        await message.author.add_roles(hide_role)
        await message.channel.send(f"{message.author.name}が隠れました。もーいーよ")
    else:
        try:
            user_id = int(message.content.split())
        except ValueError:
            await message.channel.send("不正なIDです")
            return

        member = message.guild.get_member(user_id)
        try:
            if hide_role in member.roles:
                await message.channel.send(f"{member.name}はもう隠れているようです。私には見つけられませんでした。")
                return
            admin_role = discord.utils.get(message.guild.roles, id=585999549055631408)
            if admin_role in member.roles:
                await message.channel.send("管理者を隠そうとは・・・さてはこの鯖を乗っ取る気だなおめー")
                return
            await member.add_roles(hide_role)
            await message.channel.send(f"{member.name}が隠れました。もーいーよ")
        except AttributeError:
            await message.channel.send("そのユーザーIDの人はこのサーバにはいません")


async def find_member(message):
    """
    かくれんぼなう役職を剥奪する関数"""

    hide_role = discord.utils.get(message.guild.roles, id=616790954200006717)
    if message.content == "/find me":
        if not (hide_role in message.author.roles):
            await message.channel.send("もう見つけてるよ・・・？")
            return
        await message.author.remove_roles(hide_role)
        await message.channel.send(f"{message.author.name}、見～っけ！")
        member = message.guild.get_member(user_id)
    else:
        try:
            user_id = int(message.content.split())
        except ValueError:
            await message.channel.send("不正なIDです")
            return


async def delmsg(message):
    """
    管理者持ちが実行したら実行チャンネルのメッセージを削除する
    管理者なしが実行したら怒ってドM役職を付ける"""

    admin_role = discord.utils.get(message.guild.roles, id=585999549055631408)
    if not (admin_role in message.author.roles):
        await message.channel.send("何様のつもり？")
        doM_role = discord.utils.get(message.guild.roles, id= 616212704818102275)
        await message.author.add_roles(doM_role)
        return

    try:
        how_many_delete = int(message.content.split()[1])
    except ValueError:
        await message.channel.send("不正な引数です")
        return
    except IndexError:
        await message.channel.purge(limit=None)
        return
    else:
        await message.channel.purge(limit=how_many_delete+1)


async def shiritori(message):
    """
    しりとりチャンネルでメッセージがんかンで終わったら対処する"""

    shiritori_n_list = [
        "ンジャメナ",
        "ンゴロンゴロ",
        "ンカイ",
        "ンガミ湖",
        "ンズワニ島","ンゼレコレ",
        "ンスタ",
        "ンスカ",
        "ンジャジジャ島"
    ]
    await message.channel.send(random.choice(shiritori_n_list))


async def dm_send(client1, message):
    if message.author.bot:
        return

    if len(message.content.split()) == 1:
        await message.channel.send("内容をいれてください")
        return

    try:
        user_id = int(message.content.split()[0])
    except ValueError:
        await message.channel.send("不正なIDです")
        return

    user = client1.get_user(user_id)
    if user is None:
        await message.channel.send("監視下にないユーザーIDです")
        return

    msg = ""
    for content in message.content.split()[1:]:
        msg += f"{content} "

    try:
        await user.send(msg)
    except discord.errors.Forbidden:
        await message.channel.send("権限がありません")


async def jms_notice(client1):
    """
    毎日9:10に雑談チャンネルでメンションを飛ばす"""

    ch = client1.get_channel(597130965927723048)
    await ch.send("<@&673349311228280862>\nhttps://minecraft.jp/servers/54d3529e4ddda180780041a7/vote\nhttps://minecraftservers.org/server/575658")


async def shiritori_reset(client1):
    """
    一週間に一度しりとりチャンネルをリセットする関数"""

    ch = client1.get_channel(603832801036468244)
    await ch.purge(limit=None)
    start_msg_list = [
        "しりとり",
        "霧雨魔理沙(きりさめまりさ)",
        "多々良小傘(たたらこがさ)",
        "リリカ・プリズムリバー"
    ]
    await ch.send(random.choice(start_msg_list))


async def twitter_connection(message):
    """
    私の鯖に投稿された日間整地量のグラフurlを取得してbytes型にしてtwitterに投稿する"""

    image_url = message.attachments[2].url
    res = requests.get(image_url)
    image = io.BytesIO(res.content)
    image.seek(0)
    image = image.read()

    today = datetime.date.today().strftime(r"%Y%m%d")

    try:
        import tokens_ConoHa
    except ModuleNotFoundError:
        consumer_key = os.getenv("consumer_key")
        consumer_secret = os.getenv("consumer_secret")
        twitter_token = os.getenv("twitter_token")
        token_secret = os.getenv("token_secret")
    else:
        consumer_key = tokens_ConoHa.consumer_key
        consumer_secret = tokens_ConoHa.consumer_secret
        twitter_token = tokens_ConoHa.twitter_token
        token_secret = tokens_ConoHa.token_secret

    auth = twitter.OAuth(consumer_key=consumer_key,
                        consumer_secret=consumer_secret,
                        token=twitter_token,
                        token_secret=token_secret)

    t = twitter.Twitter(auth=auth)

    pic_upload = twitter.Twitter(domain="upload.twitter.com", auth=auth)
    id_img1 = pic_upload.media.upload(media=image)["media_id_string"]
    t.statuses.update(status=f"#整地鯖\n{today}", media_ids=",".join([id_img1]))