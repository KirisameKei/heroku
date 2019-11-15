import discord
import diclog
import math
import os

client = discord.Client()

@client.event
async def on_ready():#このbotがログインしたら
    print(client.user.name+"がログインしました")#ターミナルにログインしたことを表示
    os.system("git config --global user.name "KirisameKei"")
    os.system("git config --global user.email "hayabusa4013@gmail.com"")
    os.system("git init")

@client.event
async def on_message(message):
    if not message.author.bot:
        if message.guild.id == 585998962050203672:
            with open("./diclog.py","w") as f:
                user_hatugensuu_dic = diclog.user_hatugensuu
                try:
                    before_hatugensuu = user_hatugensuu_dic[message.author.id]
                    after_hatugensuu = before_hatugensuu + 1
                except KeyError:
                    after_hatugensuu = 1

                if math.sqrt(after_hatugensuu) % 1 == 0:
                    testchannel = client.get_channel(597978849476870153)
                    await testchannel.send("ﾑﾑｯwwwﾚﾍﾞﾙｱｯﾌﾟwww\n"+message.author.name+"のレベル："+str(math.floor(math.sqrt(after_hatugensuu))))

                user_hatugensuu_dic[message.author.id] = after_hatugensuu
                f.write("user_hatugensuu = "+str(user_hatugensuu_dic))
                os.system("git add .")
                os.system("git commit")
                os.system("git push https://github.com/KirisameKei/discordbot origin master")




































client.run("NTk4MzQ4MjQxMDI0NTgxNjU1.XSVVjQ.YULYcsLW2b4wWyoxx2bRDjb7waY")#botを動かすのに必要
