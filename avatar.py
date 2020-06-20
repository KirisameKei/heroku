import os

import discord
import io
import requests
from PIL import Image, ImageDraw, ImageFont

client = discord.Client()

@client.event
async def on_ready():
    print("loginned")

@client.event
async def on_message(message):
    if message.author.bot:
        return
    if not message.content == "/icon":
        return
    avatar_url = message.author.avatar_url_as(format="png")
    pict = requests.get(avatar_url)
    pict = io.BytesIO(pict.content)
    pict.seek(0)
    pict = Image.open(pict)
    pict.save("./icon.png")
    image = discord.File("./icon.png")
    await message.channel.send(file=image)


client.run(os.getenv("discord_bot_token_1"))