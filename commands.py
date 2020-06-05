import asyncio
import datetime
import io
import json
import random
import re

import bs4
import discord
import requests
from PIL import Image,ImageDraw,ImageFont
from selenium import webdriver

def role_info(message, role_id):
    """
    実行サーバの役職の情報を取得する関数
    discord.Embedを返す"""

    role = discord.utils.get(message.guild.roles, id=role_id)
    try:
        role_info_embed = discord.Embed(title=role.name, color=role.color)
        if len(role.members) <= 10:
            member = ""
            for mem in role.members:
                member += f"{mem.mention}\n"
            role_info_embed = discord.Embed(title=role.name, description=member, color=role.color)
        else:
            role_info_embed = discord.Embed(title=role.name, description="11人以上いるため省略", color=role.color)
        role_info_embed.add_field(name="人数", value=f"{len(role.members)}", inline=False)
        role_info_embed.add_field(name="色", value=f"{role.color}", inline=False)
        role_made_time = (role.created_at + datetime.timedelta(hours=9)).strftime(r"%Y/%m/%d %H:%M")
        role_info_embed.add_field(name="作成日時", value=f"{role_made_time}　(JST)", inline=False)
        if role.mentionable:
            mention_able = "可"
        else:
            mention_able = "否"
        role_info_embed.add_field(name="メンションの可否", value=mention_able, inline=False)
        role_info_embed.set_footer(text=message.guild.name, icon_url=message.guild.icon_url)
        return role_info_embed

    except AttributeError:
        error_embed = discord.Embed(title="ERROR", description="ID指定が間違っているかこのサーバにない役職です", color=0xff0000)
        return error_embed


def guild_info(client1, guild_id):
    """
    サーバの情報を取得する関数
    discord.Embedを返す"""
    
    guild = client1.get_guild(guild_id)
    try:
        guild_info_embed = discord.Embed(title=guild.name, color=0xffffff)
        guild_info_embed.set_thumbnail(url=guild.icon_url)
        guild_info_embed.add_field(name="参加人数", value=f"{len(guild.members)}", inline=True)
        guild_made_time = (guild.created_at + datetime.timedelta(hours=9)).strftime(r"%Y/%m/%d %H:%M")
        guild_info_embed.add_field(name="作成日時", value=f"{guild_made_time}　(JST)", inline=True)
        return guild_info_embed
    except AttributeError:
        error_embed = discord.Embed(title="ERROR", description="ID指定が間違っているか本botの監視下にないサーバです", color=0xff0000)
        return error_embed


async def user_info(client1, user_id):
    """
    ユーザー情報を取得する関数
    discord.Embedを返す"""

    try:
        username = client1.get_user(user_id).name
    except AttributeError:
        bot_know = False
    else:
        bot_know = True

    try:
        user = await client1.fetch_user(user_id)
    except discord.errors.NotFound:
        error_embed = discord.Embed(title="ERROR", description="ID指定が間違っています", color=0xff0000)
        return error_embed

    user_info_embed = discord.Embed(title=user.name, color=0x000000)
    user_info_embed.set_thumbnail(url=user.avatar_url)
    user_info_embed.add_field(name="botかどうか", value=f"{user.bot}", inline=False)
    user_made_time = (user.created_at + datetime.timedelta(hours=9)).strftime(r"%Y/%m/%d %H:%M")
    user_info_embed.add_field(name="アカウント作成日時", value=f"{user_made_time}　(JST)", inline=False)
    user_info_embed.add_field(name=f"{client1.user.name}の監視下にあるか", value=f"{bot_know}", inline=False)
    return user_info_embed


async def info(client1, message):
    """
    role, guild, userの情報を表示する関数"""

    check_list = message.content.split()
    if not len(check_list) == 3:
        await message.channel.send("引数の数が正しくありません\nヒント: `/info␣[role, guild, user]␣ID`")
        return
    check = check_list[1]
    check_id = check_list[2]

    try:
        check_id = int(check_id)
    except ValueError:
        await message.channel.send("IDとして成り立ちません\nヒント: `/info␣[role, guild, user]␣ID`")
        return

    if check == "role":
        info_embed = role_info(message, check_id)
    elif check == "guild":
        info_embed = guild_info(client1, check_id)
    elif check == "user":
        info_embed = await user_info(client1, check_id)
    else:
        await message.channel.send("第二引数の指定が正しくありません\nヒント: `/info␣[role, guild, user]␣ID`")
        return

    await message.channel.send(embed=info_embed)


