import asyncio
import datetime
import json
import random

import bs4
import discord
from PIL import Image, ImageDraw, ImageFont
import requests

import commands

async def on_message(client1, message):
    """
    けい鯖にメッセージが投稿された時用の関数"""

    if message.content == "/test_member":
        test_member_role = discord.utils.get(message.guild.roles, id=586009049259311105) #実験台役職
        await message.author.add_roles(test_member_role)

    elif message.content == "/not test_member":
        test_member_role = discord.utils.get(message.guild.roles, id=586009049259311105) #実験台役職
        await message.author.remove_roles(test_member_role)

    elif message.content.startswith("/hide "):
        await hide_member(message)

    elif message.content.startswith("/find "):
        await find_member(message)

    elif message.content.startswith("/info "):
        await commands.info(client1, message)

    elif message.content.startswith("/last_login "):
        await commands.last_login(message)

    elif message.content.startswith("/weather "):
        await commands.weather(message)

    elif message.content.startswith("/name "):
        await commands.random_name(message)

    elif message.content.startswith("/break "):
        await commands.seichi_break(message)

    elif message.content.startswith("/build "):
        await commands.seichi_build(message)

    elif message.content.startswith("/delmsg"):
        await delmsg(message)

    elif message.content.startswith("/vote"):
        await commands.vote(message)

    elif message.content.startswith("/mcavatar "):
        await commands.mcavatar(client1, message)

    elif message.content.startswith("/random "):
        await commands.random_(message)

    elif message.content.startswith("/remove_role "):
        await remove_role(message)

    elif message.content == "/glist":
        await commands.glist(message, client1)

    elif message.content.startswith("/stack_eval "):
        await commands.stack_eval64(message)

    elif message.content.startswith("/stack_eval64 "):
        await commands.stack_eval64(message)

    elif message.content.startswith("/stack_eval16 "):
        await commands.stack_eval16(message)

    elif message.content.startswith("/stack_eval1 "):
        await commands.stack_eval1(message)

    elif message.content.startswith("/tanzaku "):
        await tanzaku(message)

    if message.channel.id == 603832801036468244:
        await shiritori(message)

    if message.channel.id == 639830406270681099:
        await dm_send(client1, message)

    if message.content == "/test":
        await kei_daily_score(client1)


async def on_raw_reaction_add(client1, payload):
    """
    リアクションが付けられた時用の関数"""

    channel = client1.get_channel(payload.channel_id)
    user = client1.get_user(payload.user_id)
    guild = client1.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if channel.id == 664286990677573680:
        if not payload.message_id == 975676283793055765:
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
            "\U0001f1ec",
            "\U0001f1ed",
            "\U0001f1ee",
            "\U0001f1ef"
        ]
        role_id_list = [
            586123567146729475, #シュータ
            678445373324263454, #乗り鉄
            678445640027734032, #撮り鉄
            678445821603217448, #音鉄
            870467547475091467, #V
            606481478078955530, #通知ほしい
            673349311228280862, #投票通知
            848183279458189312, #amongus
            975330354179244053, #VRC
            774551525083054090, #ミニゲーム
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

    if message.author.bot:
        return

    hide_role = discord.utils.get(message.guild.roles, id=616790954200006717)
    if message.content == "/hide me":
        if hide_role in message.author.roles:
            await message.channel.send("もう隠れているようです。私には見つけられませんでした。")
            return
        for role in message.author.roles:
            if role.id in (628175600007512066, 586000652464029697, 586000502635102209):
                await message.channel.send("警告を受けている人が隠れられるとでも思ってます？")
                return
        await message.author.add_roles(hide_role)
        await message.channel.send(f"{message.author.name}が隠れました。もーいーよ")
    else:
        try:
            user_id = int(message.content.split()[1])
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
            
            for role in member.roles:
                if role.id in (628175600007512066, 586000652464029697, 586000502635102209):
                    await message.channel.send("警告を受けている人を隠れさせることはできません")
                    return
            await member.add_roles(hide_role)
            await message.channel.send(f"{member.name}が隠れました。もーいーよ")
        except AttributeError:
            await message.channel.send("そのユーザーIDの人はこのサーバにはいません")


async def find_member(message):
    """
    かくれんぼなう役職を剥奪する関数"""

    if message.author.bot:
        return

    hide_role = discord.utils.get(message.guild.roles, id=616790954200006717)
    if message.content == "/find me":
        if not (hide_role in message.author.roles):
            await message.channel.send("もう見つけてるよ・・・？")
            return
        await message.author.remove_roles(hide_role)
        await message.channel.send(f"{message.author.name}、見～っけ！")
    else:
        try:
            user_id = int(message.content.split()[1])
        except ValueError:
            await message.channel.send("不正なIDです")
            return

        member = message.guild.get_member(user_id)
        try:
            if hide_role in member.roles:
                await member.remove_roles(hide_role)
                await message.channel.send(f"{member.name}、見～っけ！")
            else:
                await message.channel.send("もう見つけてるよ・・・")
        except AttributeError:
            await message.channel.send("そのユーザーIDの人はこのサーバにはいません")


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

    if message.author.bot:
        return

    try:
        how_many_delete = int(message.content.split()[1])
    except ValueError:
        await message.channel.send("不正な引数です")
        return
    except IndexError:
        if message.content == "/delmsg":
            await message.channel.purge(limit=None)
        else:
            await message.channel.send("後ろに余計な文字が付いています！")
        return
    else:
        await message.channel.purge(limit=how_many_delete+1)


async def remove_role(message):
    """
    引数のIDを持つ役職を一斉に外す"""

    admin_role = discord.utils.get(message.guild.roles, id=585999549055631408)
    if not (admin_role in message.author.roles):
        await message.channel.send("何様のつもり？")
        doM_role = discord.utils.get(message.guild.roles, id= 616212704818102275)
        await message.author.add_roles(doM_role)
        return

    if message.author.bot:
        return

    role_id = int(message.content.split()[1])
    role = discord.utils.get(message.guild.roles, id=role_id)
    n = 0
    for mem in role.members:
        await mem.remove_roles(role)
        n += 1

    await message.channel.send(f"{n}人から@{role.name}を剝奪しました")


async def shiritori(message):
    """
    しりとりチャンネルでメッセージがんかンで終わったら対処する"""

    if message.content.endswith("ん") or message.content.endswith("ン"):
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


async def kei_get_war(client1):
    kei_url = "https://ranking-gigantic.seichi.click/api/ranking/player/73b41f61-3b2b-4730-b775-564516101b3c?types=break"
    get_url = "https://ranking-gigantic.seichi.click/api/ranking/player/3dc5d243-2c85-4abb-aada-237511b410b8?types=break"
    try:
        res = requests.get(kei_url)
        res.raise_for_status()
        sorp = bs4.BeautifulSoup(res.text, "html.parser")
        kei_data_dict = json.loads(sorp.decode("utf-8"))
    except requests.exceptions.HTTPError:
        return

    kei_break = int(kei_data_dict[0]["data"]["raw_data"])

    try:
        res = requests.get(get_url)
        res.raise_for_status()
        sorp = bs4.BeautifulSoup(res.text, "html.parser")
        get_data_dict = json.loads(sorp.decode("utf-8"))
    except requests.exceptions.HTTPError:
        return

    get_break = int(get_data_dict[0]["data"]["raw_data"])

    nokori = get_break - kei_break
    today = datetime.date.today().strftime(r"%y-%m-%d")
    await client1.get_channel(793478659775266826).send(f"{today}\n{nokori}")


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


async def marichan_birthday(client1):
    """
    6/28は魔理沙botの誕生日です"""

    ch = client1.get_channel(585999375952642067)
    embed = discord.Embed(title="Happy Birthday!!:tada:",
                        description="本日、6月28日は魔理沙bot生誕三周年です。\n記念に現時刻から23:59(botの指示による)までに本サーバでガチャ券を寄こせと言うとガチャ券を3st進呈します。(インできる時間が合わない場合mineでpayする可能性があります)(イベントへの備えであまりあげられないことをご了承ください。)(アサルターなら受け取りに来る時間があるなら掘った方がいいと思います。)",
                        color=0xffff00)
    await ch.send(content=discord.utils.get(client1.get_guild(585998962050203672).roles, id=585998962050203672).name, embed=embed)


async def marichan_birthday_finish(client1):
    """
    しゅーりょーカンカンカン"""

    ch = client1.get_channel(585999375952642067)
    await ch.send("あはははは！おわりですおわりです！！！！")


async def jms_notice(client1):
    """
    毎日9:10に雑談チャンネルでメンションを飛ばす"""

    ch = client1.get_channel(597130965927723048)
    await ch.send(
        "<@&673349311228280862>\n"
        "https://minecraft.jp/servers/54d3529e4ddda180780041a7/vote\n"
        "https://monocraft.net/servers/Cf3BffNIRMERDNbAfWQm\n\n"
        "https://minecraftservers.org/server/575658"
    )



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


async def kei_daily_score(client1):
    import os
    import MySQLdb
    connection = MySQLdb.connect(
        host=os.getenv("mysql_host"),
        user=os.getenv("mysql_user"),
        passwd=os.getenv("mysql_passwd"),
        #db=os.getenv("mysql_db")
        db="kei_daily_score"
    )
    cur = connection.cursor()
    cur.execute("select * from kei_score")
    yesterday_score = cur.fetchone()[0]

    try:
        res = requests.get("https://ranking-gigantic.seichi.click/api/ranking/player/73b41f61-3b2b-4730-b775-564516101b3c?types=break")
        res.raise_for_status()
        data_dict = res.json()

    except requests.HTTPError:
        ch = client1.get_channel(793478659775266826)
        await ch.send("データが取れませんでした")
        return

    today_score = int(data_dict[0]["data"]["raw_data"])
    today_break = today_score - yesterday_score

    cur.execute(f"update kei_score set score={today_score}")
    connection.commit()

    embed = discord.Embed(
        title=f"{datetime.date.today().year}-{datetime.date.today().month}-{datetime.date.today().day}",
        description="{:,}".format(today_break),
        color=0xffff00
    )
    ch = client1.get_channel(793478659775266826)
    await ch.send(embed=embed)


async def tanzaku(message):
    negai = message.content.replace("/tanzaku ", "")
    bg_color = random.randint(0x000000, 0xffffff)
    letter_color = 0xffffff - bg_color
    image = Image.new("RGB", (130, 500), bg_color)
    moji = ImageDraw.Draw(image)
    font = ImageFont.truetype(r"./UDDigiKyokashoN-R.ttc", size=50)
    negai = list(negai)
    i = 0
    for x in range(2):
        for y in range(10):
            try:
                moji.text((80-x*50, y*50), text=negai[i], font=font, fill=letter_color)
            except IndexError:
                break
            i += 1
    username = list(message.author.display_name)
    font = ImageFont.truetype(r"./UDDigiKyokashoN-R.ttc", size=30)
    for y in range(10):
        try:
            moji.text((0, 100+y*30), text=username[y], font=font, fill=letter_color)
        except IndexError:
            break
    bg = Image.open("banboo.png")
    x = random.randint(0, 650)
    y = random.randint(0, 280)
    bg.paste(image, (x, y))
    bg.save("tanzaku.png")
    await message.channel.send(file=discord.File("tanzaku.png"))