async def last_login(message):
    """
    第一引数のMCIDが最後に整地鯖にログインした日時を表示する関数"""

    mcid = message.content.split()[1].replace("\\", "")
    p = re.compile(r"^[a-zA-Z0-9_]+$")
    if not p.fullmatch(mcid):
        await message.channel.send("MCIDとして成り立ちません")
        return
    if not (len(mcid) >= 3 and len(mcid) <= 16):
        await message.channel.send("MCIDとして成り立ちません")
        return
    url = f"https://w4.minecraftserver.jp/player/{mcid}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "html.parser")
        if not f"{mcid.lower()}" in f"{soup.td}":
            await message.channel.send("整地鯖にログインしたことがないMCIDです")
            return
        last_login_datetime = str(soup.select("td")[1]).split("\n")[1]
        await message.channel.send(last_login_datetime)
    except requests.exceptions.HTTPError:
        await message.channel.send("現在データ参照元が使用できない状態です。しばらく待ってからもう一度お試しください。")


async def weather(message):
    """
    weatherコマンド対応用関数"""

    citycodes = {
        "稚内": "011000",
        "旭川": "012010",
        "網走": "013010",
        "根室": "014010",
        "釧路": "014020",
        "室蘭": "015010",
        "札幌": "016010",
        "函館": "017010",
        "青森": "020010",
        "八戸": "020030",
        "盛岡": "030010",
        "仙台": "040010",
        "秋田": "050010",
        "山形": "060010",
        "米沢": "060020",
        "酒田": "060030",
        "新庄": "060040",
        "福島": "070010",
        "若松": "070030",
        "水戸": "080010",
        "宇都宮": "090010",
        "前橋": "100010",
        "みなかみ": "100020",
        "さいたま": "110010",
        "秩父": "110030",
        "熊谷": "110020",
        "千葉": "120010",
        "銚子": "120020",
        "館山": "120030",
        "東京": "130010",
        "横浜": "140010",
        "新潟": "150010",
        "長岡": "150020",
        "富山": "160010",
        "金沢": "170010",
        "福井": "180010",
        "敦賀": "180020",
        "甲府": "190010",
        "長野": "200010",
        "松本": "200020",
        "岐阜": "210010",
        "高山": "210020",
        "静岡": "220010",
        "浜松": "220040",
        "名古屋": "230010",
        "豊橋": "230020",
        "津": "240010",
        "大津": "250010",
        "京都": "260010",
        "舞鶴": "260020",
        "大阪": "270000",
        "神戸": "280010",
        "奈良": "290010",
        "和歌山": "300010",
        "潮岬": "300020",
        "鳥取": "310010",
        "米子": "310020",
        "松江": "320010",
        "岡山": "330010",
        "広島": "340010",
        "下関": "350010",
        "山口": "350020",
        "萩": "350040",
        "徳島": "360010",
        "高松": "370000",
        "松山": "380010",
        "宇和島": "380030",
        "高知": "390010",
        "室戸岬": "390020",
        "福岡": "400010",
        "久留米": "400040",
        "佐賀": "410010",
        "長崎": "420010",
        "熊本": "430010",
        "人吉": "430040",
        "大分": "440010",
        "佐伯": "440040",
        "宮崎": "450010",
        "延岡": "450020",
        "都城": "450030",
        "鹿児島": "460010",
        "種子島": "460030",
        "那覇": "471010",
        "南大東": "472000",
        "宮古島": "473000",
        "石垣島": "474010",
        "与那国島": "474020"
    }
    try:
        city = citycodes[message.content.split()[1]]
    except KeyError:
        await message.channel.send(f"{message.content.split()[1]}は登録されていません")
        return
    url = f"http://weather.livedoor.com/forecast/webservice/json/v1?city={city}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        sorp = bs4.BeautifulSoup(res.text, "html.parser")
        weather_data_dict = json.loads(sorp.decode("utf-8"))
        title = weather_data_dict["title"] + "\n"
        description = weather_data_dict["publicTime"] + "に発表\n"
        description += "```\n" + weather_data_dict["description"]["text"] + "```\n```\n"
        for f in weather_data_dict["forecasts"]:
            description += f["dateLabel"] + "の天気は" + f["telop"] + "、"
            try:
                description += "最高気温は" + f["temperature"]["max"]["celsius"] + "℃、"
            except TypeError:
                description += "最高気温の情報なし"
            try:
                description += "最低気温は" + f["temperature"]["min"]["celsius"] + "℃\n"
            except TypeError:
                description += "最低気温の情報なし\n"
        description += "```"
        weather_embed = discord.Embed(title=title, description=description, color=0xfffffe)
        weather_embed.set_thumbnail(url=weather_data_dict["forecasts"][0]["image"]["url"])
        await message.channel.send(embed=weather_embed)
    except requests.exceptions.HTTPError:
        await message.channel.send("現在データ参照元が使用できない状態です。しばらく待ってからもう一度お試しください。")


async def random_name(message):
    """
    nameコマンド対応用関数"""

    try:
        name_length = int(message.content.split()[1])
    except ValueError:
        await message.channel.send("不正な引数です")
        return

    if not (name_length >= 1 and name_length <= 10):
        await message.channel.send("引数の値は1～10の範囲にしてください")
        return

    name_kouho = [
        "あ", "い", "う", "え", "お", "か", "き", "く", "け", "こ", "さ", "し", "す", "せ", "そ",
        "た", "ち", "つ", "て", "と", "な", "に", "ぬ", "ね", "の", "は", "ひ", "ふ", "へ", "ほ",
        "ま", "み", "む", "め", "も", "や", "ゆ", "よ", "ら", "り", "る", "れ", "ろ", "わ", "ゐ", "ゑ", "を", "ん",
        "が", "ぎ", "ぐ", "げ", "ご", "ざ", "じ", "ず", "ぜ", "ぞ", "だ", "ぢ", "づ", "で", "ど",
        "ば", "び", "ぶ", "べ", "ぼ", "ぱ", "ぴ", "ぷ", "ぺ", "ぽ", "ぱ", "ぴ", "ぷ", "ぺ", "ぽ"
    ]

    name = ""
    for i in range(name_length):
        name += random.choice(name_kouho)
    await message.channel.send(name)


async def seichi_break(message):
    """
    breakコマンド対応用関数"""

    mcid = message.content.split()[1].replace("\\", "")
    url = f"https://api.mojang.com/users/profiles/minecraft/{mcid}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        sorp = bs4.BeautifulSoup(res.text, "html.parser")
        player_data_dict = json.loads(sorp.decode("utf-8"))
        uuid = player_data_dict["id"]
    except requests.exceptions.HTTPError:
        await message.channel.send("現在データ参照元が使用できない状態です。しばらく待ってからもう一度お試しください。")
        return

    uuid_1 = uuid[:8]
    uuid_2 = uuid[8:12]
    uuid_3 = uuid[12:16]
    uuid_4 = uuid[16:20]
    uuid_5 = uuid[20:]
    uuid = f"{uuid_1}-{uuid_2}-{uuid_3}-{uuid_4}-{uuid_5}"
    url = f"https://w4.minecraftserver.jp/api/ranking/player/{uuid}?types=break"

    try:
        res = requests.get(url)
        res.raise_for_status()
        sorp = bs4.BeautifulSoup(res.text, "html.parser")
        player_data_dict = json.loads(sorp.decode("utf-8"))
    except requests.exceptions.HTTPError:
        await message.channel.send("現在データ参照元が使用できない状態です。しばらく待ってからもう一度お試しください。")
        return

    broke = int(player_data_dict[0]["data"]["raw_data"])
    rank = player_data_dict[0]["rank"]
    mc_avatar_url = f"http://avatar.minecraft.jp/{mcid}/minecraft/m.png"

    #────────────ここからコピペ禁止────────────
    if broke < 15:
        level = 1
    elif broke < 49:
        level = 2
    elif broke < 106:
        level = 3
    elif broke < 198:
        level = 4
    elif broke < 333:
        level = 5
    elif broke < 705:
        level = 6
    elif broke < 1265:
        level = 7
    elif broke < 2105:
        level = 8
    elif broke < 9557:#2105～9556までがこのelfi文内に入る
        level = 9
        n = 2015
        while True:
            n += 1242
            if broke < n:
                break
            else:
                level += 1
    elif broke < 11047:
        level = 15
    elif broke < 12835:
        level = 16
    elif broke < 14980:
        level = 17
    elif broke < 17554:
        level = 18
    elif broke < 20642:
        level = 19
    elif broke < 24347:
        level = 20
    elif broke < 28793:
        level = 21
    elif broke < 34128:
        level = 22
    elif broke < 40530:
        level = 23
    elif broke < 48212:
        level = 24
    elif broke < 57430:
        level = 25
    elif broke < 68491:
        level = 26
    elif broke < 81764:
        level = 27
    elif broke < 97691:
        level = 28
    elif broke < 212363:
        level = 29
        n = 97691
        while True:
            n += 19112
            if broke < n:
                break
            else:
                level += 1
    elif broke < 235297:
        level = 35
    elif broke < 262817:
        level = 36
    elif broke < 295891:
        level = 37
    elif broke < 335469:
        level = 38
    elif broke < 383022:
        level = 39
    elif broke < 434379:
        level = 40
    elif broke < 489844:
        level = 41
    elif broke < 549746:
        level = 42
    elif broke < 614440:
        level = 43
    elif broke < 684309:
        level = 44
    elif broke < 759767:
        level = 45
    elif broke < 841261:
        level = 46
    elif broke < 929274:
        level = 47
    elif broke < 1024328:
        level = 48
    elif broke < 1126986:
        level = 49
    elif broke < 1250000:
        level = 50
    elif broke < 2375000:
        level = 51
        n = 1250000
        while True:
            n += 125000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 4125000:
        level = 60
        n = 2375000
        while True:
            n += 175000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 6325000:
        level = 70
        n = 4215000
        while True:
            n += 220000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 9215000:
        level = 80
        n = 6325000
        while True:
            n += 280000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 13165000:
        level = 90
        n = 9215000
        while True:
            n += 360000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 13615000:
        level = 100
    elif broke < 17665000:
        level = 101
        n = 13615000
        while True:
            n += 450000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 22565000:
        level = 110
        n = 13615000
        while True:
            n += 490000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 27965000:
        level = 120
        n = 22565000
        while True:
            n += 540000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 33865000:
        level = 130
        n = 27965000
        while True:
            n += 590000
            if broke <n:
                break
            else:
                level += 1
    elif broke < 40465000:
        level = 140
        n = 33865000
        while True:
            n += 660000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 47865000:
        level = 150
        n = 40465000
        while True:
            n += 740000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 56065000:
        level = 160
        n = 47865000
        while True:
            n += 820000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 65265000:
        level = 170
        n = 56065000
        while True:
            n += 920000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 75265000:
        level = 180
        n = 65265000
        while True:
            n += 1000000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 85615000:
        level = 190
        n = 75265000
        while True:
            n += 1150000
            if broke < n:
                break
            else:
                level += 1
    elif broke < 87115000:
        level = 199
    else:
        level = 200
        star_level,amari = divmod(broke,87115000)
    #────────────ここまでコピペ禁止────────────

    broke = "{:,}".format(broke)
    try:
        embed = discord.Embed(title=f"{mcid}",description=f"整地量：{broke}\n順位：{rank}\nレベル：{level}☆{star_level}")
    except UnboundLocalError:
        embed = discord.Embed(title=f"{mcid}",description=f"整地量：{broke}\n順位：{rank}\nレベル：{level}")

    embed.set_thumbnail(url=mc_avatar_url)
    await message.channel.send(embed=embed)


async def vote(message):
    """
    投票機能"""

    vote_list = message.content.split()
    if len(vote_list) == 1:
        await message.channel.send("/vote␣投票の題名\nor\n/vote␣投票の題名␣候補1␣候補2␣・・・␣候補n(n≦20)")
        return

    if len(vote_list) > 22:
        await message.channel.send("候補が多すぎます。20個以下にしてください。")
        return

    if len(vote_list) == 2:
        vote_embed = discord.Embed(title=vote_list[1], color=0xfffffe)
        vote_msg = await message.channel.send(embed=vote_embed)
        await vote_msg.add_reaction("⭕")
        await vote_msg.add_reaction("❌")

    else:
        reaction_list = [
            "🇦", "🇧", "🇨", "🇩", "🇪",
            "🇫", "🇬", "🇭", "🇮", "🇯",
            "🇰", "🇱", "🇲", "🇳", "🇴",
            "🇵", "🇶", "🇷", "🇸", "🇹"
        ]

        vote_content = ""
        i = 0
        for msg in vote_list[2:]:
            vote_content += f"{reaction_list[i]}:{msg}\n"
            i += 1
        vote_embed = discord.Embed(title=vote_list[1], description=vote_content, color=0xfffffe)
        vote_msg = await message.channel.send(embed=vote_embed)

        for j in range(i):
            await vote_msg.add_reaction(reaction_list[j])


async def mcavatar(client1, message):
    """
    第一引数のMCIDのマイクラスキンを取得"""

    mcid = message.content.split()[1]
    mcid = mcid.replace("\\_", "_")
    url = f"https://api.mojang.com/users/profiles/minecraft/{mcid}"
    try:
        res = requests.get(url)
        res.raise_for_status()
        sorp = bs4.BeautifulSoup(res.text, "html.parser")
        try:
            mcid_dict = json.loads(sorp.decode("utf-8"))
        except json.decoder.JSONDecodeError:
            await message.channel.send("そのMCIDは存在しません")
            return
    except requests.exceptions.HTTPError:
        await message.channel.send("現在データ参照元が使用できない状態です。しばらく待ってからもう一度お試しください。")
        return

    url = f"https://minotar.net/armor/body/{mcid}/130.png"
    res = requests.get(url)
    image = io.BytesIO(res.content)
    image.seek(0)
    skin = Image.open(image)
    skin.save("skin.png")
    skin = discord.File("skin.png")
    await message.channel.send(file=skin)